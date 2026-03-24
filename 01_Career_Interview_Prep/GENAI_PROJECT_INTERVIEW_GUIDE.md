# GENAI PROJECT GUIDE: OFFICE + INTERVIEW READY

## Dual Purpose Strategy

Every project you build should answer TWO questions:
1. **Office:** "Can I demo this to my manager?"
2. **Interview:** "Can I explain the architecture, trade-offs, and challenges?"

---

## GENAI INTERVIEW REALITY CHECK

### What Companies Actually Ask

Based on 2025 GenAI/ML interview patterns:

| Topic | Question Type | Depth Expected |
|-------|--------------|----------------|
| RAG | Architecture, chunking strategies, retrieval quality | Deep |
| Agents | When to use, orchestration, tool calling | Medium-Deep |
| Vector DB | Embedding choice, indexing, similarity metrics | Medium |
| Hallucination | Detection, mitigation, guardrails | Deep |
| LLM Integration | API design, prompt engineering, cost optimization | Deep |
| AWS Bedrock | Model selection, pricing, vs OpenAI/Azure | Medium |
| MCP | Protocol understanding, use cases | Emerging |

### Interview Questions You MUST Answer

```
RAG:
- "How do you handle chunking for different document types?"
- "What's your retrieval strategy? Why not just use keyword search?"
- "How do you evaluate RAG quality?"
- "What happens when context window is exceeded?"

Agents:
- "When would you use agents vs simple RAG?"
- "How do you handle agent failures/loops?"
- "Explain ReAct pattern"
- "How do you test agents?"

Hallucination:
- "How do you detect hallucinations?"
- "What guardrails do you implement?"
- "How do you handle factual grounding?"

Vector DB:
- "Why Pinecone vs Chroma vs FAISS?"
- "How do you choose embedding dimensions?"
- "What's the indexing strategy for 1M+ documents?"

AWS Bedrock:
- "Why Bedrock vs direct OpenAI?"
- "How do you handle model versioning?"
- "Cost optimization strategies?"
```

---

## PROJECT 1: DOCUMENT Q&A WITH RAG (Week 1-2)

### What You'll Build
A document question-answering system using RAG architecture.

### Office Deliverable
"Internal knowledge base chatbot for company documents"

### Interview Talking Points
- Chunking strategy decisions
- Embedding model selection
- Retrieval optimization
- Hallucination handling

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER QUERY                               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  FASTAPI BACKEND                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Query     │  │  Embedding  │  │    Retrieval        │  │
│  │   Router    │──│  Generator  │──│    (Top-K)          │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│  Vector DB   │ │  AWS     │ │  Document    │
│  (Pinecone/  │ │  Bedrock │ │  Store (S3)  │
│   Chroma)    │ │  Claude  │ │              │
└──────────────┘ └──────────┘ └──────────────┘
```

### Tech Stack
```
Backend:      Python + FastAPI
Embedding:    AWS Bedrock Titan / OpenAI Ada-002
Vector DB:    Pinecone (prod) / Chroma (local dev)
LLM:          AWS Bedrock Claude 3
Storage:      AWS S3
Deployment:   AWS Lambda + API Gateway
```

### Implementation Phases

**Phase 1: Document Processing Pipeline (Days 1-3)**
```python
# Key decisions to explain in interview:

# 1. Chunking Strategy
"""
Interview Q: "How did you decide chunk size?"

Your Answer:
"I tested 256, 512, and 1024 token chunks.
- 256: Too fragmented, lost context
- 1024: Often exceeded context window with multiple retrievals
- 512: Sweet spot for our document types

For tables/code, I used semantic chunking instead of fixed size,
keeping logical units together."
"""

# 2. Overlap Strategy
"""
Interview Q: "Why use overlapping chunks?"

Your Answer:
"50-token overlap prevents information loss at boundaries.
Without overlap, a sentence split across chunks loses meaning.
Trade-off: 10% more storage, but significantly better retrieval."
"""

# Code structure
from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]  # Priority order
    )
    return splitter.split_documents(documents)
```

**Phase 2: Embedding & Vector Storage (Days 4-5)**
```python
# Key decisions:

# 1. Embedding Model Choice
"""
Interview Q: "Why Titan embeddings vs OpenAI?"

Your Answer:
"For this project, I used Titan because:
- Already in AWS ecosystem (Bedrock)
- Lower latency (same region)
- Cost: ~$0.0001/1K tokens vs OpenAI's $0.0004
- Compliance: Data stays in AWS

Trade-off: OpenAI's ada-002 has slightly better benchmark scores,
but for internal documents, Titan's quality was sufficient."
"""

# 2. Vector DB Choice
"""
Interview Q: "Why Pinecone vs FAISS vs Chroma?"

Your Answer:
"Decision matrix:
- FAISS: Free, but no persistence, single-node
- Chroma: Good for dev, not production-ready at scale
- Pinecone: Managed, scales automatically, built-in filtering

For POC: Chroma locally
For production: Pinecone

Key factor: We needed metadata filtering (by department, date)
which Pinecone handles natively."
"""

import boto3
from pinecone import Pinecone

# Bedrock embedding
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def get_embedding(text):
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v1',
        body=json.dumps({"inputText": text})
    )
    return json.loads(response['body'].read())['embedding']
```

**Phase 3: Retrieval & Generation (Days 6-8)**
```python
# Key decisions:

# 1. Retrieval Strategy
"""
Interview Q: "How do you ensure relevant retrieval?"

Your Answer:
"Multi-stage retrieval:
1. Vector similarity: Top 20 candidates
2. Reranking: Cross-encoder to get Top 5
3. Diversity: MMR to avoid redundant chunks

Why reranking? Vector similarity is fast but imprecise.
Cross-encoder is slow but accurate. Combine both."
"""

# 2. Context Window Management
"""
Interview Q: "What if retrieved context exceeds token limit?"

Your Answer:
"I implemented a context budget system:
- Reserve 1000 tokens for response
- Reserve 500 for system prompt
- Remaining budget for context (dynamic based on model)
- If over budget, use relevance score to drop lowest chunks
- Always include at least top 2 chunks"
"""

# 3. Hallucination Prevention
"""
Interview Q: "How do you prevent hallucinations?"

Your Answer:
"Three layers:
1. Prompt engineering: 'Only answer based on provided context.
   If information not in context, say I don't know.'
2. Citation requirement: Model must cite which chunk
3. Post-processing: Check if answer entities exist in context

Still not perfect - added disclaimer for low-confidence answers."
"""

from fastapi import FastAPI

app = FastAPI()

SYSTEM_PROMPT = """You are a helpful assistant that answers questions 
based ONLY on the provided context. 

Rules:
1. If the answer is not in the context, say "I don't have information about this."
2. Always cite which part of the context supports your answer.
3. Never make up information.

Context:
{context}
"""

@app.post("/query")
async def query(question: str):
    # 1. Get embedding
    query_embedding = get_embedding(question)
    
    # 2. Retrieve from vector DB
    results = vector_db.query(query_embedding, top_k=5)
    
    # 3. Build context
    context = "\n\n".join([r.text for r in results])
    
    # 4. Generate with Bedrock
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps({
            "messages": [
                {"role": "user", "content": f"{SYSTEM_PROMPT.format(context=context)}\n\nQuestion: {question}"}
            ],
            "max_tokens": 1000
        })
    )
    
    return {"answer": response, "sources": results}
```

**Phase 4: Evaluation & Monitoring (Days 9-10)**
```python
# Interview Q: "How do you evaluate RAG quality?"

"""
Your Answer:
"Three metrics:
1. Retrieval Quality (can measure without LLM)
   - Hit rate: Is correct chunk in top-K?
   - MRR: Mean Reciprocal Rank
   
2. Answer Quality (needs human eval or LLM judge)
   - Faithfulness: Is answer supported by context?
   - Relevance: Does answer address question?
   
3. System Metrics
   - Latency: P50, P95, P99
   - Cost per query
   - Token usage

I built a eval dataset of 50 question-answer pairs from actual
documents and ran weekly regression tests."
"""
```

### Interview Story (STAR Format)

```
Situation: "Our team needed to build a GenAI POC for internal 
document search - employees were spending hours finding information 
in scattered documents."

Task: "I was responsible for designing and implementing the RAG 
architecture end-to-end."

Action: 
"I made several key technical decisions:
1. Chose 512-token chunks with 50-token overlap after testing 
   showed 23% better retrieval accuracy than fixed 1024 chunks
2. Implemented hybrid retrieval: vector similarity + BM25 keyword 
   search, improving recall by 15%
3. Built hallucination guardrails - the model cites sources and 
   admits uncertainty
4. Deployed on AWS Lambda for cost efficiency - pay per request"

Result: 
"POC handled 500+ queries in demo week with 87% user satisfaction.
Reduced average document search time from 15 min to 30 seconds.
Cost: ~$0.02 per query including embeddings and generation."
```

---

## PROJECT 2: MULTI-TOOL AGENT (Week 2-3)

### What You'll Build
An agent that can use multiple tools (search, calculator, API calls) to answer complex queries.

### Office Deliverable
"Intelligent assistant that can query databases, search docs, and perform calculations"

### Interview Talking Points
- Agent architecture (ReAct, tool calling)
- Error handling and recovery
- When agents vs simple chains
- Testing strategies

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER QUERY                               │
│         "What was our Q3 revenue growth vs Q2?"             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT ORCHESTRATOR                        │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  1. Parse query                                      │   │
│   │  2. Decide: Which tools needed?                      │   │
│   │  3. Execute tools in order                           │   │
│   │  4. Synthesize results                               │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┬─────────────┐
        ▼             ▼             ▼             ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│   RAG Tool   │ │ Database │ │Calculator│ │  Search  │
│  (from P1)   │ │  Query   │ │   Tool   │ │   Tool   │
└──────────────┘ └──────────┘ └──────────┘ └──────────┘
```

### Key Interview Concepts

**1. ReAct Pattern**
```
Interview Q: "Explain ReAct pattern"

Your Answer:
"ReAct = Reasoning + Acting

Traditional: Query → Answer (one shot)
ReAct: Query → Think → Act → Observe → Think → Act → ... → Answer

Example:
Query: 'What was revenue growth Q3 vs Q2?'

Think: I need Q3 revenue and Q2 revenue to calculate growth
Act: Call database_query('SELECT revenue FROM quarterly WHERE quarter IN (Q2, Q3)')
Observe: Q2=100M, Q3=120M
Think: Now I can calculate growth: (120-100)/100 = 20%
Act: Return answer
Answer: 'Revenue grew 20% from Q2 to Q3'

Key benefit: Explainable reasoning, can recover from errors"
```

**2. Tool Calling**
```python
# Interview Q: "How do you implement tool calling?"

"""
Your Answer:
"Two approaches:

1. Function Calling (OpenAI/Claude style):
   - Define tools as JSON schema
   - Model outputs structured tool calls
   - Parse and execute
   
2. ReAct with text parsing:
   - Model outputs reasoning + action in text
   - Parse action from text
   - Execute and feed back observation

I used AWS Bedrock Claude which supports native tool_use.
More reliable than text parsing."
"""

# Tool definition
tools = [
    {
        "name": "database_query",
        "description": "Query the company database for financial metrics",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "SQL query to execute"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "document_search",
        "description": "Search internal documents for information",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculator",
        "description": "Perform mathematical calculations",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            },
            "required": ["expression"]
        }
    }
]

# Agent execution
def run_agent(user_query: str, max_iterations: int = 5):
    messages = [{"role": "user", "content": user_query}]
    
    for i in range(max_iterations):
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet',
            body=json.dumps({
                "messages": messages,
                "tools": tools,
                "max_tokens": 1000
            })
        )
        
        # Check if model wants to use a tool
        if response.stop_reason == "tool_use":
            tool_call = response.content[-1]  # Get tool call
            tool_result = execute_tool(tool_call.name, tool_call.input)
            
            # Add tool result to conversation
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": str(tool_result)
                }]
            })
        else:
            # Model is done, return final answer
            return response.content[0].text
    
    return "Max iterations reached"
```

**3. Error Handling**
```python
# Interview Q: "How do you handle agent failures?"

"""
Your Answer:
"Three failure modes and mitigations:

1. Tool execution failure (DB down, API error)
   - Retry with exponential backoff
   - If persistent, inform user gracefully
   - Log for debugging

2. Agent loops (keeps calling same tool)
   - Track tool call history
   - Detect repeated calls with same params
   - Force termination after N iterations
   - Return partial result with explanation

3. Hallucinated tool calls (tool doesn't exist)
   - Strict tool schema validation
   - If invalid tool, return error to model
   - Model learns from feedback
"
"""

def execute_tool(tool_name: str, tool_input: dict):
    try:
        if tool_name == "database_query":
            # Validate query (prevent SQL injection)
            if not is_safe_query(tool_input["query"]):
                return {"error": "Query not allowed for security reasons"}
            return db.execute(tool_input["query"])
            
        elif tool_name == "document_search":
            return rag_search(tool_input["query"])
            
        elif tool_name == "calculator":
            # Safe eval
            return eval_math_expression(tool_input["expression"])
            
        else:
            return {"error": f"Unknown tool: {tool_name}"}
            
    except Exception as e:
        return {"error": str(e)}
```

**4. When to Use Agents vs Simple Chains**
```
Interview Q: "When would you NOT use an agent?"

Your Answer:
"Agents add complexity. Don't use when:

1. Single-step tasks
   - 'Summarize this document' → Just call LLM
   
2. Predictable workflow
   - 'Extract invoice fields' → Structured extraction
   
3. Latency-critical
   - Agents = multiple LLM calls = slow
   
4. High-reliability required
   - Agents can fail unpredictably
   - For critical paths, use deterministic code

Use agents when:
- User query is ambiguous
- Multiple tools might be needed
- Reasoning required between steps
- Exploratory tasks"
```

---

## PROJECT 3: MCP SERVER IMPLEMENTATION (Week 3-4)

### What You'll Build
A Model Context Protocol server that exposes your tools to any MCP-compatible client.

### Office Deliverable
"Standardized protocol for connecting LLMs to internal systems"

### Interview Talking Points
- Protocol design
- Tool standardization
- Integration patterns

### What is MCP?

```
Interview Q: "Explain MCP in simple terms"

Your Answer:
"MCP (Model Context Protocol) is like USB for AI.

Before USB: Every device had different connector
After USB: Standard connector, any device works

Before MCP: Every LLM integration is custom code
After MCP: Standard protocol, any LLM can use any tool

Components:
1. MCP Server: Exposes tools (your APIs, databases, etc.)
2. MCP Client: LLM application that calls tools
3. Protocol: JSON-RPC over stdio/HTTP

Why it matters:
- Build tool once, use with Claude, GPT, any LLM
- Standardized error handling
- Built-in capability discovery"
```

### MCP Server Implementation

```python
# Interview Q: "How would you implement an MCP server?"

"""
Your Answer:
"MCP uses JSON-RPC 2.0 over stdio or HTTP.

Key endpoints:
1. initialize - Handshake, capability exchange
2. tools/list - Return available tools
3. tools/call - Execute a tool

I implemented a server exposing our internal APIs:
- Database query tool
- Document search tool  
- Notification sender tool"
"""

# Basic MCP Server structure
from mcp import Server, Tool

server = Server("internal-tools")

@server.tool("query_database")
async def query_database(query: str) -> str:
    """
    Execute a read-only SQL query against company database.
    
    Args:
        query: SQL SELECT query
    
    Returns:
        Query results as JSON
    """
    # Validate read-only
    if not query.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries allowed")
    
    result = await db.execute(query)
    return json.dumps(result)

@server.tool("search_documents")
async def search_documents(query: str, department: str = None) -> str:
    """
    Search internal documents using RAG.
    
    Args:
        query: Search query
        department: Optional department filter
    
    Returns:
        Relevant document excerpts
    """
    results = await rag_search(query, filters={"department": department})
    return json.dumps(results)

@server.tool("send_notification")
async def send_notification(user_id: str, message: str, channel: str = "email") -> str:
    """
    Send notification to a user.
    
    Args:
        user_id: Target user ID
        message: Notification content
        channel: 'email' or 'slack'
    
    Returns:
        Confirmation status
    """
    result = await notification_service.send(user_id, message, channel)
    return json.dumps({"status": "sent", "id": result.id})

# Run server
if __name__ == "__main__":
    server.run()
```

### MCP Integration with ADK

```python
# Interview Q: "How does MCP work with ADK (Agent Development Kit)?"

"""
Your Answer:
"ADK is Google's agent framework. It can consume MCP servers.

Flow:
1. ADK agent starts
2. Discovers MCP servers (configured)
3. Calls tools/list to get available tools
4. When agent needs a tool, calls tools/call
5. MCP server executes and returns result

Benefit: I can expose the same MCP server to ADK agents,
Claude Desktop, custom applications - any MCP client."
"""

# ADK Agent using MCP
from google.adk import Agent
from google.adk.tools import MCPToolProvider

# Connect to MCP server
mcp_tools = MCPToolProvider("./internal-tools-server")

# Create agent with MCP tools
agent = Agent(
    model="gemini-pro",
    tools=[mcp_tools],
    system_prompt="You are a helpful assistant with access to company tools."
)

# Agent can now use query_database, search_documents, send_notification
response = agent.run("What was our revenue last quarter?")
```

---

## PROJECT 4: HALLUCINATION DETECTION SYSTEM (Week 4)

### What You'll Build
A system to detect and flag potential hallucinations in LLM outputs.

### Office Deliverable
"Quality assurance layer for GenAI outputs"

### Interview Talking Points
- Hallucination types
- Detection strategies
- Mitigation approaches

### Types of Hallucinations

```
Interview Q: "What types of hallucinations exist?"

Your Answer:
"Three main types:

1. Factual Hallucination
   - Made-up facts, statistics, dates
   - 'Company founded in 1985' (actually 1990)
   
2. Faithfulness Hallucination
   - Answer contradicts provided context
   - Context says 'revenue up', answer says 'revenue down'
   
3. Instruction Hallucination
   - Ignores user constraints
   - Asked for 3 points, gives 5

Each needs different detection approach."
```

### Detection Implementation

```python
# Interview Q: "How do you detect hallucinations?"

"""
Your Answer:
"Multi-layer detection:

1. Entity Verification
   - Extract named entities from response
   - Check if entities exist in context/knowledge base
   
2. Claim Verification
   - Extract factual claims
   - Cross-reference with source documents
   
3. Self-Consistency Check
   - Generate multiple responses
   - Flag inconsistencies
   
4. Confidence Scoring
   - Model's own uncertainty
   - Low confidence = potential hallucination"
"""

import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

class HallucinationDetector:
    
    def __init__(self, bedrock_client):
        self.bedrock = bedrock_client
    
    def detect(self, question: str, context: str, answer: str) -> Dict:
        """
        Detect potential hallucinations in an answer.
        
        Returns:
            {
                "is_hallucination": bool,
                "confidence": float,
                "issues": List[str]
            }
        """
        issues = []
        
        # 1. Entity check
        entity_issues = self._check_entities(context, answer)
        issues.extend(entity_issues)
        
        # 2. Claim verification
        claim_issues = self._verify_claims(context, answer)
        issues.extend(claim_issues)
        
        # 3. Self-consistency (expensive, optional)
        # consistency_issues = self._check_consistency(question, context)
        # issues.extend(consistency_issues)
        
        return {
            "is_hallucination": len(issues) > 0,
            "confidence": 1 - (len(issues) / 10),  # Simple scoring
            "issues": issues
        }
    
    def _check_entities(self, context: str, answer: str) -> List[str]:
        """Check if entities in answer exist in context"""
        context_doc = nlp(context)
        answer_doc = nlp(answer)
        
        context_entities = set(ent.text.lower() for ent in context_doc.ents)
        answer_entities = set(ent.text.lower() for ent in answer_doc.ents)
        
        # Entities in answer but not in context
        hallucinated = answer_entities - context_entities
        
        issues = []
        for entity in hallucinated:
            # Filter out common entities that don't need grounding
            if not self._is_common_entity(entity):
                issues.append(f"Entity '{entity}' not found in context")
        
        return issues
    
    def _verify_claims(self, context: str, answer: str) -> List[str]:
        """Use LLM to verify claims against context"""
        
        verification_prompt = f"""
        Context: {context}
        
        Answer: {answer}
        
        Task: Identify any claims in the Answer that are NOT supported by the Context.
        
        Output format:
        - If all claims are supported: "VERIFIED"
        - If unsupported claims exist: List each unsupported claim
        
        Be strict. If the context doesn't explicitly state something, it's unsupported.
        """
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku',  # Cheaper for verification
            body=json.dumps({
                "messages": [{"role": "user", "content": verification_prompt}],
                "max_tokens": 500
            })
        )
        
        result = json.loads(response['body'].read())['content'][0]['text']
        
        if "VERIFIED" in result.upper():
            return []
        else:
            return [result]
    
    def _is_common_entity(self, entity: str) -> bool:
        """Check if entity is common knowledge (doesn't need context grounding)"""
        common = {"today", "yesterday", "january", "monday", "etc", "example"}
        return entity.lower() in common


# Usage in RAG pipeline
detector = HallucinationDetector(bedrock_client)

def query_with_hallucination_check(question: str):
    # Normal RAG
    context = retrieve_context(question)
    answer = generate_answer(question, context)
    
    # Check for hallucination
    check = detector.detect(question, context, answer)
    
    if check["is_hallucination"]:
        # Option 1: Regenerate with stricter prompt
        # Option 2: Add warning to user
        # Option 3: Fallback to "I don't know"
        return {
            "answer": answer,
            "warning": "This answer may contain unverified information",
            "issues": check["issues"]
        }
    
    return {"answer": answer, "confidence": check["confidence"]}
```

### Mitigation Strategies

```
Interview Q: "How do you prevent hallucinations?"

Your Answer:
"Prevention > Detection. Layers:

1. Prompt Engineering
   - 'Only use information from context'
   - 'If unsure, say I don't know'
   - 'Cite your sources'

2. Temperature Control
   - Lower temperature = less creative = fewer hallucinations
   - Trade-off: May be less engaging

3. Context Quality
   - Better retrieval = better grounding
   - More relevant chunks = fewer gaps to fill

4. Output Constraints
   - Structured output (JSON)
   - Required citation fields
   - Confidence score requirement

5. Human in the Loop
   - Flag low-confidence for review
   - Feedback loop to improve

No silver bullet - combine multiple approaches."
```

---

## INTERVIEW PREPARATION CHECKLIST

### RAG Questions You Must Answer

| Question | Your Answer Ready? |
|----------|-------------------|
| Explain your chunking strategy and why | ☐ |
| How do you handle documents with tables/images? | ☐ |
| Vector DB choice and trade-offs | ☐ |
| How do you evaluate retrieval quality? | ☐ |
| What's your re-ranking approach? | ☐ |
| How do you handle context window limits? | ☐ |
| Cost per query breakdown | ☐ |

### Agent Questions You Must Answer

| Question | Your Answer Ready? |
|----------|-------------------|
| Explain ReAct pattern | ☐ |
| When agents vs simple chains? | ☐ |
| How do you handle agent loops? | ☐ |
| Tool calling implementation | ☐ |
| Error handling and recovery | ☐ |
| How do you test agents? | ☐ |

### Hallucination Questions You Must Answer

| Question | Your Answer Ready? |
|----------|-------------------|
| Types of hallucinations | ☐ |
| Detection strategies | ☐ |
| Prevention approaches | ☐ |
| Trade-offs (hallucination vs helpfulness) | ☐ |
| How do you measure hallucination rate? | ☐ |

### AWS/Infrastructure Questions

| Question | Your Answer Ready? |
|----------|-------------------|
| Why Bedrock vs OpenAI direct? | ☐ |
| Model selection criteria | ☐ |
| Cost optimization strategies | ☐ |
| Lambda vs EC2 for inference | ☐ |
| How do you handle model versioning? | ☐ |

---

## WEEK-BY-WEEK PROJECT TIMELINE

```
WEEK 1 (Jan 20-26):
├── Day 1-3: RAG document processing pipeline
├── Day 4-5: Vector DB setup + embeddings
├── Day 6-7: Basic RAG working end-to-end
└── Deliverable: Document Q&A demo

WEEK 2 (Jan 27 - Feb 2):
├── Day 1-3: RAG improvements (reranking, evaluation)
├── Day 4-5: Agent architecture setup
├── Day 6-7: Tool calling implementation
└── Deliverable: Multi-tool agent demo

WEEK 3 (Feb 3-9):
├── Day 1-3: MCP server implementation
├── Day 4-5: MCP + ADK integration
├── Day 6-7: Testing and error handling
└── Deliverable: MCP server with 3+ tools

WEEK 4 (Feb 10-18):
├── Day 1-3: Hallucination detection system
├── Day 4-5: Integration with RAG pipeline
├── Day 6-7: Documentation + demo polish
└── Deliverable: Complete GenAI stack with quality layer
```

---

## FINAL INTERVIEW STORY TEMPLATE

```
"In my recent GenAI work, I built a document Q&A system using RAG architecture.

[TECHNICAL DEPTH]
The key challenges were:
1. Chunking strategy - I tested multiple approaches and found 512-token 
   chunks with 50-token overlap gave 23% better retrieval accuracy
2. Hallucination - I implemented a multi-layer detection system using 
   entity verification and claim checking
3. Cost optimization - By using Bedrock Titan for embeddings and 
   caching frequent queries, I reduced cost to $0.02/query

[SCALE/IMPACT]
The system handles 500+ queries daily with 87% user satisfaction.
Response latency P95 is under 3 seconds.

[TRADE-OFFS]
I chose Pinecone over FAISS because we needed metadata filtering.
Trade-off was cost ($70/month) vs operational simplicity.

[LEARNING]
Biggest learning: Retrieval quality matters more than generation.
A mediocre LLM with great retrieval beats a great LLM with poor retrieval."
```

---

## RESOURCES

### Documentation
- AWS Bedrock: https://docs.aws.amazon.com/bedrock/
- LangChain: https://python.langchain.com/
- Pinecone: https://docs.pinecone.io/
- MCP Specification: https://modelcontextprotocol.io/

### Code Repositories to Study
- LangChain RAG examples
- AWS Bedrock samples on GitHub
- Anthropic cookbook

### Papers (Optional, for depth)
- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- "ReAct: Synergizing Reasoning and Acting in Language Models"

---

*Build these projects, understand the decisions, and you'll handle any GenAI interview question.*
