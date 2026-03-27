# API Design & SQL Practice — Complete SDE-2/SDE-3 Interview Guide

> Target audience: Jayanti Vishnoi — 5.5 YOE Java backend, targeting SDE-2/SDE-3 at product companies (Razorpay, Goldman, Flipkart, Amazon).
> Covers everything asked in 2024–2025 interviews.

---

# PART 1: API Design — Complete Interview Guide

---

## 1. REST API Design Principles

### 1.1 Resource Naming Conventions

REST resources are **nouns, not verbs**. The HTTP method expresses the action; the URL expresses the entity.

```
WRONG                        RIGHT
/getUser                     /users/{id}
/createOrder                 /orders
/deleteInvoice?id=123        /invoices/123
/getUserOrders               /users/{userId}/orders
```

Rules:
- Use **plural nouns**: `/users`, `/orders`, `/invoices` — not `/user`, `/order`
- Use **lowercase with hyphens** for multi-word resources: `/tax-returns`, `/payment-methods`
- Express **hierarchy** with nesting (max 2 levels deep): `/users/{userId}/orders/{orderId}`
- Avoid deep nesting beyond 2 levels — use query parameters instead: `/orders?userId=123&status=PENDING`
- Sub-resources vs query params: if the relationship is structural, use hierarchy. If it's filtering, use query params.

```
Structural:  GET /users/42/addresses          (addresses belong to user)
Filtering:   GET /orders?status=PENDING        (status is a filter, not a resource)
```

GSTN context: `/taxpayers/{gstin}/returns`, `/returns/{arn}/status` — GSTIN is the natural resource key.

---

### 1.2 HTTP Methods — When to Use Each

| Method | Semantics | Idempotent | Safe | Use Case |
|--------|-----------|------------|------|----------|
| GET | Read | Yes | Yes | Fetch resource(s) |
| POST | Create / trigger action | No | No | Create new resource, submit form |
| PUT | Full replace | Yes | No | Replace entire resource |
| PATCH | Partial update | No* | No | Update specific fields |
| DELETE | Remove | Yes | No | Delete resource |

*PATCH can be made idempotent with conditional logic but is not by default.

**GET**: Never mutate state. Cacheable. Response body allowed but unusual.

**POST**: Creates a new resource. The server assigns the ID. Response is `201 Created` with `Location: /orders/789` header. Not idempotent by default (calling twice creates two resources).

**PUT**: Replaces the entire resource. Client sends the full representation. Idempotent — calling `PUT /users/42` with the same body twice has the same effect. If the resource doesn't exist, some APIs create it (upsert semantics).

**PATCH**: Sends only the fields to update. Use when clients don't have or shouldn't send the full resource.
```json
PATCH /users/42
{ "email": "new@email.com" }
```
Contrast with PUT which requires sending name, phone, address, etc. too.

**DELETE**: Removes the resource. Returns `204 No Content` on success (no body). Idempotent — deleting a non-existent resource should return `404`, but deleting it twice shouldn't fail with `500`.

**HEAD**: Like GET but response has no body. Used to check if a resource exists or get headers (Last-Modified, Content-Length) without downloading the body.

**OPTIONS**: Returns allowed HTTP methods for a URL. Used by CORS preflight.

---

### 1.3 HTTP Status Codes — Which to Return When

**2xx Success**
| Code | Name | When |
|------|------|------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST that created a resource |
| 202 | Accepted | Request accepted for async processing |
| 204 | No Content | Successful DELETE, or PUT/PATCH with no response body |

**3xx Redirection**
| Code | Name | When |
|------|------|------|
| 301 | Moved Permanently | Resource URL changed forever |
| 302 | Found | Temporary redirect |
| 304 | Not Modified | Conditional GET, resource unchanged (used with ETag/If-None-Match) |

**4xx Client Errors**
| Code | Name | When |
|------|------|------|
| 400 | Bad Request | Malformed JSON, missing required field, invalid data type |
| 401 | Unauthorized | Not authenticated (no token or invalid token) |
| 403 | Forbidden | Authenticated but not authorized for this resource |
| 404 | Not Found | Resource does not exist |
| 405 | Method Not Allowed | PUT on a read-only endpoint |
| 409 | Conflict | Duplicate creation, optimistic locking failure, state conflict |
| 410 | Gone | Resource existed but was permanently deleted |
| 422 | Unprocessable Entity | Syntactically valid JSON but semantically wrong (business validation failure) |
| 429 | Too Many Requests | Rate limit exceeded |

**5xx Server Errors**
| Code | Name | When |
|------|------|------|
| 500 | Internal Server Error | Unhandled exception, unexpected failure |
| 502 | Bad Gateway | Upstream service returned invalid response |
| 503 | Service Unavailable | Overloaded, maintenance, circuit breaker open |
| 504 | Gateway Timeout | Upstream service timed out |

**Key distinctions interviewers test:**
- `401 vs 403`: 401 = "who are you?", 403 = "I know who you are, but no"
- `400 vs 422`: 400 = can't parse the request at all, 422 = parsed OK but business rule failed (e.g., date range invalid, amount negative)
- `409 vs 422`: 409 = conflict with existing state (duplicate GSTIN), 422 = input itself is wrong
- `202 vs 200`: Use 202 when the work happens asynchronously (file upload processing, batch job)

---

### 1.4 Idempotency

**Definition**: An operation is idempotent if performing it multiple times has the same effect as performing it once.

| Method | Idempotent? | Why |
|--------|-------------|-----|
| GET | Yes | Read-only, no state change |
| PUT | Yes | Sets resource to a specific state — same state every time |
| DELETE | Yes | Resource is gone after first call, subsequent calls have no additional effect |
| PATCH | No (by default) | Relative updates like "increment counter by 1" are not idempotent |
| POST | No | Creates a new resource each time |

**Implementing idempotency keys for POST:**

When a client retries a POST (due to network timeout), you must not create duplicate resources.

Flow:
1. Client generates a UUID: `Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000`
2. Client sends it in every request
3. Server checks Redis before processing:
   - If key exists and response is cached: return the cached response immediately
   - If key exists and processing: return `202 Accepted`
   - If key not found: process the request, store `(idempotencyKey -> response)` in Redis with TTL of 24h

```java
// Spring Boot filter for idempotency
@Component
public class IdempotencyFilter extends OncePerRequestFilter {

    private final RedisTemplate<String, String> redisTemplate;
    private final ObjectMapper objectMapper;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws IOException, ServletException {

        if (!"POST".equals(request.getMethod())) {
            chain.doFilter(request, response);
            return;
        }

        String idempotencyKey = request.getHeader("Idempotency-Key");
        if (idempotencyKey == null) {
            chain.doFilter(request, response);
            return;
        }

        String redisKey = "idempotency:" + idempotencyKey;
        String cachedResponse = redisTemplate.opsForValue().get(redisKey);

        if (cachedResponse != null) {
            // Return cached response
            IdempotencyRecord record = objectMapper.readValue(cachedResponse, IdempotencyRecord.class);
            response.setStatus(record.getStatus());
            response.setContentType("application/json");
            response.getWriter().write(record.getBody());
            return;
        }

        // Wrap response to capture it
        CachedBodyResponseWrapper wrappedResponse = new CachedBodyResponseWrapper(response);
        chain.doFilter(request, wrappedResponse);

        // Cache the response for 24 hours
        IdempotencyRecord record = new IdempotencyRecord(
            wrappedResponse.getStatus(),
            wrappedResponse.getCapturedBody()
        );
        redisTemplate.opsForValue().set(
            redisKey,
            objectMapper.writeValueAsString(record),
            24, TimeUnit.HOURS
        );

        // Write captured response to actual response
        response.setStatus(wrappedResponse.getStatus());
        response.getWriter().write(wrappedResponse.getCapturedBody());
    }
}
```

**GSTN context**: Return filing is inherently idempotent. When a taxpayer submits GSTR-1, the system generates an ARN (Acknowledgement Reference Number). If the same filing is submitted again:
- Same input hash → same ARN returned (deduplicated)
- No double-filing, no double-ARN generation
- ARN is stored with `(gstin + returnPeriod + returnType)` as the composite key
- Redis stores `idempotencyKey → arn` with 30-day TTL (within filing window)

---

### 1.5 Pagination: Offset vs Cursor-Based

**Offset-based pagination:**
```
GET /orders?page=5&size=20
```
```sql
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 100;
```

Problems:
- **Full table scan**: database must scan to row 100 before returning 20 rows. At row 10,000,000, this is slow.
- **Inconsistency**: if a new row is inserted while user is browsing, page 5 now shows a row that was on page 4 — items are skipped or duplicated.
- Does not scale beyond ~10,000 rows in practice.

**Cursor-based pagination:**
```
GET /orders?cursor=eyJpZCI6MTIzNCwidHMiOiIyMDI0LTAxLTE1In0=&size=20
```
The cursor is `base64({"id": 1234, "ts": "2024-01-15"})` — encoding of the last seen record.

```sql
-- Next page: fetch records after the cursor position
SELECT * FROM orders
WHERE (created_at, id) < ('2024-01-15', 1234)  -- keyset pagination
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

This uses the index on `(created_at, id)` — no offset scan, constant time regardless of position.

**Request format:**
```
GET /orders?cursor=<base64_token>&size=20
```

**Response format:**
```json
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTIxNCwidHMiOiIyMDI0LTAxLTE0In0=",
    "prevCursor": "eyJpZCI6MTI1NCwidHMiOiIyMDI0LTAxLTE2In0=",
    "hasMore": true,
    "pageSize": 20
  }
}
```

**Offset-based response format (for admin/reporting where you need "page X of Y"):**
```json
{
  "data": [...],
  "pagination": {
    "page": 5,
    "pageSize": 20,
    "totalElements": 4821,
    "totalPages": 242
  }
}
```

**When to use which:**
- Cursor: social feeds, real-time data, large datasets, infinite scroll — production user-facing APIs
- Offset: admin dashboards, reports where total count matters, small bounded datasets

---

### 1.6 API Versioning

Three strategies:

**1. URI versioning** (`/v1/`, `/v2/`)
```
GET /v1/users/42
GET /v2/users/42
```
- Most visible and widely used
- Easy to route at gateway level
- Breaks the "URI identifies a resource" principle (same resource, two URIs)
- Used by: **Stripe** (`api.stripe.com/v1`), **Twitter**, **Twilio**
- Best for: public APIs, mobile clients that can't set headers

**2. Header versioning** (`API-Version: 2`)
```
GET /users/42
API-Version: 2
```
- Keeps URIs clean
- Harder to test in browser
- Used by: **GitHub** (`X-GitHub-Api-Version: 2022-11-28`)

**3. Query parameter versioning** (`?version=2`)
```
GET /users/42?version=2
```
- Easy to test in browser
- Can accidentally cache wrong version
- Used by: some AWS APIs

**Trade-offs for interviews:**
- URI versioning wins for **public APIs** — it's explicit, bookmarkable, and works with every client.
- Header versioning wins for **internal microservices** — keeps routing clean.
- Never use query param versioning in production for critical APIs (caching issues).

**Backward compatibility rule**: New fields in responses are fine (additive). Removing fields or changing types is a breaking change requiring a new version.

---

### 1.7 Rate Limiting

**Why**: Prevent abuse, ensure fair usage, protect downstream services.

**Two main algorithms:**

**Token Bucket:**
- Bucket holds N tokens. Each request consumes 1 token.
- Tokens refill at a fixed rate (e.g., 10/second).
- Allows bursts up to bucket capacity.
- Good for: external APIs where you want to allow short bursts.

**Sliding Window Counter:**
- Counts requests in a rolling window (last 60 seconds).
- More accurate than fixed window (no boundary spikes).
- Implementation: Redis sorted set or Lua script.
- Good for: precise rate limiting.

**Redis + Lua script (atomic sliding window):**
```lua
-- KEYS[1] = rate_limit:userId:endpoint
-- ARGV[1] = current timestamp (ms)
-- ARGV[2] = window size (ms), e.g., 60000
-- ARGV[3] = max requests, e.g., 100

local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
local clearBefore = now - window

-- Remove timestamps outside the window
redis.call('ZREMRANGEBYSCORE', key, 0, clearBefore)

-- Count requests in window
local count = redis.call('ZCARD', key)

if count >= limit then
    return 0  -- rate limited
end

-- Add current request timestamp
redis.call('ZADD', key, now, now .. math.random())
redis.call('EXPIRE', key, math.ceil(window / 1000))
return 1  -- allowed
```

**Spring Boot implementation:**
```java
@Component
public class RateLimitInterceptor implements HandlerInterceptor {

    private final RedisTemplate<String, String> redisTemplate;
    private static final int MAX_REQUESTS = 100;
    private static final long WINDOW_MS = 60_000L;

    @Override
    public boolean preHandle(HttpServletRequest request,
                              HttpServletResponse response, Object handler) throws Exception {

        String userId = (String) request.getAttribute("userId"); // set by auth filter
        String key = "rate_limit:" + userId + ":" + getEndpointKey(request);

        long now = System.currentTimeMillis();
        DefaultRedisScript<Long> script = new DefaultRedisScript<>(SLIDING_WINDOW_LUA, Long.class);
        Long allowed = redisTemplate.execute(script,
            Collections.singletonList(key),
            String.valueOf(now),
            String.valueOf(WINDOW_MS),
            String.valueOf(MAX_REQUESTS));

        // Set response headers
        long remaining = allowed == 1 ? getRemainingCount(key) : 0;
        response.setHeader("X-RateLimit-Limit", String.valueOf(MAX_REQUESTS));
        response.setHeader("X-RateLimit-Remaining", String.valueOf(remaining));
        response.setHeader("X-RateLimit-Reset", String.valueOf((now + WINDOW_MS) / 1000));

        if (allowed == 0) {
            response.setStatus(429);
            response.setHeader("Retry-After", "60");
            response.setContentType("application/json");
            response.getWriter().write("""
                {"error": {"code": "RATE_LIMIT_EXCEEDED",
                 "message": "Too many requests. Retry after 60 seconds."}}
                """);
            return false;
        }
        return true;
    }
}
```

**Rate limit response headers:**
```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1706179200
Retry-After: 60
Content-Type: application/json

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Max 100 requests per minute.",
    "requestId": "req_abc123"
  }
}
```

**Rate limiting strategies:**
- Per user ID (authenticated endpoints)
- Per API key (B2B integrations)
- Per IP (unauthenticated endpoints)
- Per endpoint (write endpoints stricter than read)
- Distributed rate limiting with Redis (single source of truth across multiple pods)

---

### 1.8 Error Response Schema

Consistent error format across all endpoints is critical for API consumers.

**Standard error envelope:**
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Request validation failed",
    "details": [
      {
        "field": "amount",
        "message": "Amount must be greater than 0"
      },
      {
        "field": "currency",
        "message": "Currency code must be ISO 4217 (e.g., INR, USD)"
      }
    ],
    "requestId": "req_7f3a9b2c1d",
    "timestamp": "2024-01-15T10:30:00Z",
    "path": "/v1/payments"
  }
}
```

**Error code conventions:**
- Use SCREAMING_SNAKE_CASE for machine-readable codes
- Never expose internal error messages or stack traces in production
- `requestId` enables correlation with server logs

**Spring Boot global exception handler:**
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(
            MethodArgumentNotValidException ex, HttpServletRequest request) {

        List<ErrorDetail> details = ex.getBindingResult().getFieldErrors().stream()
            .map(fe -> new ErrorDetail(fe.getField(), fe.getDefaultMessage()))
            .collect(Collectors.toList());

        return ResponseEntity.status(400).body(ErrorResponse.builder()
            .code("VALIDATION_FAILED")
            .message("Request validation failed")
            .details(details)
            .requestId(MDC.get("requestId"))
            .path(request.getRequestURI())
            .build());
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(
            ResourceNotFoundException ex, HttpServletRequest request) {
        return ResponseEntity.status(404).body(ErrorResponse.builder()
            .code("RESOURCE_NOT_FOUND")
            .message(ex.getMessage())
            .requestId(MDC.get("requestId"))
            .path(request.getRequestURI())
            .build());
    }

    @ExceptionHandler(DuplicateResourceException.class)
    public ResponseEntity<ErrorResponse> handleConflict(
            DuplicateResourceException ex, HttpServletRequest request) {
        return ResponseEntity.status(409).body(ErrorResponse.builder()
            .code("RESOURCE_ALREADY_EXISTS")
            .message(ex.getMessage())
            .requestId(MDC.get("requestId"))
            .path(request.getRequestURI())
            .build());
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneral(
            Exception ex, HttpServletRequest request) {
        log.error("Unhandled exception for requestId={}", MDC.get("requestId"), ex);
        return ResponseEntity.status(500).body(ErrorResponse.builder()
            .code("INTERNAL_ERROR")
            .message("An unexpected error occurred")
            .requestId(MDC.get("requestId"))
            .path(request.getRequestURI())
            .build());
    }
}
```

---

### 1.9 HATEOAS

**What it is**: Hypermedia As The Engine Of Application State. Responses include links to related actions.

```json
{
  "orderId": "ord_123",
  "status": "PENDING",
  "_links": {
    "self": { "href": "/orders/ord_123" },
    "cancel": { "href": "/orders/ord_123/cancel", "method": "POST" },
    "payment": { "href": "/orders/ord_123/payment" }
  }
}
```

**When to use**: Rarely in practice. Used in:
- Public APIs where clients are truly generic (browsers, unknown third parties)
- APIs following full Richardson Maturity Model (Level 3)

**When to avoid** (most modern APIs):
- Internal microservices — clients know the API structure
- Mobile/frontend apps — clients are purpose-built
- Adds overhead, complexity, and response size without proportional benefit

Real answer: Stripe, GitHub, and most tier-1 APIs do NOT use HATEOAS. Know what it is for interviews; don't recommend it.

---

### 1.10 API Gateway Patterns

The API Gateway sits at the edge, handling cross-cutting concerns so individual services don't have to.

**Core responsibilities:**
```
Client → API Gateway → Service A
                    → Service B
                    → Service C
```

**Authentication/Authorization:**
- Validate JWT at the gateway (avoids each service doing it)
- Extract user claims and forward as headers (`X-User-Id`, `X-User-Roles`)
- Services trust the gateway — internal network only

**Rate Limiting:**
- Applied at gateway level per client/endpoint
- Uses shared Redis for distributed rate limit state

**Request Routing:**
- Path-based: `/v1/payments/*` → payment-service
- Header-based: `X-Tenant-Id: acme` → acme's dedicated cluster
- Canary: route 5% of traffic to new service version

**Request/Response Transformation:**
- Add/remove headers
- Transform response schema for backward compatibility
- Aggregate responses from multiple services (Backend for Frontend pattern)

**Other patterns:**
- Circuit breaker at gateway level (fail fast if service is down)
- Request caching for GET endpoints
- SSL termination
- Logging/tracing — assign `requestId`, propagate `traceId`

**Technology choices:**
- AWS API Gateway: managed, integrates with Lambda, limited transformation logic
- Kong: open-source, plugin ecosystem, runs on-prem or cloud
- Nginx + Lua: custom, high performance
- Spring Cloud Gateway: Java ecosystem, programmatic routing, integrates with Spring Security

---

## 2. OpenAPI / Swagger

### Why It Matters (Contract-First Development)

OpenAPI 3.0 is the industry standard for describing REST APIs. Benefits:
- **Contract-first**: frontend and backend teams agree on the API contract before implementation
- **Auto-generated client SDKs** in any language (Java, Python, TypeScript, Go)
- **Auto-generated documentation** with Swagger UI (try-it-out in browser)
- **API mocking**: frontend can work with mock servers before backend is ready
- **Validation**: request/response validation against the schema

### Complete OpenAPI 3.0 YAML Spec

```yaml
openapi: 3.0.3
info:
  title: Payment API
  description: API for processing payments
  version: 1.0.0
  contact:
    name: Platform Team
    email: platform@company.com

servers:
  - url: https://api.company.com/v1
    description: Production
  - url: https://api-staging.company.com/v1
    description: Staging

security:
  - bearerAuth: []

paths:
  /payments:
    post:
      operationId: createPayment
      summary: Create a new payment
      tags: [Payments]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreatePaymentRequest'
            example:
              amount: 50000
              currency: INR
              description: "Order payment"
              customerId: "cust_abc123"
      parameters:
        - name: Idempotency-Key
          in: header
          required: false
          schema:
            type: string
            format: uuid
          description: Client-generated UUID for idempotency
      responses:
        '201':
          description: Payment created
          headers:
            Location:
              schema:
                type: string
              description: URL of the created payment
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Payment'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '422':
          $ref: '#/components/responses/UnprocessableEntity'
        '429':
          $ref: '#/components/responses/RateLimited'

  /payments/{paymentId}:
    get:
      operationId: getPayment
      summary: Get a payment by ID
      tags: [Payments]
      parameters:
        - name: paymentId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Payment found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Payment'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    CreatePaymentRequest:
      type: object
      required: [amount, currency, customerId]
      properties:
        amount:
          type: integer
          minimum: 1
          description: Amount in smallest currency unit (paise for INR)
          example: 50000
        currency:
          type: string
          pattern: '^[A-Z]{3}$'
          description: ISO 4217 currency code
          example: INR
        description:
          type: string
          maxLength: 255
        customerId:
          type: string
          example: "cust_abc123"

    Payment:
      type: object
      properties:
        id:
          type: string
          example: "pay_xyz789"
        amount:
          type: integer
        currency:
          type: string
        status:
          type: string
          enum: [PENDING, PROCESSING, SUCCEEDED, FAILED]
        customerId:
          type: string
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    ErrorResponse:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string
            requestId:
              type: string

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
    UnprocessableEntity:
      description: Business validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
    RateLimited:
      description: Rate limit exceeded
      headers:
        Retry-After:
          schema:
            type: integer
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
```

### Spring Boot Swagger Integration

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.3.0</version>
</dependency>
```

```java
@RestController
@RequestMapping("/v1/payments")
@Tag(name = "Payments", description = "Payment processing endpoints")
public class PaymentController {

    @Operation(
        summary = "Create a payment",
        description = "Creates a new payment and returns the payment object"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "Payment created",
            content = @Content(schema = @Schema(implementation = Payment.class))),
        @ApiResponse(responseCode = "422", description = "Business validation failed",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @PostMapping
    public ResponseEntity<Payment> createPayment(
            @Parameter(description = "Idempotency key for safe retries", example = "550e8400-e29b-41d4-a716-446655440000")
            @RequestHeader(value = "Idempotency-Key", required = false) String idempotencyKey,
            @Valid @RequestBody CreatePaymentRequest request) {
        // ...
    }
}
```

Swagger UI available at: `http://localhost:8080/swagger-ui.html`

---

## 3. GraphQL vs REST vs gRPC

### REST
- **Best for**: Public APIs, browser clients, simple CRUD
- **Format**: JSON over HTTP
- **Caching**: HTTP-level caching works naturally (GET requests)
- **Tooling**: Universal — every language, every client supports it

### GraphQL
**Solves**: Over-fetching and under-fetching

Over-fetching: REST returns the full user object when mobile app only needs name and avatar.
Under-fetching: Fetching a feed requires `GET /posts`, then N calls to `GET /users/{id}` — the N+1 problem.

GraphQL lets the client specify exactly what fields it needs:
```graphql
query {
  user(id: "42") {
    name
    avatar
    recentPosts(limit: 5) {
      title
      createdAt
    }
  }
}
```

**N+1 problem it introduces**: When resolving `recentPosts`, GraphQL naively fetches each post's author with a separate DB query. Solution: DataLoader (batches and deduplicates queries).

**When to use GraphQL**:
- Mobile apps where bandwidth matters and field selection changes frequently
- BFF (Backend for Frontend) layer aggregating multiple services
- When client teams need to iterate on data requirements without backend deploys

**When NOT to use GraphQL**:
- Simple CRUD APIs
- File uploads (REST does this better)
- When caching is critical (GraphQL queries are all POST, not cacheable by default)

### gRPC
- **Format**: Protocol Buffers (binary, 3-10x smaller than JSON)
- **Transport**: HTTP/2 (multiplexing, header compression, bidirectional streaming)
- **Code gen**: `.proto` file → auto-generated client/server stubs in any language

```protobuf
syntax = "proto3";

service PaymentService {
  rpc CreatePayment(CreatePaymentRequest) returns (Payment);
  rpc StreamTransactions(StreamRequest) returns (stream Transaction);  // server streaming
}

message CreatePaymentRequest {
  int64 amount = 1;
  string currency = 2;
  string customer_id = 3;
}
```

**When gRPC beats REST**:
- Internal microservice communication (no browser involved)
- Low-latency requirements (binary serialization is faster than JSON)
- Bidirectional streaming (real-time data, live dashboards)
- Polyglot environments (auto-generated clients in Java, Go, Python from one `.proto`)
- Inter-datacenter calls where bandwidth matters

**gRPC limitations**:
- Not browser-native (needs gRPC-Web proxy)
- Binary format is not human-readable (harder to debug without tooling)
- Harder to test with curl

**Decision matrix:**
| Scenario | Choice |
|----------|--------|
| Public API for external developers | REST |
| Mobile app with complex data needs | GraphQL |
| Internal service-to-service (Java ↔ Go) | gRPC |
| Real-time streaming data | gRPC or WebSocket |
| Simple admin CRUD | REST |

---

## 4. Security

### 4.1 JWT (JSON Web Token)

**Structure**: `header.payload.signature` — three Base64URL-encoded parts separated by dots.

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyXzQyIiwicm9sZXMiOlsiVVNFUiJdLCJpYXQiOjE3MDYxNzkyMDAsImV4cCI6MTcwNjE4MjgwMH0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

- **Header**: `{"alg": "HS256", "typ": "JWT"}` — signing algorithm
- **Payload**: `{"sub": "user_42", "roles": ["USER"], "iat": 1706179200, "exp": 1706182800}` — claims
- **Signature**: `HMACSHA256(base64(header) + "." + base64(payload), secret)`

**Validation flow**:
1. Verify signature (ensures token wasn't tampered with)
2. Check `exp` claim (token not expired)
3. Check `iss` claim (issued by expected authority)
4. Check `aud` claim (intended for this service)

**Refresh token pattern**:
- Access token: short-lived (15 min), stored in memory
- Refresh token: long-lived (7 days), stored in HttpOnly cookie (not accessible to JS)
- When access token expires, client calls `/auth/refresh` with the refresh token cookie
- Server validates refresh token (checks DB/Redis for revocation), issues new access token
- Refresh token rotation: issue new refresh token on each refresh (invalidate old one)

```java
// Token validation in Spring Security
@Component
public class JwtAuthFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws IOException, ServletException {

        String authHeader = request.getHeader("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            chain.doFilter(request, response);
            return;
        }

        String token = authHeader.substring(7);
        try {
            Claims claims = Jwts.parserBuilder()
                .setSigningKey(signingKey)
                .build()
                .parseClaimsJws(token)
                .getBody();

            String userId = claims.getSubject();
            List<String> roles = claims.get("roles", List.class);

            UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(
                userId, null,
                roles.stream().map(SimpleGrantedAuthority::new).collect(Collectors.toList())
            );
            SecurityContextHolder.getContext().setAuthentication(auth);
            MDC.put("userId", userId);

        } catch (ExpiredJwtException e) {
            response.setStatus(401);
            response.getWriter().write("{\"error\": {\"code\": \"TOKEN_EXPIRED\"}}");
            return;
        } catch (JwtException e) {
            response.setStatus(401);
            response.getWriter().write("{\"error\": {\"code\": \"INVALID_TOKEN\"}}");
            return;
        }

        chain.doFilter(request, response);
    }
}
```

### 4.2 OAuth2 Flows

**Authorization Code Flow** (for user-delegated access):
```
1. User clicks "Login with Google"
2. App redirects to Google: /authorize?response_type=code&client_id=...&redirect_uri=...&scope=email
3. User authenticates with Google and consents
4. Google redirects back: /callback?code=AUTH_CODE
5. App server exchanges code for tokens: POST /token (code + client_secret)
6. Google returns access_token + refresh_token
7. App uses access_token to call Google APIs
```

Use when: User needs to grant your app access to their data on another platform.

**Client Credentials Flow** (for service-to-service):
```
1. Service A wants to call Service B
2. Service A sends: POST /token (client_id + client_secret + grant_type=client_credentials)
3. Auth server returns access_token
4. Service A calls Service B with Bearer token
5. Service B validates token against auth server (introspection or JWT verification)
```

Use when: No user involved — machine-to-machine communication, cron jobs, microservices.

### 4.3 API Key vs JWT vs OAuth2 — Decision Matrix

| Criteria | API Key | JWT | OAuth2 |
|----------|---------|-----|--------|
| User identity | No | Yes | Yes |
| Stateless | Yes | Yes | No (token store) |
| Revocation | Immediate (delete key) | Hard (until expiry) | Immediate |
| Complexity | Low | Medium | High |
| Refresh | No | Yes (refresh token) | Yes |
| Best for | B2B API access, simple services | Internal microservices, mobile apps | Third-party delegated access |
| Examples | Stripe secret key, AWS access key | Internal service auth | "Login with Google/GitHub" |

---

## 5. 20 API Design Interview Questions with Answers

### Q1: Design the API for a payment system.

**Answer:**
```
POST   /v1/payments                    Create a payment
GET    /v1/payments/{paymentId}        Get payment by ID
GET    /v1/payments?customerId=&status=&cursor=  List payments (cursor-based)
POST   /v1/payments/{paymentId}/refund  Refund a payment
POST   /v1/payments/{paymentId}/capture Capture an authorized payment

POST   /v1/customers                   Create customer
GET    /v1/customers/{customerId}      Get customer
POST   /v1/customers/{customerId}/payment-methods  Add payment method
GET    /v1/customers/{customerId}/payment-methods  List payment methods
```

Key design decisions:
- `POST /payments` returns `202 Accepted` if async (bank processing), `201 Created` if sync
- Idempotency-Key header required on `POST /payments`
- `POST /payments/{id}/refund` is a sub-resource action (refund is not a top-level resource, it belongs to a payment)
- Payment status transitions via state machine: `PENDING → PROCESSING → SUCCEEDED/FAILED`

### Q2: How do you handle backward compatibility?

**Answer:**
The cardinal rule: **never break existing clients**.

Additive changes are safe (backward compatible):
- Add new optional fields to response
- Add new optional request fields
- Add new endpoints
- Add new values to enums (clients should handle unknown values gracefully)

Breaking changes require a new version:
- Remove fields from response
- Change field names or types
- Change the meaning of a field
- Remove endpoints

Strategy:
1. Deploy v2 alongside v1 (never delete v1 immediately)
2. Deprecate v1 with a `Sunset` header: `Sunset: Sat, 01 Jan 2025 00:00:00 GMT`
3. Notify API consumers with at least 6-12 months notice
4. Monitor v1 usage; shut down only when traffic drops to zero

### Q3: What's the difference between PUT and PATCH?

**Answer:**
PUT replaces the entire resource. PATCH updates specific fields.

If a user has `{name, email, phone, address}` and you only want to update email:
- PUT requires sending all four fields. Missing fields may be set to null.
- PATCH sends only `{"email": "new@email.com"}` — other fields untouched.

Use PATCH when:
- The resource is large and sending the full object is wasteful
- Concurrent updates — two clients updating different fields won't clobber each other
- You don't have the full resource state on the client

Use PUT when:
- You want replace semantics (intentionally clearing fields)
- The full resource is small and simple

### Q4: How would you implement rate limiting?

**Answer:**
Covered in detail in section 1.7. Key points to mention in interview:
1. Choose sliding window counter (more accurate than fixed window)
2. Use Redis for distributed state (single source of truth across all pods)
3. Lua script for atomic operations (check + increment in one operation — no race condition)
4. Rate limit at multiple granularities: per user, per IP, per endpoint
5. Return `429` with `Retry-After` header
6. Apply at API Gateway level so services don't need to implement it individually

### Q5: How do you design an API for long-running operations?

**Answer:**
Use the async job pattern:

```
POST /v1/reports/generate        → 202 Accepted
                                   Location: /v1/jobs/job_abc123

GET  /v1/jobs/job_abc123         → 200 { status: "PROCESSING", progress: 45 }
GET  /v1/jobs/job_abc123         → 200 { status: "COMPLETED", resultUrl: "/v1/reports/rpt_xyz" }
GET  /v1/reports/rpt_xyz         → 200 { ... report data ... }
```

Alternative: Webhooks — client registers a callback URL, server POSTs to it when done.
Alternative: SSE (Server-Sent Events) — server pushes progress updates over a long-lived HTTP connection.

### Q6: How would you design pagination for a search API?

**Answer:**
Search APIs have a special challenge: relevance scores change as the index updates.

For search:
- Offset-based pagination is acceptable (results are ephemeral, not a stable dataset)
- Elasticsearch uses `search_after` (cursor-like) for deep pagination
- For user-facing search, most users never go beyond page 3 — offset is fine for shallow pagination

Response should include:
```json
{
  "results": [...],
  "total": 1423,
  "page": 1,
  "pageSize": 20,
  "nextPage": "/search?q=kafka&page=2&size=20"
}
```

### Q7: What is idempotency and why does it matter?

**Answer:**
Idempotency means calling the same operation multiple times has the same effect as calling it once. It matters because networks are unreliable — clients retry failed requests.

Without idempotency: client retries a payment → two charges on the customer's card.
With idempotency key: client retries → server detects the key, returns cached response → one charge.

Critical for: payment APIs, order creation, any operation with real-world side effects.

### Q8: How would you version an API when you can't break existing clients?

**Answer:**
Short-term: Use URI versioning (`/v2/`) with the old version still running.
Medium-term: Deploy with feature flags — same endpoint, different behavior based on header.
Long-term: Deprecate v1 with 12-month notice, sunset date in headers, emails to registered API consumers.

For mobile apps where you can't force upgrades: support the old version until app store data shows <1% of users on old version.

### Q9: How do you handle file uploads in a REST API?

**Answer:**
Two approaches:

**Multipart/form-data** (small files, <10MB):
```
POST /v1/documents
Content-Type: multipart/form-data

[file content + metadata]
```

**Pre-signed URL** (large files, better performance):
```
POST /v1/documents/upload-url
{ "filename": "report.pdf", "contentType": "application/pdf" }
→ { "uploadUrl": "https://s3.amazonaws.com/...?signature=...", "documentId": "doc_123" }

PUT <uploadUrl>                    (client uploads directly to S3)

POST /v1/documents/doc_123/confirm (tell server upload is complete)
```

The pre-signed URL approach is better because the file never goes through your API server, saving bandwidth and compute.

### Q10: What's the difference between authentication and authorization?

**Answer:**
- **Authentication** (AuthN): Verifying *who* you are. "This JWT is valid and belongs to user 42."
- **Authorization** (AuthZ): Verifying *what* you can do. "User 42 is allowed to access order 99."

In Spring Security: authentication happens in the filter chain (JwtAuthFilter). Authorization happens in `@PreAuthorize` or `SecurityConfig` rules.

HTTP status codes: 401 = authentication failed (unauthenticated), 403 = authorization failed (authenticated but not permitted).

### Q11: How do you handle concurrent updates to the same resource?

**Answer:**
**Optimistic locking** (preferred for most cases):
- Response includes a `version` field
- Client sends `If-Match: "version-5"` header on update
- Server rejects with `409 Conflict` if current version != provided version
- Client must re-fetch and retry

```sql
UPDATE orders SET status = 'SHIPPED', version = version + 1
WHERE id = 123 AND version = 5;
-- If 0 rows updated → another client updated first → 409
```

**Pessimistic locking** (for high-contention, short critical sections):
- `SELECT ... FOR UPDATE` in SQL
- Blocks other transactions from modifying the row
- Risk: deadlocks, performance issues under high concurrency

Use optimistic locking by default; use pessimistic locking only when contention is very high and the critical section is short.

### Q12: How would you design the API for a notification system?

**Answer:**
```
POST /v1/notifications                    Send notification
GET  /v1/users/{userId}/notifications     List user's notifications (cursor-paginated)
PATCH /v1/notifications/{id}              Mark as read: { "read": true }
POST /v1/notifications/mark-all-read      Bulk action for authenticated user
GET  /v1/notifications/preferences        Get notification preferences
PUT  /v1/notifications/preferences        Update preferences

Webhook registration:
POST /v1/webhooks                         Register webhook endpoint
GET  /v1/webhooks                         List webhooks
DELETE /v1/webhooks/{webhookId}           Remove webhook
```

### Q13: What is the Richardson Maturity Model?

**Answer:**
Four levels of REST maturity:
- Level 0: RPC over HTTP (SOAP, XML-RPC) — one endpoint for everything
- Level 1: Resources — multiple URIs, one per resource type
- Level 2: HTTP methods — correct use of GET/POST/PUT/DELETE and status codes
- Level 3: Hypermedia (HATEOAS) — responses include links to actions

Most production APIs are Level 2. Level 3 is theoretically correct but rarely practical. Aim for Level 2.

### Q14: How do you implement API caching?

**Answer:**

**HTTP caching headers:**
- `Cache-Control: public, max-age=3600` — cacheable by browser and CDN for 1 hour
- `Cache-Control: private, max-age=300` — only browser cache, not CDN (user-specific data)
- `Cache-Control: no-cache` — must revalidate with server before using cached response
- `ETag: "v5-abc123"` — conditional GET: client sends `If-None-Match: "v5-abc123"`, server returns `304 Not Modified` if unchanged

**Application-level caching (Redis):**
- Cache expensive GET responses: `GET /v1/products/{id}` → Redis key `product:{id}`, TTL 5 min
- Cache-aside pattern: check Redis first, miss → DB → write to Redis → return
- Invalidation: when product is updated, delete `product:{id}` from Redis

**CDN caching:**
- Static assets: `Cache-Control: public, max-age=31536000, immutable`
- API responses: `Cache-Control: public, s-maxage=60` (CDN caches for 60s, browser doesn't)

### Q15: How do you design an API for bulk operations?

**Answer:**
```
POST /v1/orders/bulk-create
{
  "operations": [
    { "action": "CREATE", "data": { ... } },
    { "action": "CREATE", "data": { ... } }
  ]
}

→ 207 Multi-Status
{
  "results": [
    { "status": 201, "id": "ord_123" },
    { "status": 422, "error": { "code": "VALIDATION_FAILED" } }
  ]
}
```

Key decisions:
- `207 Multi-Status` when individual operations have different outcomes
- Decide on all-or-nothing (transactional) vs partial success semantics upfront
- For large bulk operations (>1000 items), use async job pattern

### Q16: What headers should every API response include?

**Answer:**
```
Content-Type: application/json; charset=UTF-8
X-Request-Id: req_7f3a9b2c1d         (correlation ID for logging)
X-Trace-Id: trace_4f8a2c1b9d          (distributed tracing)
Cache-Control: no-cache               (for dynamic endpoints)
Strict-Transport-Security: max-age=31536000  (force HTTPS)
X-Content-Type-Options: nosniff       (prevent MIME sniffing)
X-Frame-Options: DENY                 (prevent clickjacking)
Vary: Accept-Encoding, Accept         (correct caching with content negotiation)
```

### Q17: How do you document API deprecation?

**Answer:**
```
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 01 Jun 2025 00:00:00 GMT
Link: <https://api.company.com/v2/users>; rel="successor-version"
```

Steps:
1. Add `Deprecation` and `Sunset` headers to old endpoint responses
2. Log which clients are still calling deprecated endpoints
3. Email registered API consumers 6-12 months before sunset
4. Deploy v2 before deprecating v1
5. Monitor traffic, extend deadline if significant clients still using it
6. Shut down v1 only when traffic is negligible

### Q18: How would you implement webhook delivery reliably?

**Answer:**
Webhooks are HTTP POST requests your server sends to clients when events occur.

Reliable delivery:
1. **At-least-once delivery**: store events in DB, retry until client returns 2xx
2. **Retry with exponential backoff**: 1s, 2s, 4s, 8s... up to 72h
3. **Signature verification**: sign payload with HMAC-SHA256 using shared secret
   - Header: `X-Webhook-Signature: sha256=<hmac>`
   - Client verifies before processing
4. **Event deduplication**: include `eventId` in payload; clients deduplicate by ID
5. **Delivery tracking**: store delivery attempts with status in DB

```json
{
  "eventId": "evt_abc123",
  "type": "payment.succeeded",
  "createdAt": "2024-01-15T10:30:00Z",
  "data": {
    "paymentId": "pay_xyz",
    "amount": 50000,
    "currency": "INR"
  }
}
```

### Q19: REST API design for an e-commerce order system?

**Answer:**
```
# Catalog
GET    /v1/products                   List products (cursor, filters)
GET    /v1/products/{productId}       Get product
GET    /v1/categories/{catId}/products Products by category

# Cart
GET    /v1/carts/{cartId}             Get cart
POST   /v1/carts                      Create cart
PUT    /v1/carts/{cartId}/items/{itemId}  Update item quantity
DELETE /v1/carts/{cartId}/items/{itemId}  Remove item

# Orders
POST   /v1/orders                     Place order (from cart)
GET    /v1/orders/{orderId}           Get order
GET    /v1/users/{userId}/orders      User's order history
POST   /v1/orders/{orderId}/cancel    Cancel order
POST   /v1/orders/{orderId}/return    Return request

# Payments
POST   /v1/payments                   Initiate payment
GET    /v1/payments/{paymentId}       Payment status
```

### Q20: How do you handle API security against common attacks?

**Answer:**

| Attack | Defense |
|--------|---------|
| SQL injection | Parameterized queries, ORM (never string concatenation in SQL) |
| CSRF | SameSite=Strict cookie, CSRF token for browser clients |
| XSS | Content-Security-Policy header, sanitize output |
| Mass assignment | Use DTOs (never bind request directly to JPA entity) |
| SSRF | Whitelist allowed URLs for any feature that fetches user-provided URLs |
| Broken access control | Check resource ownership on every request (`order.userId == authenticatedUserId`) |
| Rate limiting | As described in section 1.7 |
| Secrets in logs | Mask card numbers, tokens in logs; use structured logging |

---

# PART 2: SQL Coding Practice — 25 Problems with Solutions

**Schema used throughout:**

```sql
-- Employees
CREATE TABLE employees (
    id          INT PRIMARY KEY,
    name        VARCHAR(100),
    salary      DECIMAL(10,2),
    department_id INT,
    manager_id  INT,           -- self-referential FK
    hire_date   DATE
);

-- Departments
CREATE TABLE departments (
    id    INT PRIMARY KEY,
    name  VARCHAR(100)
);

-- Orders (e-commerce context)
CREATE TABLE orders (
    id          INT PRIMARY KEY,
    customer_id INT,
    product_id  INT,
    amount      DECIMAL(10,2),
    order_date  DATE,
    status      VARCHAR(20)
);

-- Customers
CREATE TABLE customers (
    id    INT PRIMARY KEY,
    name  VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

-- Products
CREATE TABLE products (
    id         INT PRIMARY KEY,
    name       VARCHAR(100),
    category   VARCHAR(50),
    price      DECIMAL(10,2),
    stock_qty  INT
);

-- User activity
CREATE TABLE user_activity (
    user_id       INT,
    activity_date DATE,
    PRIMARY KEY (user_id, activity_date)
);

-- Seats (cinema)
CREATE TABLE seats (
    seat_id   INT PRIMARY KEY,
    is_free   TINYINT(1)    -- 1 = available, 0 = taken
);
```

---

### Problem 1: Find the Second Highest Salary

**Problem**: Find the second highest salary in the employees table. Return NULL if no second highest exists.

```sql
SELECT MAX(salary) AS second_highest_salary
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

**Explanation**: Inner query finds the max salary. Outer query finds the max among all salaries below that — which is the second highest. Returns NULL if all employees have the same salary.

**Alternative using LIMIT/OFFSET** (fragile — fails with ties):
```sql
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;
```

**Alternative using dense_rank** (most robust):
```sql
SELECT salary AS second_highest_salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk = 2
LIMIT 1;
```

**Complexity**: O(n) full table scan.

---

### Problem 2: Find Employees Earning More Than Their Manager

**Problem**: Return employee names who earn more than their direct manager.

```sql
SELECT e.name AS employee_name,
       e.salary AS employee_salary,
       m.name AS manager_name,
       m.salary AS manager_salary
FROM employees e
INNER JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;
```

**Explanation**: Self-join on the same table. Alias `e` is the employee, alias `m` is their manager (found by `e.manager_id = m.id`). Filter rows where employee salary exceeds manager salary.

**Complexity**: O(n) with index on `manager_id` and `id`.

---

### Problem 3: Find Duplicate Emails

**Problem**: Find all emails that appear more than once in the customers table.

```sql
SELECT email, COUNT(*) AS count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;
```

**Explanation**: GROUP BY collapses rows with the same email. HAVING filters groups to those with more than one occurrence. HAVING vs WHERE: WHERE filters rows before grouping; HAVING filters groups after aggregation.

**Find duplicate rows with all duplicates listed:**
```sql
SELECT c1.*
FROM customers c1
INNER JOIN (
    SELECT email FROM customers GROUP BY email HAVING COUNT(*) > 1
) dups ON c1.email = dups.email
ORDER BY c1.email;
```

---

### Problem 4: Department with Highest Average Salary

**Problem**: Find the department(s) with the highest average salary.

```sql
SELECT d.name AS department, AVG(e.salary) AS avg_salary
FROM employees e
INNER JOIN departments d ON e.department_id = d.id
GROUP BY d.id, d.name
ORDER BY avg_salary DESC
LIMIT 1;
```

**If multiple departments tie for highest:**
```sql
SELECT d.name, AVG(e.salary) AS avg_salary
FROM employees e
INNER JOIN departments d ON e.department_id = d.id
GROUP BY d.id, d.name
HAVING AVG(e.salary) = (
    SELECT MAX(dept_avg) FROM (
        SELECT AVG(salary) AS dept_avg FROM employees GROUP BY department_id
    ) sub
);
```

**Complexity**: O(n) with index on `department_id`.

---

### Problem 5: Nth Highest Salary (Parameterized)

**Problem**: Create a query (or function) to find the Nth highest salary.

```sql
-- Using a variable for N
SET @N = 3;

SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET (@N - 1);
```

**As a stored function:**
```sql
DELIMITER //
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS DECIMAL(10,2)
READS SQL DATA
BEGIN
    DECLARE result DECIMAL(10,2);
    SET N = N - 1;
    SELECT DISTINCT salary INTO result
    FROM employees
    ORDER BY salary DESC
    LIMIT 1 OFFSET N;
    RETURN result;
END //
DELIMITER ;

-- Usage:
SELECT getNthHighestSalary(3);
```

**With window function (handles ties correctly):**
```sql
SELECT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk = 3  -- Replace 3 with N
LIMIT 1;
```

Note: DENSE_RANK gives the same rank to tied salaries, so "3rd highest" means 3rd distinct salary value.

---

### Problem 6: Employees Who Never Placed an Order (LEFT JOIN Pattern)

**Problem**: Find customers who have never placed an order.

```sql
SELECT c.id, c.name, c.email
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
```

**Explanation**: LEFT JOIN returns all customers including those with no matching orders. `WHERE o.id IS NULL` keeps only rows where no order was found — i.e., customers who never ordered.

**Alternative with NOT EXISTS** (often more readable to interviewers):
```sql
SELECT id, name, email
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

NOT EXISTS typically has better query optimizer support when orders table is large.

---

### Problem 7: Running Total / Cumulative Sum

**Problem**: For each order, show the running total of amount ordered by date.

```sql
SELECT
    id,
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date, id) AS running_total
FROM orders
ORDER BY order_date, id;
```

**Running total per customer (partition by customer):**
```sql
SELECT
    id,
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date, id
    ) AS customer_running_total
FROM orders
ORDER BY customer_id, order_date;
```

**Explanation**: `SUM(...) OVER (ORDER BY ...)` computes cumulative sum. The window grows with each row in order. `PARTITION BY` resets the running total for each customer.

**Complexity**: O(n log n) for the sort; O(n) for the window aggregation.

---

### Problem 8: Rank Employees Within Department

**Problem**: Rank employees by salary within their department. Show both RANK and DENSE_RANK.

```sql
SELECT
    e.name,
    d.name AS department,
    e.salary,
    RANK() OVER (
        PARTITION BY e.department_id
        ORDER BY e.salary DESC
    ) AS salary_rank,
    DENSE_RANK() OVER (
        PARTITION BY e.department_id
        ORDER BY e.salary DESC
    ) AS salary_dense_rank,
    ROW_NUMBER() OVER (
        PARTITION BY e.department_id
        ORDER BY e.salary DESC
    ) AS row_num
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;
```

**Difference between RANK, DENSE_RANK, ROW_NUMBER:**
- Salaries: 100, 100, 90, 80
- RANK:       1,   1,  3,  4  (gaps after ties)
- DENSE_RANK: 1,   1,  2,  3  (no gaps)
- ROW_NUMBER: 1,   2,  3,  4  (always unique)

---

### Problem 9: Most Recent Order Per Customer

**Problem**: Find the most recent order for each customer.

```sql
-- Using ROW_NUMBER (best approach)
SELECT customer_id, id AS order_id, order_date, amount
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY customer_id
               ORDER BY order_date DESC, id DESC
           ) AS rn
    FROM orders
) ranked
WHERE rn = 1;
```

**Alternative using self-join:**
```sql
SELECT o.*
FROM orders o
INNER JOIN (
    SELECT customer_id, MAX(order_date) AS max_date
    FROM orders
    GROUP BY customer_id
) latest ON o.customer_id = latest.customer_id
         AND o.order_date = latest.max_date;
```

Note: The self-join approach breaks if two orders have the same date (returns both). The ROW_NUMBER approach always returns exactly one row per customer.

---

### Problem 10: Customers Who Ordered Every Product (Relational Division)

**Problem**: Find customers who have ordered every product in the products table.

```sql
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING COUNT(DISTINCT product_id) = (SELECT COUNT(*) FROM products);
```

**Explanation**: Relational division. For each customer, count distinct products ordered. A customer who ordered every product will have a distinct product count equal to the total number of products.

**More precise — using NOT EXISTS (handles the case where orders reference deleted products):**
```sql
SELECT DISTINCT c.id, c.name
FROM customers c
WHERE NOT EXISTS (
    SELECT p.id FROM products p
    WHERE NOT EXISTS (
        SELECT 1 FROM orders o
        WHERE o.customer_id = c.id AND o.product_id = p.id
    )
);
```

Read: "Find customers for whom there is no product that they haven't ordered."

---

### Problem 11: Month-over-Month Growth Calculation

**Problem**: Calculate the month-over-month revenue growth percentage.

```sql
WITH monthly_revenue AS (
    SELECT
        DATE_FORMAT(order_date, '%Y-%m') AS month,
        SUM(amount) AS revenue
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
),
with_lag AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue
    FROM monthly_revenue
)
SELECT
    month,
    revenue,
    prev_month_revenue,
    ROUND(
        (revenue - prev_month_revenue) / prev_month_revenue * 100,
        2
    ) AS growth_pct
FROM with_lag;
```

**Explanation**: `LAG(revenue)` returns the revenue from the previous row (previous month). Growth = `(current - previous) / previous * 100`. First month has NULL for `prev_month_revenue` and NULL growth.

---

### Problem 12: Find Consecutive Available Seats

**Problem**: Find groups of 3+ consecutive available seats.

```sql
WITH numbered AS (
    SELECT
        seat_id,
        is_free,
        seat_id - ROW_NUMBER() OVER (ORDER BY seat_id) AS grp
    FROM seats
    WHERE is_free = 1
),
groups AS (
    SELECT MIN(seat_id) AS start_seat,
           MAX(seat_id) AS end_seat,
           COUNT(*) AS consecutive_count
    FROM numbered
    GROUP BY grp
)
SELECT start_seat, end_seat, consecutive_count
FROM groups
WHERE consecutive_count >= 3
ORDER BY start_seat;
```

**Key insight**: If seats 5, 6, 7 are all free, then `seat_id - ROW_NUMBER()` gives:
- 5 - 1 = 4
- 6 - 2 = 4
- 7 - 3 = 4

Same constant → they're in the same consecutive group. Then GROUP BY that constant to find each island.

---

### Problem 13: Find the Median Salary

**Problem**: Find the median salary of all employees.

```sql
-- Works in MySQL 8.0+
SELECT AVG(salary) AS median_salary
FROM (
    SELECT salary,
           ROW_NUMBER() OVER (ORDER BY salary) AS rn,
           COUNT(*) OVER () AS total
    FROM employees
) ranked
WHERE rn IN (FLOOR((total + 1) / 2), CEIL((total + 1) / 2));
```

**Explanation**: For odd count N, median is row `(N+1)/2`. For even count N, median is the average of rows `N/2` and `N/2 + 1`. `FLOOR` and `CEIL` of `(N+1)/2` cover both cases.

**Alternative (older MySQL):**
```sql
SELECT AVG(salary) AS median_salary
FROM (
    SELECT salary
    FROM (
        SELECT salary, @rownum := @rownum + 1 AS row_num,
               (SELECT COUNT(*) FROM employees) AS total
        FROM employees, (SELECT @rownum := 0) r
        ORDER BY salary
    ) sorted
    WHERE row_num IN (FLOOR((total + 1) / 2), CEIL((total + 1) / 2))
) median_rows;
```

---

### Problem 14: Top N Products Per Category

**Problem**: Find the top 3 highest-priced products in each category.

```sql
SELECT category, name, price
FROM (
    SELECT
        category,
        name,
        price,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY price DESC
        ) AS rn
    FROM products
) ranked
WHERE rn <= 3
ORDER BY category, price DESC;
```

**Use RANK() instead of ROW_NUMBER() if you want to include ties:**
```sql
-- With RANK(), if two products tie at rank 2, both are included (may return more than 3)
-- With ROW_NUMBER(), exactly 3 per category (arbitrary tiebreaking by DB)
-- With DENSE_RANK(), 3rd rank includes all ties at that rank
```

---

### Problem 15: Find Users Active on Consecutive Days

**Problem**: Find users who were active on at least 3 consecutive days.

```sql
WITH with_prev AS (
    SELECT
        user_id,
        activity_date,
        LAG(activity_date, 1) OVER (PARTITION BY user_id ORDER BY activity_date) AS prev1,
        LAG(activity_date, 2) OVER (PARTITION BY user_id ORDER BY activity_date) AS prev2
    FROM user_activity
)
SELECT DISTINCT user_id
FROM with_prev
WHERE DATEDIFF(activity_date, prev1) = 1
  AND DATEDIFF(prev1, prev2) = 1;
```

**Alternative using the island grouping technique:**
```sql
WITH grouped AS (
    SELECT
        user_id,
        activity_date,
        DATE_SUB(activity_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY activity_date) DAY) AS grp
    FROM user_activity
)
SELECT DISTINCT user_id
FROM grouped
GROUP BY user_id, grp
HAVING COUNT(*) >= 3;
```

---

### Problem 16: Pivot Table (Conditional Aggregation)

**Problem**: Show total orders per customer for each month (Jan-Mar) as columns.

```sql
SELECT
    customer_id,
    SUM(CASE WHEN MONTH(order_date) = 1 THEN amount ELSE 0 END) AS jan_total,
    SUM(CASE WHEN MONTH(order_date) = 2 THEN amount ELSE 0 END) AS feb_total,
    SUM(CASE WHEN MONTH(order_date) = 3 THEN amount ELSE 0 END) AS mar_total
FROM orders
WHERE YEAR(order_date) = 2024
GROUP BY customer_id
ORDER BY customer_id;
```

**Explanation**: MySQL doesn't have a native PIVOT operator. Use conditional aggregation: `SUM(CASE WHEN ... THEN value END)`. This effectively rotates rows into columns.

**Count of orders per month:**
```sql
SELECT
    customer_id,
    COUNT(CASE WHEN MONTH(order_date) = 1 THEN 1 END) AS jan_count,
    COUNT(CASE WHEN MONTH(order_date) = 2 THEN 1 END) AS feb_count,
    COUNT(CASE WHEN MONTH(order_date) = 3 THEN 1 END) AS mar_count
FROM orders
GROUP BY customer_id;
```

---

### Problem 17: Find Islands and Gaps in Date Sequences

**Problem**: Find date ranges (islands) of continuous activity for each user, and identify the gaps between them.

```sql
-- Step 1: Find islands (consecutive activity ranges)
WITH grouped AS (
    SELECT
        user_id,
        activity_date,
        DATE_SUB(activity_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY activity_date) DAY) AS grp
    FROM user_activity
),
islands AS (
    SELECT
        user_id,
        MIN(activity_date) AS island_start,
        MAX(activity_date) AS island_end,
        COUNT(*) AS days_active
    FROM grouped
    GROUP BY user_id, grp
)
SELECT * FROM islands ORDER BY user_id, island_start;
```

```sql
-- Step 2: Find gaps between islands
WITH islands AS (
    -- ... (same as above)
    SELECT user_id, island_start, island_end FROM ...
),
with_next AS (
    SELECT
        user_id,
        island_end,
        LEAD(island_start) OVER (PARTITION BY user_id ORDER BY island_start) AS next_island_start
    FROM islands
)
SELECT
    user_id,
    DATE_ADD(island_end, INTERVAL 1 DAY) AS gap_start,
    DATE_SUB(next_island_start, INTERVAL 1 DAY) AS gap_end,
    DATEDIFF(next_island_start, island_end) - 1 AS gap_days
FROM with_next
WHERE next_island_start IS NOT NULL
  AND DATEDIFF(next_island_start, island_end) > 1;
```

---

### Problem 18: Hierarchical Query (Employee-Manager Tree)

**Problem**: Show the full reporting chain for each employee (who reports to whom).

```sql
-- Recursive CTE (MySQL 8.0+)
WITH RECURSIVE hierarchy AS (
    -- Base case: top-level employees (no manager)
    SELECT id, name, manager_id, name AS path, 0 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees who report to someone in the hierarchy
    SELECT e.id, e.name, e.manager_id,
           CONCAT(h.path, ' -> ', e.name) AS path,
           h.depth + 1 AS depth
    FROM employees e
    INNER JOIN hierarchy h ON e.manager_id = h.id
)
SELECT id, name, depth, path
FROM hierarchy
ORDER BY path;
```

**Find all direct and indirect reports for a given manager:**
```sql
WITH RECURSIVE reports AS (
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id = 5  -- Start from manager with id=5

    UNION ALL

    SELECT e.id, e.name, e.manager_id, r.level + 1
    FROM employees e
    INNER JOIN reports r ON e.manager_id = r.id
)
SELECT * FROM reports ORDER BY level, name;
```

**Complexity**: O(n * depth) where depth is the tree depth. Add `MAXRECURSION` hint if tree depth is unbounded.

---

### Problem 19: Find Most Common Value Per Group

**Problem**: Find the most frequently ordered product for each customer.

```sql
WITH order_counts AS (
    SELECT
        customer_id,
        product_id,
        COUNT(*) AS order_count,
        RANK() OVER (
            PARTITION BY customer_id
            ORDER BY COUNT(*) DESC
        ) AS rnk
    FROM orders
    GROUP BY customer_id, product_id
)
SELECT oc.customer_id, p.name AS favorite_product, oc.order_count
FROM order_counts oc
INNER JOIN products p ON oc.product_id = p.id
WHERE rnk = 1
ORDER BY oc.customer_id;
```

**Note**: If two products are tied for most ordered by the same customer, RANK() returns both. Use ROW_NUMBER() if you want exactly one result per customer (arbitrary tiebreaking).

---

### Problem 20: Calculate Retention Rate (Cohort Analysis)

**Problem**: For each monthly cohort (users who first ordered in month X), what percentage are still ordering in month X+1?

```sql
WITH first_order AS (
    SELECT customer_id, MIN(order_date) AS first_order_date
    FROM orders
    GROUP BY customer_id
),
cohorts AS (
    SELECT
        DATE_FORMAT(fo.first_order_date, '%Y-%m') AS cohort_month,
        o.customer_id,
        DATE_FORMAT(o.order_date, '%Y-%m') AS activity_month,
        TIMESTAMPDIFF(MONTH, fo.first_order_date, o.order_date) AS months_since_first
    FROM orders o
    INNER JOIN first_order fo ON o.customer_id = fo.customer_id
),
cohort_sizes AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_size
    FROM cohorts
    WHERE months_since_first = 0
    GROUP BY cohort_month
)
SELECT
    c.cohort_month,
    c.months_since_first,
    COUNT(DISTINCT c.customer_id) AS active_users,
    cs.cohort_size,
    ROUND(COUNT(DISTINCT c.customer_id) * 100.0 / cs.cohort_size, 1) AS retention_pct
FROM cohorts c
INNER JOIN cohort_sizes cs ON c.cohort_month = cs.cohort_month
GROUP BY c.cohort_month, c.months_since_first, cs.cohort_size
ORDER BY c.cohort_month, c.months_since_first;
```

---

### Problem 21: Find Duplicate Rows and Keep Only One

**Problem**: The orders table has duplicate rows. Delete duplicates, keeping the one with the lowest id.

```sql
-- Step 1: Identify duplicates (same customer_id, product_id, order_date)
SELECT customer_id, product_id, order_date, MIN(id) AS keep_id, COUNT(*) AS cnt
FROM orders
GROUP BY customer_id, product_id, order_date
HAVING COUNT(*) > 1;

-- Step 2: Delete duplicates (keep the one with MIN id)
DELETE o FROM orders o
INNER JOIN (
    SELECT MIN(id) AS min_id, customer_id, product_id, order_date
    FROM orders
    GROUP BY customer_id, product_id, order_date
    HAVING COUNT(*) > 1
) dups ON o.customer_id = dups.customer_id
      AND o.product_id = dups.product_id
      AND o.order_date = dups.order_date
      AND o.id > dups.min_id;
```

**MySQL gotcha**: MySQL doesn't allow referencing the same table in a DELETE subquery directly. The JOIN approach above works. Alternatively, wrap in a subquery:

```sql
DELETE FROM orders
WHERE id NOT IN (
    SELECT min_id FROM (
        SELECT MIN(id) AS min_id
        FROM orders
        GROUP BY customer_id, product_id, order_date
    ) keep_these
);
```

---

### Problem 22: String Aggregation (GROUP_CONCAT)

**Problem**: For each customer, list all their ordered product names as a comma-separated string.

```sql
SELECT
    c.id,
    c.name AS customer_name,
    GROUP_CONCAT(p.name ORDER BY p.name SEPARATOR ', ') AS ordered_products,
    COUNT(DISTINCT o.product_id) AS product_count
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
INNER JOIN products p ON o.product_id = p.id
GROUP BY c.id, c.name
ORDER BY c.name;
```

**With DISTINCT to avoid repeating products:**
```sql
GROUP_CONCAT(DISTINCT p.name ORDER BY p.name SEPARATOR ', ')
```

**MySQL default GROUP_CONCAT limit is 1024 characters. For longer strings:**
```sql
SET SESSION group_concat_max_len = 65536;
```

**Equivalent in PostgreSQL**: `STRING_AGG(p.name, ', ' ORDER BY p.name)`

---

### Problem 23: Find Rows Where a Column Changed from Previous Row

**Problem**: Find orders where the status changed from the previous order for the same customer.

```sql
WITH with_prev_status AS (
    SELECT
        id,
        customer_id,
        order_date,
        status,
        LAG(status) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, id
        ) AS prev_status
    FROM orders
)
SELECT id, customer_id, order_date, prev_status, status AS new_status
FROM with_prev_status
WHERE prev_status IS NOT NULL
  AND status != prev_status
ORDER BY customer_id, order_date;
```

**Explanation**: `LAG(status)` returns the status of the previous row within the same customer partition. Filter rows where status differs from the previous one.

**For audit tables** (tracking all changes to a record over time), this pattern is very common:
```sql
LAG(column) OVER (PARTITION BY record_id ORDER BY changed_at) AS previous_value
```

---

### Problem 24: Calculate Percentile Using NTILE()

**Problem**: Classify employees into salary quartiles (top 25%, next 25%, etc.).

```sql
SELECT
    name,
    salary,
    NTILE(4) OVER (ORDER BY salary DESC) AS quartile,
    CASE NTILE(4) OVER (ORDER BY salary DESC)
        WHEN 1 THEN 'Top 25%'
        WHEN 2 THEN 'Upper Middle 25%'
        WHEN 3 THEN 'Lower Middle 25%'
        WHEN 4 THEN 'Bottom 25%'
    END AS salary_band
FROM employees
ORDER BY salary DESC;
```

**Find employees in the top 10th percentile:**
```sql
SELECT name, salary
FROM (
    SELECT name, salary,
           NTILE(10) OVER (ORDER BY salary DESC) AS decile
    FROM employees
) deciles
WHERE decile = 1;
```

**NTILE(n)** divides rows into n buckets as evenly as possible. If rows don't divide evenly, earlier buckets get one extra row.

**More precise percentile using PERCENT_RANK():**
```sql
SELECT name, salary,
       ROUND(PERCENT_RANK() OVER (ORDER BY salary) * 100, 1) AS percentile_rank
FROM employees;
```

---

### Problem 25: Complex Join — Find Orders Where All Items Are in Stock

**Problem**: Find orders where every item in the order has sufficient stock.

```sql
-- Schema adjustment: an order can have multiple line items
-- orders_items table:
-- order_id, product_id, quantity

SELECT DISTINCT o.id AS order_id, o.customer_id, o.order_date
FROM orders o
WHERE NOT EXISTS (
    SELECT 1
    FROM order_items oi
    INNER JOIN products p ON oi.product_id = p.id
    WHERE oi.order_id = o.id
      AND p.stock_qty < oi.quantity  -- this item is under-stocked
);
```

**Explanation**: "All items in stock" = "there is no item in the order that is out of stock." Using NOT EXISTS with the negated condition is the cleanest way to express universal quantification in SQL.

**Alternative using LEFT JOIN:**
```sql
SELECT o.id AS order_id
FROM orders o
LEFT JOIN (
    SELECT oi.order_id
    FROM order_items oi
    INNER JOIN products p ON oi.product_id = p.id
    WHERE p.stock_qty < oi.quantity
) understocked ON o.id = understocked.order_id
WHERE understocked.order_id IS NULL;
```

**Count of fulfillable orders per customer:**
```sql
SELECT o.customer_id, COUNT(*) AS fulfillable_orders
FROM orders o
WHERE NOT EXISTS (
    SELECT 1 FROM order_items oi
    INNER JOIN products p ON oi.product_id = p.id
    WHERE oi.order_id = o.id AND p.stock_qty < oi.quantity
)
GROUP BY o.customer_id;
```

---

## Quick Reference: SQL Window Functions

```sql
-- Syntax template
function_name(expr) OVER (
    [PARTITION BY partition_expr]
    [ORDER BY order_expr [ASC|DESC]]
    [ROWS|RANGE BETWEEN frame_start AND frame_end]
)

-- Ranking functions
ROW_NUMBER()                           -- unique sequential number
RANK()                                 -- same rank for ties, gaps after
DENSE_RANK()                           -- same rank for ties, no gaps
NTILE(n)                               -- bucket into n groups
PERCENT_RANK()                         -- relative rank 0.0 to 1.0

-- Value functions
LAG(col, offset, default)              -- value from N rows before
LEAD(col, offset, default)             -- value from N rows ahead
FIRST_VALUE(col)                       -- first value in window
LAST_VALUE(col)                        -- last value in window
NTH_VALUE(col, n)                      -- nth value in window

-- Aggregate functions (as window functions)
SUM(col) OVER (...)                    -- running/cumulative sum
AVG(col) OVER (...)                    -- moving average
COUNT(col) OVER (...)                  -- running count
MIN/MAX(col) OVER (...)                -- running min/max

-- Frame specification
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW    -- from start to current
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW            -- last 3 rows (moving avg)
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING    -- from current to end
RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW  -- last 7 days
```

---

## Quick Reference: Common Query Patterns

```sql
-- Deduplication: keep one row per group
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY group_col ORDER BY priority_col) rn
    FROM table
) t WHERE rn = 1;

-- Top N per group
SELECT * FROM (
    SELECT *, RANK() OVER (PARTITION BY group_col ORDER BY sort_col DESC) rnk
    FROM table
) t WHERE rnk <= N;

-- Year-over-year comparison
SELECT year, revenue,
       LAG(revenue) OVER (ORDER BY year) AS prev_year,
       revenue - LAG(revenue) OVER (ORDER BY year) AS yoy_change
FROM yearly_revenue;

-- Consecutive sequence detection
SELECT *, col - ROW_NUMBER() OVER (ORDER BY col) AS grp FROM table;
-- Same grp value = consecutive sequence

-- Hierarchy traversal (recursive CTE)
WITH RECURSIVE tree AS (
    SELECT * FROM nodes WHERE parent_id IS NULL
    UNION ALL
    SELECT n.* FROM nodes n JOIN tree t ON n.parent_id = t.id
)
SELECT * FROM tree;
```

---

*End of Section: API Design & SQL Practice*
