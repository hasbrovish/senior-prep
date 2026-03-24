# 🚀 CLOUD + GENAI INTERVIEW CHEAT SHEET (Print This!)

## 📅 10-Day Schedule At-A-Glance

| Day | Focus | Build This |
|-----|-------|------------|
| 1 | LLM Basics | First API call (OpenAI/Claude) |
| 2 | RAG | Simple RAG with LangChain |
| 3 | Agents | LangChain Agent with tools |
| 4 | AWS Compute | EC2 + Lambda + S3 |
| 5 | AWS Bedrock | Bedrock API + Knowledge Base |
| 6 | AWS Security | IAM + Deploy GenAI app |
| 7 | Azure | Azure OpenAI quick setup |
| 8 | Production | Error handling, retry, costs |
| 9 | Interview Qs | Answer 20 questions aloud |
| 10 | Mock | Whiteboard architectures |

---

## 🧠 GenAI Vocabulary (Memorize!)

| Term | Meaning | Example |
|------|---------|---------|
| Token | ~4 characters | "Hello" = 1 token |
| Prompt | Input to LLM | "Explain RAG" |
| Temperature | Randomness (0-1) | 0=factual, 1=creative |
| Context Window | Max input size | 128K tokens (Claude 3) |
| Embedding | Text → Numbers | 1536-dim vector |
| RAG | Retrieve + Generate | Q&A over your docs |
| Agent | LLM + Tools + Decision | Can call APIs, search |
| MCP | Tool standard protocol | Any agent ↔ any tool |

---

## ☁️ AWS ↔ Azure Mapping

| Purpose | AWS | Azure |
|---------|-----|-------|
| Compute | EC2 | Virtual Machines |
| Serverless | Lambda | Azure Functions |
| Storage | S3 | Blob Storage |
| NoSQL | DynamoDB | Cosmos DB |
| GenAI | **Bedrock** | **Azure OpenAI** |
| Vector DB | OpenSearch | AI Search |
| Identity | IAM | Azure AD |
| Secrets | Secrets Manager | Key Vault |

---

## 🏗️ The ONLY Architecture You Need

```
[User] → [API Gateway] → [Lambda]
                            │
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
         [Bedrock]    [DynamoDB]       [S3]
          (LLM)       (History)      (Docs)
              │             
              ↓             
         [OpenSearch] ← For RAG
         (Vectors)
```

---

## 📝 Top 10 Interview Questions (Answer in 30 sec)

1. **What is RAG?** → Retrieve relevant docs, feed to LLM, generate answer

2. **RAG vs Fine-tuning?** → RAG: adds knowledge, easy update. Fine-tune: changes behavior, expensive

3. **What is an Agent?** → LLM that decides which tools to call based on user request

4. **Lambda vs EC2?** → Lambda: serverless, auto-scale, pay-per-use. EC2: full control, always on

5. **What is Bedrock?** → AWS managed service for foundation models (Claude, Titan, Llama)

6. **How to secure GenAI?** → IAM roles, input validation, output filtering, Guardrails

7. **How to reduce LLM cost?** → Smaller models, caching, token limits, batching

8. **What is vector DB?** → Stores embeddings, enables semantic search for RAG

9. **MCP vs LangChain tools?** → MCP is protocol (standard), LangChain is framework (implementation)

10. **Streaming vs Batch?** → Streaming: show tokens as generated. Batch: wait for complete response

---

## 💻 Code Snippets (Copy-Paste Ready)

### Bedrock Claude Call
```python
import boto3, json
bedrock = boto3.client('bedrock-runtime')
response = bedrock.invoke_model(
    modelId='anthropic.claude-3-sonnet-20240229-v1:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": "Hello"}]
    })
)
print(json.loads(response['body'].read())['content'][0]['text'])
```

### Simple RAG (LangChain)
```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

vectordb = Chroma.from_documents(chunks, OpenAIEmbeddings())
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(), retriever=vectordb.as_retriever()
)
answer = qa.invoke("What is X?")
```

---

## ✅ Day-of-Interview Checklist

- [ ] Can draw RAG architecture on whiteboard
- [ ] Can explain Agent vs RAG difference
- [ ] Know AWS: Lambda, S3, DynamoDB, Bedrock, IAM
- [ ] Can discuss cost optimization strategies
- [ ] Have 1-2 project stories ready
- [ ] Can write basic LLM API call from memory

---

## 🎯 Your Project Story Template

> "I built a **[chatbot/RAG app/agent]** using **[Bedrock/Azure OpenAI]**.
> 
> **Architecture:** API Gateway → Lambda → Bedrock, with DynamoDB for history and S3 for documents.
> 
> **Challenge:** [latency/cost/accuracy] - Solved by [streaming/caching/hybrid search].
> 
> **Result:** [X]ms response time, handles [Y] users, [Z]% accuracy."

---

**Remember:** They want to see you can BUILD, not just explain. Have working code ready! 💪
