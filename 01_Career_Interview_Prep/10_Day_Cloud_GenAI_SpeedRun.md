# 🚀 10-DAY CLOUD + GENAI SPEED RUN
## Zero to Interview-Ready for Project Allocation

---

## 🎯 THE GOAL

```
┌─────────────────────────────────────────────────────────────────┐
│  BY DAY 10, YOU SHOULD BE ABLE TO:                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ Explain a GenAI application architecture on whiteboard     │
│  ✅ Discuss RAG, Agents, MCP confidently                       │
│  ✅ Deploy a GenAI app on AWS                                  │
│  ✅ Answer 20 common Cloud + GenAI interview questions         │
│  ✅ Have 2 working projects to show                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 THE MENTAL MODEL: How Cloud + GenAI Connect

```
┌─────────────────────────────────────────────────────────────────────┐
│                 MODERN GENAI APPLICATION STACK                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [User] ──► [Frontend]                                             │
│                  │                                                  │
│                  ▼                                                  │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │              API LAYER (Your Backend)                        │  │
│   │   AWS: API Gateway + Lambda / ECS                           │  │
│   │   Azure: API Management + Functions / AKS                   │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                  │                                                  │
│        ┌─────────┴─────────┬─────────────────┐                     │
│        ▼                   ▼                 ▼                      │
│   ┌─────────┐       ┌───────────┐     ┌───────────┐                │
│   │  LLM    │       │  VECTOR   │     │  MEMORY   │                │
│   │ SERVICE │       │    DB     │     │   STORE   │                │
│   └─────────┘       └───────────┘     └───────────┘                │
│   Bedrock/OpenAI    Pinecone/         Redis/                       │
│   Azure OpenAI      Weaviate/         DynamoDB                     │
│                     pgvector                                        │
│        │                   │                 │                      │
│        └─────────┬─────────┴─────────────────┘                     │
│                  ▼                                                  │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │              AGENT / ORCHESTRATION LAYER                     │  │
│   │   LangChain / LlamaIndex / ADK                              │  │
│   │   MCP Servers for Tools                                      │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                  │                                                  │
│                  ▼                                                  │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │              TOOLS & INTEGRATIONS                            │  │
│   │   Databases, APIs, File Systems, Search Engines             │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📅 THE 10-DAY BATTLE PLAN

### ═══════════════════════════════════════════════════════════
### PHASE 1: GENAI FOUNDATIONS (Day 1-3)
### ═══════════════════════════════════════════════════════════

## DAY 1: LLM Fundamentals + First API Call

### Morning (2 hrs): Concepts

**Watch (30 min):**
- "How LLMs Work" - 3Blue1Brown or Andrej Karpathy (just first 20 min)

**Understand these terms (write definitions in YOUR words):**

```
┌─────────────────────────────────────────────────────────────────┐
│  GENAI VOCABULARY (Memorize This!)                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TOKEN        = Smallest unit LLM processes (~4 chars)         │
│  PROMPT       = Input you give to LLM                          │
│  COMPLETION   = Output LLM generates                           │
│  CONTEXT      = Information available to LLM in one request    │
│  TEMPERATURE  = Randomness (0=deterministic, 1=creative)       │
│  TOP-P        = Diversity of word selection                    │
│  MAX_TOKENS   = Limit on output length                         │
│  SYSTEM PROMPT= Instructions that define LLM behavior          │
│  FEW-SHOT     = Examples in prompt to guide output             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Afternoon (3 hrs): Hands-On - Your First LLM API Call

```python
# DO THIS: Create llm_basics.py

# Option 1: OpenAI
from openai import OpenAI

client = OpenAI(api_key="your-key")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain RAG in 3 sentences."}
    ],
    temperature=0.7,
    max_tokens=200
)

print(response.choices[0].message.content)


# Option 2: Anthropic Claude
from anthropic import Anthropic

client = Anthropic(api_key="your-key")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    messages=[
        {"role": "user", "content": "Explain RAG in 3 sentences."}
    ]
)

print(response.content[0].text)


# Option 3: AWS Bedrock (No API key needed if on AWS)
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

response = bedrock.invoke_model(
    modelId='anthropic.claude-3-sonnet-20240229-v1:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "messages": [
            {"role": "user", "content": "Explain RAG in 3 sentences."}
        ]
    })
)

result = json.loads(response['body'].read())
print(result['content'][0]['text'])
```

### Evening (1 hr): Experiment
```
Try different:
- System prompts (make it formal, casual, technical)
- Temperatures (0.0 vs 0.5 vs 1.0)
- Questions (coding, creative, factual)

OBSERVE: How does output change?
```

---

## DAY 2: RAG (Retrieval Augmented Generation)

### THE MOST IMPORTANT GENAI CONCEPT FOR INTERVIEWS

```
┌─────────────────────────────────────────────────────────────────┐
│                    RAG EXPLAINED SIMPLY                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   PROBLEM: LLMs don't know your company's private data         │
│                                                                 │
│   SOLUTION: RAG = Search your docs → Feed to LLM → Answer      │
│                                                                 │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐              │
│   │ Your     │     │ Vector   │     │ LLM      │              │
│   │ Documents│ ──► │ Database │ ──► │ (Claude) │ ──► Answer   │
│   └──────────┘     └──────────┘     └──────────┘              │
│        │                │                │                      │
│    Chunking        Embedding        Context +                  │
│    + Embed         + Search         Question                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Morning (2 hrs): RAG Concepts

**The RAG Pipeline (Draw This!):**

```
INGESTION (One-time):
─────────────────────
Documents → Chunking → Embedding → Store in Vector DB
   │           │           │              │
   PDF      Split into   Convert to    Pinecone/
   TXT      ~500 tokens  numbers       Weaviate
   DOCX                  (vectors)     ChromaDB

QUERY (Every request):
──────────────────────
User Question → Embed → Search Vector DB → Top K chunks
                                               │
                                               ▼
                              LLM receives: Question + Retrieved Chunks
                                               │
                                               ▼
                                          Final Answer
```

### Afternoon (3 hrs): Build Simple RAG

```python
# DO THIS: Create rag_simple.py

# Using LangChain (most common in interviews)

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Step 1: Load your document
loader = TextLoader("your_document.txt")
documents = loader.load()

# Step 2: Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # ~500 characters per chunk
    chunk_overlap=50     # overlap to maintain context
)
chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# Step 3: Create embeddings and store
embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Step 4: Create retrieval chain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={"k": 3})
)

# Step 5: Ask questions!
question = "What is the main topic of this document?"
answer = qa_chain.invoke(question)
print(answer)
```

### Evening (1 hr): Understand Each Component

```
Answer these (interview questions!):

1. Why do we chunk documents?
   → LLMs have context limits, smaller chunks = more precise retrieval

2. What's an embedding?
   → Vector representation of text (e.g., 1536 dimensions for OpenAI)

3. How does vector search work?
   → Cosine similarity between query embedding and document embeddings

4. What's the difference between "stuff" vs "map_reduce" chain?
   → stuff: all chunks in one prompt
   → map_reduce: process chunks separately, then combine

5. What happens if chunk size is too small/large?
   → Too small: loses context
   → Too large: retrieval less precise, context limit issues
```

---

## DAY 3: Agents & Tools (LangChain + MCP)

### THE KEY CONCEPT: LLM + Decision Making + Tools

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   User: "What's the weather in Mumbai and book a reminder"     │
│                           │                                     │
│                           ▼                                     │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    AGENT (LLM)                           │  │
│   │   Thinks: "I need to:                                    │  │
│   │   1. Call weather tool for Mumbai                        │  │
│   │   2. Call reminder tool to set reminder"                 │  │
│   └─────────────────────────────────────────────────────────┘  │
│                           │                                     │
│              ┌────────────┼────────────┐                       │
│              ▼            ▼            ▼                        │
│         [Weather]    [Calendar]   [Database]                   │
│           Tool          Tool         Tool                       │
│                                                                 │
│   MCP = Standard way to define and expose these tools          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Morning (2 hrs): LangChain Agent

```python
# DO THIS: Create agent_basic.py

from langchain_openai import ChatOpenAI
from langchain.agents import tool, AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Define custom tools
@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # In real app, call weather API
    return f"Weather in {city}: Sunny, 28°C"

@tool
def search_database(query: str) -> str:
    """Search internal database for information."""
    # In real app, query your DB
    return f"Found 3 results for: {query}"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to someone."""
    return f"Email sent to {to} with subject: {subject}"

# Create agent
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant with access to tools.
    Use the appropriate tool to answer user questions.
    If you don't need a tool, respond directly."""),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

tools = [get_weather, search_database, send_email]
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Test it
response = agent_executor.invoke({
    "input": "What's the weather in Delhi and search for monsoon data"
})
print(response)
```

### Afternoon (2 hrs): Connect Your ADK/MCP Knowledge

```
YOUR MENTAL MAP:
────────────────

LangChain Agent      ←→      ADK Agent
    │                            │
    │ @tool decorator           │ McpToolset
    │                            │
    ▼                            ▼
Custom Functions            MCP Server
(defined in code)         (separate service)

MCP ADVANTAGE:
- Tools are STANDARDIZED (any agent can use)
- Tools are SEPARATE (microservices)
- Tools are REUSABLE (across projects)
```

### Evening (2 hrs): Document Your Understanding

```
INTERVIEW ANSWER TEMPLATES:

Q: "What's the difference between RAG and Agents?"
──────────────────────────────────────────────────
"RAG is about retrieving information from documents to augment
LLM responses. Agents go further - they can DECIDE which tools
to use and take ACTIONS like calling APIs, querying databases,
or executing code. RAG is often ONE tool that an agent uses."

Q: "Explain MCP in simple terms"
───────────────────────────────
"MCP is like a USB standard for AI tools. Just like any USB
device works with any computer, MCP lets any AI agent use
any tool that follows the MCP standard. It separates tool
development from agent development."

Q: "How would you choose between LangChain and ADK?"
─────────────────────────────────────────────────────
"LangChain is more mature with huge ecosystem, great for
quick prototypes. ADK is Google's framework, better integration
with Vertex AI and Google Cloud. If deploying on GCP, ADK.
Otherwise, LangChain for flexibility."
```

---

### ═══════════════════════════════════════════════════════════
### PHASE 2: AWS CLOUD CORE (Day 4-6)
### ═══════════════════════════════════════════════════════════

## DAY 4: AWS Compute + Storage

### Morning (2 hrs): EC2 + Lambda

```
DO THIS (not watch, DO):

TASK 1: Launch EC2
──────────────────
1. AWS Console → EC2 → Launch Instance
2. Amazon Linux 2, t2.micro (free tier)
3. Create key pair, download .pem
4. Connect: ssh -i key.pem ec2-user@<public-ip>
5. Install something: sudo yum install nginx -y
6. Access via browser: http://<public-ip>
7. TERMINATE when done!

TASK 2: Create Lambda
─────────────────────
1. AWS Console → Lambda → Create function
2. Python 3.x, Author from scratch
3. Code:
   
   import json
   
   def lambda_handler(event, context):
       name = event.get('name', 'World')
       return {
           'statusCode': 200,
           'body': json.dumps(f'Hello, {name}!')
       }

4. Test with: {"name": "Hasbrovish"}
5. Add API Gateway trigger
6. Get URL, test in browser
```

### Afternoon (2 hrs): S3 + DynamoDB

```
TASK 3: S3 Operations
─────────────────────
1. Create bucket (unique name)
2. Upload file via console
3. Make public (bucket policy)
4. Access via URL
5. Try with AWS CLI:
   aws s3 cp localfile.txt s3://your-bucket/
   aws s3 ls s3://your-bucket/

TASK 4: DynamoDB
────────────────
1. Create table: Users, Partition key: user_id (String)
2. Add items via console
3. Query via console
4. Try with boto3:

   import boto3
   
   dynamodb = boto3.resource('dynamodb')
   table = dynamodb.Table('Users')
   
   # Put item
   table.put_item(Item={'user_id': '123', 'name': 'Test'})
   
   # Get item
   response = table.get_item(Key={'user_id': '123'})
   print(response['Item'])
```

### Evening (1 hr): Draw Architecture

```
Draw this by hand (you'll need in interviews):

        ┌─────────────────────────────────────────┐
        │            Your GenAI App               │
        └─────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────┐
        │         API Gateway                      │
        │    (REST API endpoint)                   │
        └─────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────┐
        │            Lambda                        │
        │    (Your Python code)                    │
        │    - Calls Bedrock for LLM              │
        │    - Queries DynamoDB for history       │
        │    - Gets docs from S3                  │
        └─────────────────────────────────────────┘
               │              │              │
               ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Bedrock  │   │ DynamoDB │   │    S3    │
        │  (LLM)   │   │ (History)│   │  (Docs)  │
        └──────────┘   └──────────┘   └──────────┘
```

---

## DAY 5: AWS Bedrock (GenAI on AWS)

### THE KEY SERVICE FOR GENAI INTERVIEWS

```
┌─────────────────────────────────────────────────────────────────┐
│                    AWS BEDROCK                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WHAT: Managed service to access foundation models              │
│                                                                 │
│  MODELS AVAILABLE:                                              │
│  - Amazon Titan (Amazon's own)                                  │
│  - Anthropic Claude (Claude 3 Sonnet, Haiku, Opus)             │
│  - Meta Llama                                                   │
│  - Mistral                                                      │
│  - Stability AI (images)                                        │
│  - Cohere (embeddings)                                          │
│                                                                 │
│  WHY USE:                                                       │
│  - No API keys to manage                                        │
│  - IAM-based security                                           │
│  - Data stays in AWS                                            │
│  - Enterprise compliance                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Morning (3 hrs): Bedrock Hands-On

```python
# DO THIS: Create bedrock_demo.py

import boto3
import json

# Initialize Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

# ============================================
# TASK 1: Basic Text Generation with Claude
# ============================================

def call_claude(prompt):
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
    )
    result = json.loads(response['body'].read())
    return result['content'][0]['text']

answer = call_claude("What is AWS Bedrock?")
print(answer)

# ============================================
# TASK 2: Embeddings with Titan
# ============================================

def get_embedding(text):
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v1',
        body=json.dumps({"inputText": text})
    )
    result = json.loads(response['body'].read())
    return result['embedding']

embedding = get_embedding("Hello World")
print(f"Embedding dimension: {len(embedding)}")

# ============================================
# TASK 3: Streaming Response
# ============================================

def stream_claude(prompt):
    response = bedrock.invoke_model_with_response_stream(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
    )
    
    for event in response['body']:
        chunk = json.loads(event['chunk']['bytes'])
        if chunk['type'] == 'content_block_delta':
            print(chunk['delta']['text'], end='', flush=True)

stream_claude("Write a haiku about coding")
```

### Afternoon (2 hrs): Bedrock Knowledge Bases (Managed RAG!)

```
AWS Bedrock Knowledge Bases = RAG as a Service

┌─────────────────────────────────────────────────────────────────┐
│                 BEDROCK KNOWLEDGE BASES                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   YOU PROVIDE:                                                  │
│   └── S3 bucket with documents (PDF, TXT, DOCX, HTML)          │
│                                                                 │
│   BEDROCK DOES:                                                 │
│   ├── Chunking (automatic)                                      │
│   ├── Embedding (Titan or Cohere)                              │
│   ├── Vector storage (OpenSearch Serverless)                   │
│   └── Retrieval + Generation                                    │
│                                                                 │
│   YOU GET:                                                      │
│   └── API endpoint for Q&A over your documents                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

DO THIS:
1. Console → Bedrock → Knowledge bases → Create
2. Data source: S3 (create bucket, upload PDFs)
3. Embedding model: Titan
4. Vector store: Create new OpenSearch Serverless
5. Wait for sync to complete
6. Test in console with questions!
```

```python
# Query Knowledge Base programmatically
import boto3

bedrock_agent = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

response = bedrock_agent.retrieve_and_generate(
    input={'text': 'What is mentioned about pricing?'},
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': 'YOUR_KB_ID',
            'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
        }
    }
)

print(response['output']['text'])
```

---

## DAY 6: AWS Security + Deployment

### Morning (2 hrs): IAM for GenAI

```
┌─────────────────────────────────────────────────────────────────┐
│              IAM FOR GENAI APPLICATIONS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Lambda needs permission to call Bedrock:                       │
│                                                                 │
│  {                                                              │
│    "Version": "2012-10-17",                                    │
│    "Statement": [                                               │
│      {                                                          │
│        "Effect": "Allow",                                       │
│        "Action": [                                              │
│          "bedrock:InvokeModel",                                │
│          "bedrock:InvokeModelWithResponseStream"               │
│        ],                                                       │
│        "Resource": "arn:aws:bedrock:*::foundation-model/*"     │
│      },                                                         │
│      {                                                          │
│        "Effect": "Allow",                                       │
│        "Action": [                                              │
│          "bedrock-agent:Retrieve",                             │
│          "bedrock-agent:RetrieveAndGenerate"                   │
│        ],                                                       │
│        "Resource": "arn:aws:bedrock:*:*:knowledge-base/*"      │
│      }                                                          │
│    ]                                                            │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Afternoon (3 hrs): Deploy GenAI App

```python
# Complete Lambda function for GenAI chatbot
# File: lambda_function.py

import json
import boto3
from datetime import datetime

# Initialize clients
bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ChatHistory')

def lambda_handler(event, context):
    # Parse request
    body = json.loads(event.get('body', '{}'))
    user_id = body.get('user_id', 'anonymous')
    message = body.get('message', '')
    
    # Get chat history from DynamoDB
    history = get_history(user_id)
    
    # Build messages for Claude
    messages = history + [{"role": "user", "content": message}]
    
    # Call Bedrock
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "system": "You are a helpful assistant.",
            "messages": messages
        })
    )
    
    result = json.loads(response['body'].read())
    assistant_message = result['content'][0]['text']
    
    # Save to history
    save_message(user_id, "user", message)
    save_message(user_id, "assistant", assistant_message)
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'response': assistant_message})
    }

def get_history(user_id, limit=10):
    response = table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id},
        Limit=limit,
        ScanIndexForward=False
    )
    messages = []
    for item in reversed(response.get('Items', [])):
        messages.append({
            "role": item['role'],
            "content": item['content']
        })
    return messages

def save_message(user_id, role, content):
    table.put_item(Item={
        'user_id': user_id,
        'timestamp': datetime.now().isoformat(),
        'role': role,
        'content': content
    })
```

---

### ═══════════════════════════════════════════════════════════
### PHASE 3: AZURE BASICS + INTEGRATION (Day 7-8)
### ═══════════════════════════════════════════════════════════

## DAY 7: Azure Quick Overview

### AWS ↔ Azure Mapping (Just Memorize This!)

```
┌────────────────────┬────────────────────┬─────────────────────┐
│      PURPOSE       │        AWS         │       AZURE         │
├────────────────────┼────────────────────┼─────────────────────┤
│ Compute            │ EC2                │ Virtual Machines    │
│ Serverless         │ Lambda             │ Azure Functions     │
│ Containers         │ ECS / EKS          │ ACI / AKS           │
│ Object Storage     │ S3                 │ Blob Storage        │
│ SQL Database       │ RDS                │ Azure SQL           │
│ NoSQL              │ DynamoDB           │ Cosmos DB           │
│ API Management     │ API Gateway        │ API Management      │
│ Identity           │ IAM                │ Azure AD + RBAC     │
│ Secrets            │ Secrets Manager    │ Key Vault           │
│ Monitoring         │ CloudWatch         │ Azure Monitor       │
│ GenAI              │ Bedrock            │ Azure OpenAI        │
│ Vector Search      │ OpenSearch         │ AI Search           │
└────────────────────┴────────────────────┴─────────────────────┘
```

### Hands-On (2 hrs): Azure OpenAI

```python
# DO THIS: Create azure_openai_demo.py

from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://YOUR_RESOURCE.openai.azure.com/",
    api_key="YOUR_KEY",
    api_version="2024-02-15-preview"
)

# Chat completion
response = client.chat.completions.create(
    model="gpt-4",  # Your deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Azure OpenAI?"}
    ]
)

print(response.choices[0].message.content)

# Embeddings
embedding_response = client.embeddings.create(
    model="text-embedding-ada-002",  # Your embedding deployment
    input="Hello World"
)

print(f"Embedding dimension: {len(embedding_response.data[0].embedding)}")
```

---

## DAY 8: Production Patterns

### Morning (2 hrs): GenAI Production Concerns

```
┌─────────────────────────────────────────────────────────────────┐
│          PRODUCTION CHECKLIST (Interview Questions!)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. RATE LIMITING                                               │
│     - Token buckets per user                                    │
│     - AWS: API Gateway throttling                               │
│     - Track: tokens/min, requests/hour                          │
│                                                                 │
│  2. COST CONTROL                                                │
│     - Set max_tokens limits                                     │
│     - Use cheaper models for simple tasks (Haiku vs Opus)      │
│     - Cache frequent responses                                  │
│     - Monitor with CloudWatch/Azure Monitor                     │
│                                                                 │
│  3. LATENCY OPTIMIZATION                                        │
│     - Streaming responses (show tokens as they generate)        │
│     - Async processing for heavy tasks                          │
│     - CDN for static assets                                     │
│                                                                 │
│  4. SECURITY                                                    │
│     - Input validation (prompt injection prevention)            │
│     - Output filtering (PII, harmful content)                   │
│     - Audit logging                                             │
│                                                                 │
│  5. OBSERVABILITY                                               │
│     - Log: prompts, responses, latency, tokens used            │
│     - Metrics: error rate, cost per request                     │
│     - Tracing: end-to-end request flow                         │
│                                                                 │
│  6. GUARDRAILS                                                  │
│     - Content filtering                                         │
│     - Topic restrictions                                        │
│     - AWS: Bedrock Guardrails                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Afternoon (2 hrs): Error Handling & Retry

```python
# Production-ready LLM call with retry
import boto3
import json
import time
from botocore.exceptions import ClientError

class BedrockClient:
    def __init__(self):
        self.client = boto3.client('bedrock-runtime')
        self.max_retries = 3
        self.base_delay = 1
    
    def invoke_with_retry(self, prompt, max_tokens=500):
        for attempt in range(self.max_retries):
            try:
                response = self.client.invoke_model(
                    modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                    body=json.dumps({
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": max_tokens,
                        "messages": [{"role": "user", "content": prompt}]
                    })
                )
                result = json.loads(response['body'].read())
                return {
                    'success': True,
                    'content': result['content'][0]['text'],
                    'usage': result.get('usage', {})
                }
            
            except ClientError as e:
                error_code = e.response['Error']['Code']
                
                if error_code == 'ThrottlingException':
                    # Exponential backoff
                    delay = self.base_delay * (2 ** attempt)
                    time.sleep(delay)
                    continue
                
                elif error_code == 'ModelTimeoutException':
                    # Retry with shorter output
                    max_tokens = max_tokens // 2
                    continue
                
                else:
                    return {
                        'success': False,
                        'error': str(e)
                    }
        
        return {'success': False, 'error': 'Max retries exceeded'}

# Usage
client = BedrockClient()
result = client.invoke_with_retry("Explain GenAI briefly")
print(result)
```

---

### ═══════════════════════════════════════════════════════════
### PHASE 4: INTERVIEW PREP (Day 9-10)
### ═══════════════════════════════════════════════════════════

## DAY 9: Common Interview Questions

### Answer These OUT LOUD (Record Yourself!)

```
Q1: "Explain RAG architecture"
─────────────────────────────
"RAG has two phases: Ingestion and Query.
In Ingestion, we chunk documents, create embeddings, and store in vector DB.
In Query, we embed the question, search for similar chunks, and pass them
with the question to LLM for answer generation.
This lets LLM answer questions about private data it wasn't trained on."

Q2: "How would you build a chatbot for internal docs?"
─────────────────────────────────────────────────────
"I'd use AWS Bedrock Knowledge Bases:
1. Upload docs to S3
2. Create Knowledge Base with Titan embeddings
3. Deploy Lambda function that calls RetrieveAndGenerate API
4. Expose via API Gateway
5. Add DynamoDB for conversation history
6. Frontend calls API, shows streaming responses"

Q3: "What's the difference between fine-tuning and RAG?"
───────────────────────────────────────────────────────
"Fine-tuning changes the model itself - good for learning new behaviors
or specific styles. RAG keeps model unchanged but provides context -
good for factual Q&A over documents. RAG is easier, cheaper, and docs
can be updated without retraining. Use fine-tuning only when RAG isn't enough."

Q4: "How do you handle prompt injection?"
────────────────────────────────────────
"Multiple layers:
1. Input validation - reject suspicious patterns
2. System prompt that explicitly ignores override attempts
3. Output filtering - check for leaked system prompts
4. Separate trusted/untrusted content in prompts
5. Use Bedrock Guardrails for automated filtering"

Q5: "How would you reduce LLM costs?"
────────────────────────────────────
"Several strategies:
1. Use smaller models for simple tasks (Haiku for classification)
2. Cache frequent responses (semantic caching)
3. Limit max_tokens based on task
4. Batch similar requests
5. Use embeddings for similarity search before LLM call
6. Set user quotas and rate limits"

Q6: "Explain your MCP/ADK experience"
────────────────────────────────────
"MCP is a protocol that standardizes how agents communicate with tools.
I've worked with ADK, Google's Agent Development Kit, which has native
MCP support. I've set up agents that connect to MCP servers exposing
tools like database queries and API calls. The advantage is tool
reusability - any MCP-compatible agent can use any MCP server."

Q7: "Serverless vs Containers for GenAI?"
────────────────────────────────────────
"Lambda (serverless): Good for sporadic, event-driven workloads.
Cold start can add latency but auto-scales to zero (cost efficient).

Containers (ECS/EKS): Better for consistent, high-traffic loads.
No cold start, more control over resources.

For GenAI: Lambda for simple chat APIs with moderate traffic.
Containers for high-traffic apps or when you need GPUs."

Q8: "How do you evaluate LLM outputs?"
─────────────────────────────────────
"Multiple approaches:
1. Automated metrics: BLEU, ROUGE for summarization
2. LLM-as-judge: Use GPT-4 to evaluate responses
3. Human evaluation: Relevance, accuracy, helpfulness scores
4. Task-specific: Exact match for classification, F1 for NER
5. RAG-specific: Retrieved chunk relevance, answer faithfulness"
```

---

## DAY 10: Mock Interviews + Final Review

### Morning (2 hrs): Whiteboard Architecture

**Practice drawing these 3 architectures:**

```
ARCHITECTURE 1: Simple Chatbot
──────────────────────────────
[User] → [API Gateway] → [Lambda] → [Bedrock Claude]
                              ↓
                        [DynamoDB] (history)


ARCHITECTURE 2: RAG Application  
────────────────────────────────
                    [S3 Docs]
                        ↓
[User] → [API Gateway] → [Lambda] → [Bedrock KB]
                              ↓          ↓
                        [DynamoDB]  [OpenSearch]


ARCHITECTURE 3: Multi-Agent System
──────────────────────────────────
[User] → [Orchestrator Agent]
              │
    ┌─────────┼─────────┐
    ↓         ↓         ↓
[Research  [Database  [Email
 Agent]    Agent]     Agent]
    │         │         │
    ↓         ↓         ↓
[Web      [RDS]     [SES]
Search]
```

### Afternoon (2 hrs): Rapid Fire Practice

```
ANSWER IN 30 SECONDS EACH:

1. What is a token? → ~4 characters, unit LLM processes
2. What is temperature? → Randomness, 0=deterministic, 1=creative
3. What is an embedding? → Vector representation of text
4. What is chunking? → Splitting docs into smaller pieces for RAG
5. What is context window? → Max tokens LLM can process at once
6. What is Lambda cold start? → Initial setup time when function scales
7. What is IAM role? → Identity for AWS services to access other services
8. What is S3 bucket policy? → JSON rules for bucket access control
9. What is VPC? → Virtual private network in AWS
10. What is API Gateway? → Managed service to create REST/WebSocket APIs
```

### Evening (1 hr): Your Project Story

```
PREPARE THIS STORY:

"In my recent project, I worked on [GenAI application type].

ARCHITECTURE:
- Frontend: [React/Angular/etc.]
- Backend: [Lambda/ECS] with Python
- LLM: [Bedrock Claude / Azure OpenAI]
- Storage: [S3] for documents, [DynamoDB] for history
- Search: [OpenSearch/Pinecone] for vector storage

CHALLENGES SOLVED:
1. [Latency] - Implemented streaming responses
2. [Cost] - Used model routing (simple→Haiku, complex→Sonnet)
3. [Accuracy] - Improved RAG with hybrid search

RESULTS:
- [X]% improvement in response accuracy
- [Y] seconds average response time
- Handles [Z] concurrent users"
```

---

## 🎯 END OF 10 DAYS CHECKLIST

### Must Know (Interview Non-Negotiables)
- [ ] Can explain RAG with diagram
- [ ] Can write LLM API call (OpenAI/Bedrock)
- [ ] Can explain Agent architecture
- [ ] Know AWS: Lambda, S3, DynamoDB, API Gateway, Bedrock
- [ ] Know IAM basics (roles, policies)
- [ ] Can discuss cost/latency optimization
- [ ] Have 2 mini-projects to reference

### Bonus (Extra Points)
- [ ] Know Azure OpenAI
- [ ] Understand MCP/ADK
- [ ] Know vector databases
- [ ] Can discuss fine-tuning vs RAG

---

## 📚 ONLY THESE RESOURCES (NO MORE!)

```
FOR GENAI:
──────────
1. LangChain Docs (python.langchain.com) - Just quickstart
2. AWS Bedrock Getting Started - Official docs
3. Anthropic Cookbook - github.com/anthropics/anthropic-cookbook

FOR AWS:
────────
1. KodeKloud AWS (You have subscription!) 
   → Only: EC2, S3, Lambda, DynamoDB, IAM sections
2. AWS Skill Builder - Free, just Bedrock module

FOR PRACTICE:
─────────────
1. Build 2 projects (chatbot + RAG app)
2. Answer questions out loud daily
3. Draw architectures on paper

THAT'S IT. NO MORE RESOURCES.
```
