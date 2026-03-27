# SECTION 3: HIBERNATE / JPA — Interview Answers (Q76–Q90)
## With GSTN Codebase References

---

### Q76. What is the difference between JPA, Hibernate, and Spring Data JPA?

**Answer:**

| Layer | What | Role |
|-------|------|------|
| **JPA** (Jakarta Persistence API) | **Specification** (interfaces + annotations) | Defines WHAT ORM should do: `@Entity`, `@Table`, `EntityManager` |
| **Hibernate** | **Implementation** of JPA | Provides HOW: caching, dirty checking, HQL, connection pooling |
| **Spring Data JPA** | **Abstraction** above JPA/Hibernate | Eliminates boilerplate: auto-generates queries from method names, `JpaRepository` |

```
Spring Data JPA (convenience layer)
    ↓ uses
JPA (specification — javax.persistence.*)
    ↓ implemented by
Hibernate (actual ORM engine)
    ↓ uses
JDBC (database communication)
    ↓ connects to
MySQL / PostgreSQL
```

**GSTN Stack:** Hibernate 4.2.11 as the JPA implementation + Spring Data JPA for repositories + MySQL 8.0.19.

```java
// JPA annotations (standard)
@Entity
@Table(name = "WF_TASK")
public class WfTask implements Serializable { ... }

// Spring Data JPA repository (convenience)
@Repository
public interface GspAuthToknLogRepository extends JpaRepository<GspAuthTokenLog, Long> {
    // Spring Data auto-generates implementation at runtime
}

// Hibernate-specific (non-JPA) features used in GSTN:
// @BatchSize, StatelessSession, HQL-specific syntax
```

---

### Q77. Entity states — Transient, Persistent, Detached, Removed?

**Answer:**

```
                  new Entity()
                      │
                      ▼
                 ┌──TRANSIENT──┐
                 │  Not in PC  │
                 │  Not in DB  │
                 └──────┬──────┘
                 persist() / save()
                        │
                        ▼
                 ┌──PERSISTENT─┐
                 │  In PC ✓    │ ← find() / get() / query results
                 │  In DB ✓    │
                 │  Auto dirty │ ← Changes auto-synced to DB on flush
                 │  checking   │
                 └──┬──────┬───┘
           detach()/   │ remove()
           clear()/    ▼
           close()  ┌─REMOVED──┐
              │     │ In PC    │
              │     │ Deleted  │
              │     │ from DB  │
              ▼     └──────────┘
          ┌─DETACHED──┐
          │ Not in PC │
          │ Still in  │
          │ DB        │
          └────┬──────┘
          merge()
              │
              ▼
          PERSISTENT (re-attached)
```

**Persistence Context (PC):** A first-level cache that tracks entities. Managed by `EntityManager`. Flushed to DB on `commit()` or `flush()`.

**GSTN Example:**
```java
@Transactional
public void updateTask(int taskId, String newStatus) {
    WfTask task = entityManager.find(WfTask.class, taskId); // PERSISTENT
    task.setTaskStatus(newStatus);  // Dirty checking — NO explicit save needed!
    // On transaction commit, Hibernate auto-detects change and issues UPDATE
}
```

---

### Q78. Relationship mappings? LAZY vs EAGER?

**Answer:**

**GSTN Entity Relationships:**

```java
// @ManyToOne — Many WfTasks belong to one WfProcess
@Entity
@Table(name = "WF_TASK")
public class WfTask implements Serializable {
    @ManyToOne  // Default: EAGER for @ManyToOne
    @JoinColumn(name = "PROCESS_ID")
    private WfProcess wfProcess;
    
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "TASK_ID")
    private int taskId;
    
    @Column(name = "TASK_STATUS")
    private String taskStatus;
    
    @Temporal(TemporalType.DATE)
    @Column(name = "DUE_DT")
    private Date dueDt;
}

// @OneToMany — One WfProcess has many WfTasks
@Entity
@Table(name = "WF_PROCESS")
public class WfProcess implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "PROCESS_ID")
    private int processId;
    
    @OneToMany(mappedBy = "wfProcess", cascade = {CascadeType.ALL})  // Default: LAZY
    private Set<WfTask> wfTasks;
}
```

**Fetch Types:**

| Annotation | Default Fetch | Recommendation |
|------------|--------------|----------------|
| `@OneToOne` | **EAGER** | Change to LAZY |
| `@ManyToOne` | **EAGER** | Change to LAZY |
| `@OneToMany` | **LAZY** | Keep LAZY |
| `@ManyToMany` | **LAZY** | Keep LAZY |

```java
// Override default — ALWAYS use LAZY
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "PROCESS_ID")
private WfProcess wfProcess;
```

**Key rule:** Default to LAZY everywhere, then use JOIN FETCH or @EntityGraph when you need related data.

---

### Q79. What is the N+1 query problem? How do you solve it?

**Answer:**

**N+1 Problem:** 1 query to fetch parent entities + N queries to fetch each parent's children.

```java
// This generates N+1 queries:
List<WfProcess> processes = processRepository.findAll(); // 1 query: SELECT * FROM WF_PROCESS
for (WfProcess p : processes) {
    Set<WfTask> tasks = p.getWfTasks(); // N queries: SELECT * FROM WF_TASK WHERE PROCESS_ID = ?
    // Each access triggers a separate query!
}
```

**Solutions:**

```java
// 1. JOIN FETCH (JPQL)
@Query("SELECT p FROM WfProcess p JOIN FETCH p.wfTasks WHERE p.processId = :id")
WfProcess findByIdWithTasks(@Param("id") int id);
// Result: 1 query with JOIN

// 2. @EntityGraph
@EntityGraph(attributePaths = {"wfTasks"})
List<WfProcess> findAll();
// Result: 1 query with LEFT JOIN

// 3. @BatchSize (Hibernate-specific)
@OneToMany(mappedBy = "wfProcess")
@BatchSize(size = 20)  // Fetch 20 parent's children in one query
private Set<WfTask> wfTasks;
// Result: 1 + ceil(N/20) queries instead of 1 + N

// 4. Subselect fetch
@OneToMany(mappedBy = "wfProcess")
@Fetch(FetchMode.SUBSELECT)
private Set<WfTask> wfTasks;
// Result: 2 queries total (1 for parents, 1 subselect for all children)
```

**GSTN Context:** With large datasets (millions of records), N+1 can be devastating. Our approach: LAZY loading by default + JOIN FETCH in specific queries where we know we need related data.

---

### Q80. First-level cache vs Second-level cache?

**Answer:**

| Feature | First-Level (L1) | Second-Level (L2) |
|---------|------------------|-------------------|
| Scope | **Per EntityManager/Session** | **Per SessionFactory** (shared across sessions) |
| Enabled | **Always** (can't disable) | **Opt-in** (must configure) |
| Lifetime | Transaction/session lifetime | Application lifetime |
| Shared | No — each thread has its own | Yes — all threads share |
| Implementation | Built into Hibernate | EhCache, Infinispan, Redis |

```java
// L1 cache example — same session, same object
@Transactional
public void demo() {
    WfTask task1 = em.find(WfTask.class, 1); // DB query
    WfTask task2 = em.find(WfTask.class, 1); // NO query — returns cached object
    assert task1 == task2; // Same Java object! (identity guarantee)
}

// L2 cache configuration
@Entity
@Cacheable
@org.hibernate.annotations.Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class StateMaster {
    // Rarely changing reference data — perfect for L2 cache
}
```

**GSTN Caching:** We use `DistCacheUtil` (Redis-based distributed cache) and `LocalCacheFwk` (in-memory local cache) for caching reference data. This is application-level caching, separate from Hibernate's L2 cache.

```java
// GSTN's approach — application-level caching with DistCacheUtil
public GSTMaster getGstMstrDetails(String uid) {
    // Check distributed cache (Redis) first
    // If miss, query DB and cache result
}

// Local cache for reference data
public static Map getRefDetails(String type) {
    Map cacheMap = getMasterCache().getFromCache(type);
    if (cacheMap == null) {
        loadCacheMap = loadToCache(CacheConstants.MASTER_CACHE, type);
    }
    return cacheMap;
}
```

---

### Q81. HQL vs JPQL vs Native SQL vs Criteria API?

**Answer:**

| Query Type | Standard | Entity/Table | Type-safe | Use Case |
|-----------|----------|-------------|-----------|----------|
| **JPQL** | JPA standard | Entity names | No | Most queries (portable) |
| **HQL** | Hibernate-specific | Entity names | No | Hibernate-specific features |
| **Native SQL** | Database-specific | Table names | No | Complex queries, DB-specific functions |
| **Criteria API** | JPA standard | Programmatic | **Yes** | Dynamic queries (variable filters) |

**GSTN Examples:**
```java
// JPQL via @Query (from GspAuthToknLogRepository)
@Query("UPDATE GspAuthTokenLog e SET e.authStatus = 'X' " +
       "WHERE e.userName = :username AND e.clientId = :clientId")
void markAuthTokenExpired(@Param("username") String username, 
                         @Param("clientId") String clientId);

// Native SQL (for complex queries)
@Query(value = "SELECT * FROM GSP_AUTH_TOKEN_LOG WHERE AUTH_STATUS = 'A' " +
               "AND CREATED_DT < DATE_SUB(NOW(), INTERVAL 24 HOUR)", 
       nativeQuery = true)
List<GspAuthTokenLog> findExpiredTokens();

// Criteria API (for dynamic search filters)
CriteriaBuilder cb = em.getCriteriaBuilder();
CriteriaQuery<WfTask> query = cb.createQuery(WfTask.class);
Root<WfTask> root = query.from(WfTask.class);
List<Predicate> predicates = new ArrayList<>();
if (status != null) predicates.add(cb.equal(root.get("taskStatus"), status));
if (dueDate != null) predicates.add(cb.lessThan(root.get("dueDt"), dueDate));
query.where(predicates.toArray(new Predicate[0]));
```

---

### Q82. Optimistic locking vs Pessimistic locking?

**Answer:**

| Aspect | Optimistic (@Version) | Pessimistic (@Lock) |
|--------|----------------------|---------------------|
| Mechanism | Version check at commit time | Database lock on SELECT |
| Conflicts | Detected at update time | Prevented upfront |
| Performance | **Better** — no locks held | Worse — locks block other transactions |
| Concurrency | High — no blocking | Low — blocking |
| Failure mode | `OptimisticLockException` | Deadlocks possible |
| Best for | Read-heavy, low contention | Write-heavy, high contention |

```java
// OPTIMISTIC LOCKING — version-based
@Entity
public class ReturnEntity {
    @Id
    private Long id;
    
    @Version  // Hibernate auto-increments on update
    private Integer version;
    
    private String status;
}
// UPDATE RETURN SET status=?, version=2 WHERE id=? AND version=1
// If version changed → OptimisticLockException → retry

// PESSIMISTIC LOCKING — database lock
@Query("SELECT r FROM ReturnEntity r WHERE r.gstin = :gstin")
@Lock(LockModeType.PESSIMISTIC_WRITE) // SELECT ... FOR UPDATE
ReturnEntity findByGstinForUpdate(@Param("gstin") String gstin);
```

**GSTN Use Cases:**
- **Optimistic**: Return filing — multiple users rarely update same return simultaneously
- **Pessimistic**: Ledger balance updates — prevent concurrent deductions from same balance
```java
@Transactional(value = "transactionManagerItcLedger", 
              propagation = Propagation.REQUIRES_NEW)
public void updateLedgerBalance(LedgerVO ledger) {
    // Use pessimistic lock on ledger row to prevent race conditions
}
```

---

### Q83. Database migration — Flyway vs Liquibase?

**Answer:**

| Feature | Flyway | Liquibase |
|---------|--------|-----------|
| Format | **SQL files** (V1__create.sql) | XML/YAML/JSON/SQL |
| Naming | Version-based (V1, V2...) | Changeset-based |
| Rollback | Manual (undo migrations) | Auto-rollback support |
| Simplicity | **Simpler** | More features |
| Schema diff | No | Yes (diff between envs) |

```sql
-- Flyway: V1__create_return_table.sql
CREATE TABLE GST_RETURN (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    gstin VARCHAR(15) NOT NULL,
    return_period VARCHAR(6) NOT NULL,
    status VARCHAR(20),
    filed_date DATETIME,
    version INT DEFAULT 0
);

-- V2__add_index.sql  
CREATE INDEX idx_gstin_period ON GST_RETURN(gstin, return_period);
```

**GSTN:** Database schema changes are managed through controlled migration scripts deployed across environments (dev → QA → staging → prod).

---

### Q84. Bulk inserts efficiently?

**Answer:**

```java
// BAD — N separate INSERT statements
for (ReturnItem item : items) {
    repository.save(item); // Each save = 1 INSERT
}

// GOOD — Batch inserts with batch_size
// application.properties
spring.jpa.properties.hibernate.jdbc.batch_size=50
spring.jpa.properties.hibernate.order_inserts=true
spring.jpa.properties.hibernate.order_updates=true

// Repository usage
repository.saveAll(items); // Groups into batches of 50

// BEST — StatelessSession for massive bulk operations
StatelessSession session = sessionFactory.openStatelessSession();
Transaction tx = session.beginTransaction();
for (int i = 0; i < items.size(); i++) {
    session.insert(items.get(i));
    if (i % 1000 == 0) {
        // StatelessSession doesn't cache — no need to flush
    }
}
tx.commit();
session.close();
```

**GSTN:** During filing season, bulk operations (processing millions of return items) use batch processing with `GstBatchJobConfigurer` from the Spring Boot starter.

---

### Q85. Dirty Checking mechanism?

**Answer:**

When an entity is **persistent** (managed by EntityManager), Hibernate keeps a **snapshot** of its original state. At flush time, it compares the current state with the snapshot → if different, generates UPDATE SQL.

```java
@Transactional
public void updateTaskStatus(int taskId, String newStatus) {
    WfTask task = em.find(WfTask.class, taskId); // Loads + takes snapshot
    task.setTaskStatus(newStatus);  // Modifies in-memory object
    // NO explicit save/update needed!
    // At transaction commit → Hibernate compares current vs snapshot
    // Detects change → generates: UPDATE WF_TASK SET TASK_STATUS=? WHERE TASK_ID=?
}
```

**Performance concern:** For read-only queries, dirty checking wastes CPU. Use `@Transactional(readOnly = true)` to disable it.

---

### Q86. Projection queries — fetch specific columns?

**Answer:**

```java
// Interface-based projection
public interface GstinProjection {
    String getGstin();
    String getLegalName();
}

@Query("SELECT r.gstin as gstin, r.legalName as legalName FROM Registration r WHERE r.stateCode = :state")
List<GstinProjection> findGstinsByState(@Param("state") String state);

// DTO-based projection (constructor expression)
@Query("SELECT new org.gst.dto.GstinDTO(r.gstin, r.legalName) FROM Registration r")
List<GstinDTO> findGstinDTOs();

// Tuple projection
@Query("SELECT r.gstin, r.legalName FROM Registration r")
List<Object[]> findGstinTuples();
```

**Why:** Fetching only needed columns reduces memory usage and network transfer — crucial for GSTN's large tables.

---

### Q87. @Embeddable and @Embedded? Composite keys?

**Answer:**

**GSTN's composite key pattern:**
```java
// Composite key class
@Embeddable
@EqualsAndHashCode  // MUST implement equals/hashCode for composite keys
public class ApplnPK implements Serializable {
    @ManyToOne
    @JoinColumn(name = "APPLN_DETL_ID")
    private ApplnDraftDetlEntity applnDrftDetl;
    
    @Column(name = "VER_ID")
    private Integer versionId;
}

// Entity using composite key
@Entity
@Table(name = "APPLN_VER_DTLS")
public class ApplnVersionDetails implements Serializable {
    @EmbeddedId
    private ApplnPK id;  // Composite primary key
    
    @Column(name = "COMMENTS")
    private String comments;
}
```

**@Embedded for value objects:**
```java
@Embeddable
public class Address {
    private String street;
    private String city;
    private String stateCode;
    private String pinCode;
}

@Entity
public class Registration {
    @Id
    private Long id;
    
    @Embedded
    @AttributeOverrides({
        @AttributeOverride(name = "street", column = @Column(name = "BIZ_STREET")),
        @AttributeOverride(name = "city", column = @Column(name = "BIZ_CITY"))
    })
    private Address businessAddress;
    
    @Embedded
    @AttributeOverrides({
        @AttributeOverride(name = "street", column = @Column(name = "CORR_STREET")),
        @AttributeOverride(name = "city", column = @Column(name = "CORR_CITY"))
    })
    private Address correspondenceAddress;
}
```

---

### Q88. Spring Data JPA — derived queries, @Query, @Modifying, custom repositories?

**Answer:**

```java
// DERIVED QUERY METHODS — auto-generated from method name
@Repository
public interface GspActiveAuthSessionRepository extends JpaRepository<GspActiveAuthSession, Long> {
    
    List<GspActiveAuthSession> findByUserNameAndClientId(String userName, String clientId);
    List<GspActiveAuthSession> findByAuthStatus(String status);
    Optional<GspActiveAuthSession> findByAuthTokenAndUserName(String token, String userName);
    
    // More complex derived methods
    List<GspActiveAuthSession> findByAuthStatusAndCreatedDateAfter(String status, Date date);
    long countByAuthStatus(String status);
    void deleteByAuthTokenAndUserName(String token, String userName);
}

// @Query — custom JPQL
@Query("UPDATE GspAuthTokenLog e SET e.authStatus = 'X' " +
       "WHERE e.userName = :username AND e.clientId = :clientId AND e.authToken = :authToken")
@Modifying  // Required for UPDATE/DELETE queries
void markAuthTokenExpired(@Param("username") String username,
                         @Param("clientId") String clientId,
                         @Param("authToken") String authToken);

// Custom repository implementation
public interface CustomReturnRepository {
    List<ReturnEntity> searchReturns(SearchCriteria criteria);
}

public class CustomReturnRepositoryImpl implements CustomReturnRepository {
    @PersistenceContext
    private EntityManager em;
    
    @Override
    public List<ReturnEntity> searchReturns(SearchCriteria criteria) {
        CriteriaBuilder cb = em.getCriteriaBuilder();
        // Dynamic query building...
    }
}

// Combine Spring Data + custom
public interface ReturnRepository extends JpaRepository<ReturnEntity, Long>, 
                                         CustomReturnRepository {
    // Has both auto-generated AND custom methods
}
```

---

### Q89. Entity auditing?

**Answer:**

```java
@Configuration
@EnableJpaAuditing
public class AuditConfig {
    @Bean
    public AuditorAware<String> auditorProvider() {
        return () -> Optional.of(SecurityContextHolder.getContext()
            .getAuthentication().getName());
    }
}

@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseEntity {
    @CreatedDate
    @Column(name = "INSERT_TMSTMP", updatable = false)
    private Date createdDate;
    
    @LastModifiedDate
    @Column(name = "UPDATE_TMSTMP")
    private Date updatedDate;
    
    @CreatedBy
    @Column(name = "CREATED_BY", updatable = false)
    private String createdBy;
    
    @LastModifiedBy
    @Column(name = "MODIFIED_BY")
    private String modifiedBy;
}
```

**GSTN Pattern:** Our entities use `@Temporal(TemporalType.TIMESTAMP)` for audit timestamps:
```java
@Temporal(TemporalType.TIMESTAMP)
@Column(name = "INSERT_TMSTMP")
private Date insertTmstmp;

@Temporal(TemporalType.TIMESTAMP)
@Column(name = "UPDATE_TMSTMP")
private Date updateTmstmp;
```

---

### Q90. save() vs saveAndFlush() vs persist()?

**Answer:**

| Method | Source | Returns | When SQL fires | Detached entity? |
|--------|--------|---------|---------------|------------------|
| `save()` | Spring Data | Saved entity | At flush/commit | Calls `merge()` |
| `saveAndFlush()` | Spring Data | Saved entity | **Immediately** | Calls `merge()` |
| `persist()` | JPA EntityManager | void | At flush/commit | **Exception** if detached |

```java
// save() — defers SQL execution
ReturnEntity entity = new ReturnEntity();
entity.setGstin("29AAACG1234A1ZD");
repository.save(entity);  // INSERT may not fire yet
// SQL fires at transaction commit or explicit flush

// saveAndFlush() — immediate SQL execution
repository.saveAndFlush(entity);  // INSERT fires NOW
// Useful when you need the generated ID immediately

// persist() — JPA standard
entityManager.persist(entity);  // Schedules INSERT
// Throws PersistenceException if entity is detached
```

**GSTN Usage:**
```java
// From UserMasterServiceImpl
@Transactional(value = "transactionManagerReturns", 
              propagation = Propagation.REQUIRED, rollbackFor = Exception.class)
public UserMaster updateUser(UserMaster user) {
    return userMasterRepository.saveAndFlush(user);  // Immediate flush for consistency
}
```
