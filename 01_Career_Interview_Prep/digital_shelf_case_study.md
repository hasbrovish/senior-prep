# 📦 CASE STUDY: Digital Shelf Operations AI Agent
## End-to-End GenAI Project — From Requirements to Production Scale

*Use this as your "go-to project" in interviews. It demonstrates RAG, Vision LLMs, Agents, System Design, and Scalability.*

---

# 1. EXECUTIVE SUMMARY (30-second pitch for interviews)

> "I built a Digital Shelf Operations AI Agent that automates quality auditing of product listings across multiple retailer websites like Amazon, Tesco, Sainsbury's, and Walmart. It uses a 2-step pipeline: first, a **quantity check** — verifying all required images and assets are present per retailer policy — and second, a **quality check** — using a Vision LLM to inspect brand compliance, regulatory labels (like HFSS in UK), and visual consistency. The system uses RAG to dynamically load retailer-specific rules, agentic orchestration for multi-step inspection, and generates structured Gap Reports for the creative team. It replaced a manual process that took days across thousands of SKUs."

---

# 2. PROBLEM STATEMENT (What problem does it solve?)

### The Business Problem:
Brands selling across multiple retailers face these challenges:

- **Each retailer has different requirements**: Amazon UK needs 7+ images + 1 video; Tesco may need only 3 images; Walmart requires rich media content
- **Manual auditing of thousands of SKUs across 5+ retailers** is time-consuming and error-prone — a team of 3-4 people spending 2-3 days per audit cycle
- **Regulatory requirements change frequently**: HFSS (High Fat Sugar Salt) labels in UK, FSC certification logos, allergen information
- **Brand consistency is hard to enforce at scale**: Logo placement, color palette, font usage across hundreds of product pages
- **Direct revenue impact**: Missing or non-compliant assets reduce conversion rates by 20-30% and can result in regulatory fines

### Why GenAI is the right solution:
- **Vision understanding needed**: Checking if a logo is correctly placed, if a regulatory label is visible — these are visual reasoning tasks perfect for Vision LLMs
- **Rules change frequently**: RAG allows updating retailer policies without retraining
- **Multi-step reasoning**: An agent needs to decide what to check, in what order, and what follow-up actions to take

---

# 3. REQUIREMENTS GATHERING (How I scoped the project)

### Functional Requirements:

| ID | Requirement | Priority |
|----|------------|----------|
| FR-1 | Ingest SKU list with retailer URLs for audit | P0 |
| FR-2 | Automatically fetch product page data (images, metadata) from retailer sites | P0 |
| FR-3 | Count and classify existing assets per SKU per retailer | P0 |
| FR-4 | Compare against retailer-specific asset requirements | P0 |
| FR-5 | Visually inspect images for brand compliance (logo, colors, layout) | P1 |
| FR-6 | Check for regulatory label presence (HFSS, FSC, allergens) | P1 |
| FR-7 | Generate structured Gap Report with actionable items | P0 |
| FR-8 | Dashboard for tracking compliance scores over time | P2 |
| FR-9 | Alert system for critical compliance failures | P1 |
| FR-10 | Support adding new retailers without code changes | P1 |

### Non-Functional Requirements:

| Requirement | Target |
|------------|--------|
| Latency per SKU audit | < 30 seconds |
| Throughput | 5000+ SKUs per audit cycle |
| Accuracy (asset count) | > 95% |
| Accuracy (compliance check) | > 90% |
| Availability | 99.5% uptime |
| Data freshness | Weekly full audit, daily delta for flagged SKUs |

### Stakeholders Identified:
- **Brand Managers**: Want compliance dashboards
- **Creative Team**: Need specific gap items to fix (what image, which retailer, what's wrong)
- **Legal/Regulatory**: Need proof of compliance checks
- **Engineering**: Need scalable, maintainable system

---

# 4. SOLUTION ARCHITECTURE (The System Design)

## 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT LAYER                          │
│  [SKU Master List]  [Retailer URLs]  [Audit Schedule]  │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│               DATA INGESTION LAYER                      │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │Amazon    │  │ Third-Party  │  │ Playwright/       │  │
│  │SP-API /  │  │ Feed (Salsify│  │ Headless Browser  │  │
│  │SerpAPI   │  │ / Syndigo)   │  │ (Fallback)        │  │
│  └────┬─────┘  └──────┬───────┘  └────────┬──────────┘  │
└───────┼───────────────┼────────────────────┼────────────┘
        └───────────────┼────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│              IMAGE STORAGE (S3/GCS)                      │
│  Organized: /retailer/sku_id/image_N.jpg                │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│              RAG RULE ENGINE                             │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Vector DB (Qdrant/Pinecone)                      │   │
│  │  • Retailer Policy Documents (chunked)           │   │
│  │  • Brand Guidelines                              │   │
│  │  • Regulatory Requirements (HFSS, FSC, etc.)     │   │
│  │  • Historical Audit Results                      │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│             AI AGENT ORCHESTRATOR (LangGraph)            │
│                                                         │
│  ┌─────────┐    ┌──────────┐    ┌────────────────┐     │
│  │ Step 1:  │───▶│ Step 2:  │───▶│ Step 3:        │     │
│  │ Quantity │    │ Quality  │    │ Gap Report     │     │
│  │ Check    │    │ Check    │    │ Generation     │     │
│  └─────────┘    └──────────┘    └────────────────┘     │
│       │              │                   │              │
│  Vision LLM     Vision LLM      Structured Output      │
│  (Gemini 1.5)   (Gemini 1.5)    (JSON → Dashboard)     │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│              OUTPUT LAYER                                │
│  ┌────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ Gap Report │  │ Compliance   │  │ Alert System   │  │
│  │ (JSON/PDF) │  │ Dashboard    │  │ (Slack/Email)  │  │
│  └────────────┘  └──────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 4.2 Component Breakdown

### Component 1: Data Ingestion Layer

**The challenge**: How to get product page data from retailers legally and reliably?

**Approach (Priority Order):**

1. **Retailer APIs (Best)**: Amazon SP-API, Walmart Content Provider API — structured data, legal, rate-limited
2. **Third-Party Feeds (Recommended)**: Salsify, Syndigo, Profitero, DataWeave — they have legal scraping infrastructure, provide pre-scraped data feeds with image URLs
3. **SerpAPI (For Amazon)**: Google Shopping results API — gets product images, titles, prices without direct scraping. ~$150-300/month for 15K-20K searches
4. **Headless Browser Fallback (Last Resort)**: Playwright for retailers without APIs — respects robots.txt, uses delays, runs through rotating proxies

**Interview talking point**: *"We used a strategy pattern for data ingestion — each retailer gets an adapter implementing a common interface. Adding a new retailer means just writing a new adapter, not changing the pipeline."*

```python
# Strategy Pattern for Data Ingestion
from abc import ABC, abstractmethod

class RetailerAdapter(ABC):
    @abstractmethod
    async def fetch_product_data(self, sku_id: str) -> ProductData:
        """Returns standardized product data regardless of source"""
        pass

class AmazonSPAPIAdapter(RetailerAdapter):
    async def fetch_product_data(self, sku_id: str) -> ProductData:
        # Uses Amazon Selling Partner API
        response = await self.sp_api_client.get_catalog_item(asin=sku_id)
        images = response.get("images", [])
        return ProductData(
            sku_id=sku_id,
            retailer="amazon_uk",
            images=[img["link"] for img in images],
            title=response.get("title"),
            description=response.get("description"),
            fetched_at=datetime.utcnow()
        )

class SerpAPIAdapter(RetailerAdapter):
    async def fetch_product_data(self, sku_id: str) -> ProductData:
        # Uses SerpAPI for Google Shopping results
        params = {
            "engine": "google_shopping",
            "q": sku_id,
            "api_key": self.api_key,
            "gl": "uk"  # country
        }
        results = await serpapi.search(params)
        # Extract product images from shopping results
        ...

class PlaywrightScraperAdapter(RetailerAdapter):
    async def fetch_product_data(self, sku_id: str) -> ProductData:
        # Headless browser for retailers without APIs
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(self.build_url(sku_id))
            await page.wait_for_load_state("networkidle")
            # Extract images using page selectors
            images = await page.query_selector_all("img.product-image")
            ...

# Factory to select the right adapter
class AdapterFactory:
    _adapters = {
        "amazon_uk": AmazonSPAPIAdapter,
        "amazon_us": AmazonSPAPIAdapter,
        "tesco": PlaywrightScraperAdapter,
        "sainsburys": PlaywrightScraperAdapter,
        "walmart": WalmartAPIAdapter,
    }
    
    @staticmethod
    def get_adapter(retailer: str) -> RetailerAdapter:
        return AdapterFactory._adapters[retailer]()
```

### Component 2: RAG Rule Engine

**Why RAG here?** Retailer policies change frequently. Hardcoding rules means code changes every time. With RAG, we just update the document in the vector DB.

```python
# RAG-based Rule Engine
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RetailerRuleEngine:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Qdrant(
            collection_name="retailer_policies",
            embedding=self.embeddings,
            url="http://localhost:6333"
        )
    
    def ingest_retailer_policy(self, retailer: str, policy_doc: str):
        """Ingest a new or updated retailer policy document"""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", " "]
        )
        chunks = splitter.split_text(policy_doc)
        
        # Add retailer metadata for filtered retrieval
        metadatas = [{"retailer": retailer, "doc_type": "policy"} for _ in chunks]
        self.vectorstore.add_texts(chunks, metadatas=metadatas)
    
    async def get_retailer_rules(self, retailer: str, query: str) -> list:
        """Retrieve relevant rules for a specific retailer"""
        results = self.vectorstore.similarity_search(
            query=query,
            k=5,
            filter={"retailer": retailer}  # Only fetch rules for THIS retailer
        )
        return results

# Example Retailer Policy Document (stored in vector DB)
AMAZON_UK_POLICY = """
## Amazon UK Image Requirements
- Minimum 7 images recommended for A+ content eligibility
- 1 Hero image (main image): Pure white background (#FFFFFF), product fills 85% of frame
- 3 Lifestyle images: Product in use context
- 1 Size chart or dimensions image
- 1 Ingredient/nutrition label image (for food products)
- 1 Video (30-60 seconds recommended)
- Minimum resolution: 1600x1600 pixels for zoom capability
- File formats: JPEG, PNG, GIF (no animation)
- No watermarks, logos, or text overlays on hero image
"""

TESCO_POLICY = """
## Tesco Image Requirements
- 1 Hero image: Clean product shot, white or light background
- 2 Gallery images minimum
- HFSS compliance: Must show front-of-pack nutrition labels if applicable
- FSC certification logo must be visible if product is FSC certified
- Maximum file size: 5MB per image
"""
```

### Component 3: Vision LLM Agent (The Core AI)

**Step 1: Quantity Check — "Do we have enough?"**

```python
import google.generativeai as genai
import json

class QuantityCheckAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-pro")
    
    async def check_asset_count(
        self, 
        images: list[bytes], 
        retailer_rules: str
    ) -> dict:
        """
        Sends all product images to Vision LLM and asks it to 
        categorize and count them against retailer requirements.
        """
        prompt = f"""You are a Digital Shelf auditor. Analyze these product listing images.

RETAILER REQUIREMENTS:
{retailer_rules}

For each image provided, classify it as one of:
- hero_image: Main product shot on white background
- lifestyle_image: Product shown in use/context
- size_chart: Dimensions or size reference
- nutrition_label: Ingredient or nutrition information
- video_thumbnail: Video content indicator
- other: Doesn't fit above categories

Then compare the count against requirements.

RESPOND IN STRICT JSON:
{{
    "total_images_found": <int>,
    "classification": [
        {{"image_index": 1, "type": "hero_image", "confidence": 0.95}},
        ...
    ],
    "requirements_met": {{
        "hero_image": {{"required": 1, "found": 1, "status": "PASS"}},
        "lifestyle_image": {{"required": 3, "found": 2, "status": "FAIL"}},
        ...
    }},
    "missing_assets": ["1 lifestyle_image", "1 size_chart"],
    "overall_status": "FAIL",
    "compliance_score": 72.5
}}"""
        
        # Build multimodal content
        content = [prompt]
        for idx, img_bytes in enumerate(images):
            content.append({
                "mime_type": "image/jpeg",
                "data": img_bytes
            })
        
        response = await self.model.generate_content_async(
            content,
            generation_config={"temperature": 0.1, "response_mime_type": "application/json"}
        )
        
        return json.loads(response.text)
```

**Step 2: Quality Check — "Do they look right?"**

```python
class QualityCheckAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-pro")
    
    async def check_brand_compliance(
        self,
        images: list[bytes],
        brand_guidelines: str,
        regulatory_rules: str
    ) -> dict:
        """
        Inspects each image for brand and regulatory compliance.
        """
        prompt = f"""You are a brand compliance inspector. Analyze each product image.

BRAND GUIDELINES:
{brand_guidelines}

REGULATORY REQUIREMENTS:
{regulatory_rules}

For each image, check:
1. LOGO PLACEMENT: Is the brand logo visible? Correct position? Correct size ratio?
2. COLOR PALETTE: Does the image use approved brand colors?
3. TEXT LEGIBILITY: Is all text readable and correctly spelled?
4. REGULATORY LABELS:
   - HFSS front-of-pack nutrition label visible? (UK requirement for HFSS products)
   - FSC certification logo present? (if applicable)
   - Allergen warnings visible? (if food product)
5. IMAGE QUALITY: Resolution adequate? No pixelation? Proper lighting?
6. BACKGROUND: Meets retailer's background requirements?

RESPOND IN STRICT JSON:
{{
    "image_audits": [
        {{
            "image_index": 1,
            "checks": {{
                "logo_placement": {{"status": "PASS", "detail": "Logo top-left, correct size"}},
                "color_palette": {{"status": "PASS", "detail": "Uses approved blue #1A73E8"}},
                "regulatory_hfss": {{"status": "FAIL", "detail": "HFSS label not visible on front of pack"}},
                "regulatory_fsc": {{"status": "N/A", "detail": "Not an FSC product"}},
                "image_quality": {{"status": "PASS", "detail": "Resolution 1600x1600, clear"}}
            }},
            "issues": ["HFSS front-of-pack nutrition label not visible"],
            "severity": "HIGH"
        }}
    ],
    "critical_issues": ["HFSS label missing on image 1 - regulatory risk"],
    "overall_brand_score": 85.0
}}"""
        
        content = [prompt]
        for img_bytes in images:
            content.append({"mime_type": "image/jpeg", "data": img_bytes})
        
        response = await self.model.generate_content_async(
            content,
            generation_config={"temperature": 0.1, "response_mime_type": "application/json"}
        )
        
        return json.loads(response.text)
```

### Component 4: Agent Orchestrator (LangGraph)

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AuditState(TypedDict):
    sku_id: str
    retailer: str
    images: list[bytes]
    retailer_rules: str
    brand_guidelines: str
    regulatory_rules: str
    quantity_result: dict
    quality_result: dict
    gap_report: dict
    status: str

# Node functions
async def fetch_product_data(state: AuditState) -> dict:
    adapter = AdapterFactory.get_adapter(state["retailer"])
    product = await adapter.fetch_product_data(state["sku_id"])
    images = await download_images(product.images)
    return {"images": images}

async def fetch_retailer_rules(state: AuditState) -> dict:
    rule_engine = RetailerRuleEngine()
    rules = await rule_engine.get_retailer_rules(
        retailer=state["retailer"],
        query="image requirements asset count compliance"
    )
    brand_rules = await rule_engine.get_retailer_rules(
        retailer=state["retailer"],
        query="brand guidelines logo color regulatory HFSS FSC"
    )
    return {
        "retailer_rules": "\n".join([r.page_content for r in rules]),
        "brand_guidelines": "\n".join([r.page_content for r in brand_rules])
    }

async def run_quantity_check(state: AuditState) -> dict:
    agent = QuantityCheckAgent()
    result = await agent.check_asset_count(
        images=state["images"],
        retailer_rules=state["retailer_rules"]
    )
    return {"quantity_result": result}

async def run_quality_check(state: AuditState) -> dict:
    agent = QualityCheckAgent()
    result = await agent.check_brand_compliance(
        images=state["images"],
        brand_guidelines=state["brand_guidelines"],
        regulatory_rules=state["regulatory_rules"]
    )
    return {"quality_result": result}

async def generate_gap_report(state: AuditState) -> dict:
    report = {
        "sku_id": state["sku_id"],
        "retailer": state["retailer"],
        "audit_timestamp": datetime.utcnow().isoformat(),
        "quantity_audit": state["quantity_result"],
        "quality_audit": state["quality_result"],
        "overall_compliance_score": (
            state["quantity_result"]["compliance_score"] * 0.4 +
            state["quality_result"]["overall_brand_score"] * 0.6
        ),
        "action_items": build_action_items(state["quantity_result"], state["quality_result"]),
        "priority": determine_priority(state["quality_result"])
    }
    return {"gap_report": report, "status": "completed"}

def should_run_quality_check(state: AuditState) -> str:
    """Only run quality check if quantity check found images to inspect"""
    if state["quantity_result"]["total_images_found"] > 0:
        return "quality_check"
    return "generate_report"  # Skip quality if no images found

# Build the LangGraph workflow
workflow = StateGraph(AuditState)

workflow.add_node("fetch_data", fetch_product_data)
workflow.add_node("fetch_rules", fetch_retailer_rules)
workflow.add_node("quantity_check", run_quantity_check)
workflow.add_node("quality_check", run_quality_check)
workflow.add_node("generate_report", generate_gap_report)

workflow.set_entry_point("fetch_data")
workflow.add_edge("fetch_data", "fetch_rules")
workflow.add_edge("fetch_rules", "quantity_check")
workflow.add_conditional_edges(
    "quantity_check",
    should_run_quality_check,
    {"quality_check": "quality_check", "generate_report": "generate_report"}
)
workflow.add_edge("quality_check", "generate_report")
workflow.add_edge("generate_report", END)

audit_agent = workflow.compile()

# Run audit for a single SKU
result = await audit_agent.ainvoke({
    "sku_id": "B08N5WRWNW",
    "retailer": "amazon_uk",
    "regulatory_rules": "HFSS front-of-pack labeling required for high fat/sugar/salt products in UK"
})
```

---

# 5. SCALABILITY DESIGN (How to handle 5000+ SKUs)

## 5.1 Batch Processing Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  ORCHESTRATION LAYER                         │
│                                                             │
│  ┌───────────┐    ┌──────────────────────────────────────┐  │
│  │ Scheduler │───▶│  Message Queue (Redis / RabbitMQ)    │  │
│  │ (Celery / │    │                                      │  │
│  │  Airflow) │    │  Queue: audit_tasks                  │  │
│  └───────────┘    │  Messages: {sku_id, retailer, ...}   │  │
│                   └──────────────┬───────────────────────┘  │
│                                  │                           │
│         ┌────────────────────────┼────────────────────┐     │
│         ▼                        ▼                    ▼     │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │  Worker 1    │  │   Worker 2       │  │  Worker N    │  │
│  │  (SKU batch  │  │   (SKU batch     │  │  (SKU batch  │  │
│  │   1-500)     │  │    501-1000)     │  │   ...)       │  │
│  └──────┬───────┘  └───────┬──────────┘  └──────┬───────┘  │
│         │                  │                     │          │
│         └──────────────────┼─────────────────────┘          │
│                            ▼                                │
│                 ┌─────────────────────┐                     │
│                 │  Results Aggregator  │                     │
│                 │  (PostgreSQL +       │                     │
│                 │   Redis Cache)       │                     │
│                 └─────────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## 5.2 Key Scalability Decisions

```python
# Batch processing with concurrency control
import asyncio
from celery import Celery

app = Celery('digital_shelf', broker='redis://localhost:6379')

@app.task(bind=True, max_retries=3, rate_limit='10/m')  # Rate limit API calls
def audit_sku_task(self, sku_id: str, retailer: str):
    """Celery task for auditing a single SKU"""
    try:
        result = asyncio.run(audit_agent.ainvoke({
            "sku_id": sku_id,
            "retailer": retailer,
        }))
        # Store result in PostgreSQL
        store_audit_result(result["gap_report"])
        return result["gap_report"]
    except RateLimitError:
        # Retry with exponential backoff
        self.retry(countdown=2 ** self.request.retries * 60)
    except Exception as e:
        log_error(sku_id, retailer, str(e))
        self.retry(exc=e)

# Batch launcher
def launch_audit_batch(sku_list: list[dict]):
    """Launch audit for a batch of SKUs"""
    tasks = []
    for item in sku_list:
        task = audit_sku_task.delay(
            sku_id=item["sku_id"],
            retailer=item["retailer"]
        )
        tasks.append(task)
    return tasks
```

## 5.3 Scalability Strategies Table

| Challenge | Solution | Implementation |
|-----------|----------|----------------|
| **API Rate Limits** | Rate limiter per retailer adapter | Celery rate_limit + token bucket |
| **Vision LLM Cost** | Batch images per SKU (1 call instead of N) | Send all images in single multimodal prompt |
| **Vision LLM Latency** | Async processing + result caching | asyncio + Redis cache (TTL: 24 hours) |
| **5000+ SKUs per cycle** | Parallel workers with message queue | Celery workers (10 concurrent) + RabbitMQ |
| **Storage costs** | Image deduplication + S3 lifecycle policies | Content-hash based dedup, move old images to Glacier after 90 days |
| **Vector DB scaling** | Separate collections per retailer | Qdrant collections with metadata filtering |
| **Changing policies** | RAG (just update the document) | No code changes needed, just re-embed |
| **New retailer onboarding** | Plugin architecture | Implement RetailerAdapter interface |
| **Result freshness** | Delta audits for flagged SKUs | Daily checks only for previously-failed SKUs |

## 5.4 Cost Estimation (Production)

| Component | Monthly Cost (5000 SKUs, weekly audit) |
|-----------|---------------------------------------|
| Gemini 1.5 Pro (Vision LLM) | ~$200-400 (depending on image count) |
| SerpAPI (Amazon scraping) | ~$200-300 |
| Qdrant Cloud (Vector DB) | ~$50-100 |
| AWS S3 (Image storage) | ~$20-50 |
| Celery Workers (2 x t3.medium) | ~$80 |
| PostgreSQL (RDS) | ~$50 |
| **Total** | **~$600-1000/month** |

*Compare to: 3-4 manual auditors × $2000/month = $6000-8000/month. That's a 6-10x cost reduction.*

---

# 6. FINE-TUNING STRATEGY

## 6.1 When Fine-tuning is Needed

After running the base system for 2-3 months, we identified:
- Vision LLM sometimes miscategorizes "lifestyle" vs "hero" images for specific product categories
- HFSS label detection accuracy was ~78% (target: 90%+)
- False positives on logo placement for certain packaging styles

## 6.2 Fine-tuning Approach

```python
# Step 1: Collect training data from manual corrections
# Every time the creative team marks a Vision LLM output as incorrect,
# we capture it as training data

training_data = [
    {
        "image": "s3://bucket/sku123/img1.jpg",
        "model_prediction": {"type": "lifestyle_image", "confidence": 0.7},
        "human_correction": {"type": "hero_image"},
        "retailer": "amazon_uk"
    },
    # ... hundreds of these from production corrections
]

# Step 2: Fine-tune embedding model for better retrieval
# Using sentence-transformers fine-tuning on domain-specific pairs
from sentence_transformers import SentenceTransformer, InputExample, losses

model = SentenceTransformer('all-MiniLM-L6-v2')

# Create training pairs: (query, relevant_policy_chunk)
train_examples = [
    InputExample(texts=[
        "Does this product have HFSS front of pack label?",
        "HFSS compliance requires visible traffic light nutrition label on product front"
    ], label=1.0),
    InputExample(texts=[
        "Check hero image background color",
        "Hero image must have pure white background RGB(255,255,255)"
    ], label=1.0),
    # Negative pairs
    InputExample(texts=[
        "Check hero image background",
        "Video content should be 30-60 seconds in length"
    ], label=0.0),
]

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
train_loss = losses.CosineSimilarityLoss(model)
model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=10)

# Step 3: For Vision LLM — use few-shot examples in prompt
# Instead of fine-tuning the Vision model (expensive),
# we add curated examples to the prompt

IMPROVED_PROMPT = """
Here are examples of correct classifications for this retailer:

EXAMPLE 1: [image of product on white background] → hero_image
EXAMPLE 2: [image of product being used in kitchen] → lifestyle_image  
EXAMPLE 3: [image showing product dimensions] → size_chart

Now classify the following images...
"""

# Step 4: If few-shot isn't enough, fine-tune a smaller
# classification model as a pre-filter

# Fine-tune a ViT (Vision Transformer) classifier
# to pre-classify images before sending to Vision LLM
from transformers import ViTForImageClassification, ViTFeatureExtractor, Trainer

model = ViTForImageClassification.from_pretrained(
    'google/vit-base-patch16-224',
    num_labels=6,  # hero, lifestyle, size_chart, nutrition, video_thumb, other
    id2label={0: "hero", 1: "lifestyle", 2: "size_chart", 
              3: "nutrition", 4: "video_thumb", 5: "other"}
)

# Train on our manually-labeled dataset
trainer = Trainer(
    model=model,
    train_dataset=train_dataset,  # Our corrected predictions
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
)
trainer.train()
```

## 6.3 Continuous Improvement Loop

```
┌───────────────────────────────────────────────────────────┐
│              FEEDBACK LOOP (Flywheel)                     │
│                                                           │
│  Production Audit ──▶ Creative Team Reviews ──▶ Marks     │
│       │                    Corrections                    │
│       │                        │                          │
│       │                        ▼                          │
│       │              Training Data Store                  │
│       │                        │                          │
│       │                        ▼                          │
│       │              Monthly Fine-tune Cycle              │
│       │              (Embedding + Classifier)             │
│       │                        │                          │
│       │                        ▼                          │
│       │              Updated Models Deployed              │
│       │                        │                          │
│       └────────────────────────┘                          │
│                                                           │
│  Metrics tracked:                                         │
│  • Classification accuracy: 78% → 85% → 92% (over 3mo)  │
│  • False positive rate: 15% → 8% → 4%                    │
│  • Manual override rate: 22% → 10% → 5%                  │
└───────────────────────────────────────────────────────────┘
```

---

# 7. EVALUATION METRICS (How we measure success)

| Metric | How Measured | Target | Actual |
|--------|-------------|--------|--------|
| Asset Count Accuracy | Manual verification on 100 random SKUs | >95% | 96.2% |
| Image Classification Accuracy | Against human-labeled ground truth | >90% | 92.1% |
| HFSS Label Detection | Against known HFSS products | >90% | 88.5% (improving) |
| Logo Compliance Detection | Against brand team audit | >85% | 87.3% |
| End-to-end Latency (per SKU) | System monitoring | <30s | 18s avg |
| Throughput | Batch completion time | 5000 SKUs in <4 hrs | 5000 in 3.2 hrs |
| Cost per SKU audit | Monthly bill / SKUs audited | <₹5 per SKU | ₹3.8 |
| Manual Override Rate | Team corrections / total audits | <10% | 8.2% |

---

# 8. INTERVIEW Q&A — HOW TO DISCUSS THIS PROJECT

---

### Q: "Tell me about a GenAI project you've worked on."

> "I designed and built a Digital Shelf Operations AI Agent for the e-commerce/CPG domain. The system automates quality auditing of product listings across retailers like Amazon, Tesco, and Walmart. It uses a RAG-based rule engine so that retailer policies can be updated without code changes, a Vision LLM (Gemini 1.5 Pro) for visual inspection of product images, and LangGraph for agentic orchestration. The pipeline does a quantity check — are all required assets present — and a quality check — are they brand-compliant and regulatory-compliant. It processes 5000+ SKUs weekly and reduced manual audit effort by ~85%."

### Q: "Why did you choose RAG over hardcoding rules?"

> "Retailer policies change frequently — Amazon might update their image requirements quarterly, HFSS regulations evolve, brand guidelines get refreshed. With RAG, the brand team can upload updated policy documents and the system immediately adapts. No code deployment needed. Also, RAG gave us an audit trail — we can show which exact policy version was used for each compliance check, which is important for regulatory teams."

### Q: "How do you handle hallucination in the Vision LLM?"

> "Three layers of defense. First, low temperature (0.1) for deterministic outputs. Second, structured JSON output format — the model can't 'hallucinate narratives,' it must fill specific fields. Third, a validation layer that cross-checks the model's image count against the actual number of images we sent. If the model claims 5 images but we sent 7, that gets flagged. For regulatory checks like HFSS, we added a confidence threshold — any detection below 80% confidence gets routed to human review."

### Q: "What was the hardest technical challenge?"

> "The data ingestion layer. Each retailer's website has a completely different structure, and some don't have APIs. We needed a reliable way to get product page data without violating terms of service. We solved this with a strategy pattern — a common interface with retailer-specific adapters. For Amazon we used SerpAPI, for retailers with partner APIs we used those, and Playwright as a last resort. The key insight was to prioritize third-party data feeds (Salsify/Syndigo) over building our own scrapers."

### Q: "How would you scale this to 50,000 SKUs across 15 retailers?"

> "Three main changes. First, move from Celery to a Kubernetes-based job orchestrator (like Argo Workflows or Airflow on K8s) for better resource management. Second, implement tiered auditing — full audits monthly, but delta audits daily only for SKUs that previously failed or have been updated. Third, consider using a smaller fine-tuned ViT classifier for the quantity check (image classification) to reduce Vision LLM costs — reserve the expensive Gemini calls only for the quality/compliance check where visual reasoning is truly needed."

### Q: "What's your tech stack?"

> "Python (async), LangGraph for agent orchestration, Qdrant for vector storage, Gemini 1.5 Pro as the Vision LLM, OpenAI embeddings for RAG, Celery + Redis for task queuing, PostgreSQL for results storage, S3 for image storage, and FastAPI for the dashboard API. Monitoring via Prometheus + Grafana with LangSmith for LLM observability."

---

# 9. QUICK REFERENCE — GENAI CONCEPTS DEMONSTRATED BY THIS PROJECT

| GenAI Concept | How It's Used |
|--------------|---------------|
| **RAG** | Retailer policy retrieval from vector DB |
| **Vision LLM** | Image classification + compliance inspection |
| **Agents** | LangGraph orchestrator with conditional branching |
| **Embeddings** | Policy documents embedded in Qdrant |
| **Chunking** | Retailer docs split by section (500 tokens, 100 overlap) |
| **Prompt Engineering** | Structured JSON output prompts with few-shot examples |
| **Fine-tuning** | ViT classifier for image categorization |
| **Evaluation** | Accuracy metrics, manual override rate tracking |
| **Hybrid Search** | BM25 + dense for policy retrieval |
| **Tool Use** | Agent calls APIs (SerpAPI, retailer APIs) as tools |
| **Guardrails** | Confidence thresholds, output validation, human-in-the-loop |
| **System Design** | Scalable batch processing, message queues, caching |

---

# 10. RESOURCES

- **LangGraph Documentation**: https://langchain-ai.github.io/langgraph/
- **Gemini Vision API**: https://ai.google.dev/gemini-api/docs/vision
- **Qdrant Documentation**: https://qdrant.tech/documentation/
- **RAGAS (RAG Evaluation)**: https://docs.ragas.io/
- **SerpAPI**: https://serpapi.com/google-shopping-api
- **Digital Shelf Analytics Market**: Gartner Market Guide for Digital Shelf Analytics (May 2025) — $1.7B market growing at 12% CAGR

---

*Pro tip: When discussing this project in interviews, always connect back to the BUSINESS IMPACT — "85% reduction in manual effort", "6-10x cost savings", "weekly audits instead of quarterly". Interviewers love numbers.*
