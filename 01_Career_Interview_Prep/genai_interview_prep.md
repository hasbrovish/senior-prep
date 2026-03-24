# 🚀 GenAI Interview Preparation - Complete Guide
## 4-5 Hour Crash Course with Deep Dives

---

# ⏰ TIME ALLOCATION STRATEGY (4-5 hours)

| Block | Time | Topics |
|-------|------|--------|
| Block 1 | 60 min | Transformer Architecture + LLM Fundamentals |
| Block 2 | 75 min | RAG (End-to-End) — THE MOST ASKED TOPIC |
| Block 3 | 45 min | Prompt Engineering + Fine-tuning |
| Block 4 | 45 min | AI Agents + LangChain/LangGraph |
| Block 5 | 30 min | Evaluation Metrics + Ethics + Hallucination |
| Block 6 | 30 min | System Design Scenarios + Mock Q&A Practice |

---

# 📌 SECTION 1: TRANSFORMER ARCHITECTURE & LLM FUNDAMENTALS

---

## Q1: What is a Transformer and why did it revolutionize NLP?

### 🎤 Interview Answer Style:
> "Transformers were introduced in the 2017 paper 'Attention Is All You Need' by Vaswani et al. Before transformers, we relied on RNNs and LSTMs which processed sequences sequentially — meaning word-by-word. This made them slow and caused vanishing gradient problems for long sequences.
>
> Transformers solved this with the **self-attention mechanism** which processes all tokens in parallel. The key innovation is that every token can attend to every other token directly, capturing long-range dependencies efficiently. This parallelism also made training on GPUs much faster.
>
> The architecture has two main parts: **Encoder** (understands input) and **Decoder** (generates output). Models like BERT use only the encoder, GPT uses only the decoder, and T5 uses both."

### 🔍 Expected Follow-up Deep Dives:

**F1: Explain Self-Attention step by step.**

> "For each token, we create three vectors: Query (Q), Key (K), and Value (V) by multiplying the input embedding with learned weight matrices.
>
> Step 1: Compute attention scores = Q × K^T (dot product tells us how relevant each token is to the current token)
> Step 2: Scale by √d_k (dimension of key) to prevent large values that push softmax into tiny gradients
> Step 3: Apply softmax to get attention weights (probabilities summing to 1)
> Step 4: Multiply weights × V to get the weighted sum
>
> Formula: Attention(Q,K,V) = softmax(QK^T / √d_k) × V"

**F2: What is Multi-Head Attention?**

> "Instead of computing attention once, we do it h times in parallel with different learned projections. Each 'head' can attend to different types of relationships — one head might capture syntactic relationships, another semantic similarity. The outputs are concatenated and linearly transformed. This gives the model richer representational power."

**F3: What's the difference between Encoder-only, Decoder-only, and Encoder-Decoder models?**

| Type | Example | Use Case | Attention Type |
|------|---------|----------|---------------|
| Encoder-only | BERT, RoBERTa | Classification, NER, Embeddings | Bidirectional (sees full context) |
| Decoder-only | GPT, LLaMA, Claude | Text generation, Chat | Causal/Masked (sees only past tokens) |
| Encoder-Decoder | T5, BART | Translation, Summarization | Cross-attention between encoder & decoder |

---

## Q2: Explain the key parameters: Temperature, Top-k, Top-p

### 🎤 Interview Answer:
> "These are **decoding strategies** that control how the model picks the next token from its probability distribution.
>
> **Temperature** (0 to 2 typically): Controls randomness. Lower temperature (0.1) makes the model more deterministic/focused by sharpening the probability distribution. Higher temperature (1.5) makes it more creative/random by flattening the distribution. At temperature = 0, it always picks the highest probability token (greedy decoding).
>
> **Top-k**: Only considers the k most probable tokens. If k=50, the model randomly samples from only the top 50 tokens. Eliminates low-probability noise.
>
> **Top-p (Nucleus Sampling)**: Instead of a fixed count, it picks the smallest set of tokens whose cumulative probability exceeds p. If p=0.9, it considers tokens until their probabilities add up to 90%. This is more adaptive than top-k.
>
> In practice, I'd use low temperature (0.1-0.3) for factual tasks, medium (0.7) for general chat, and higher (1.0+) for creative writing."

### 🔍 Follow-up: What's the difference between Greedy, Beam Search, and Sampling?

> "**Greedy**: Always picks highest probability token. Fast but can miss globally optimal sequences.
> **Beam Search**: Maintains top-B candidates at each step. Better quality but slower. Used in translation.
> **Sampling with Temperature/Top-k/Top-p**: Introduces controlled randomness. Better for creative and conversational tasks."

---

## Q3: What are Embeddings and why are they important in GenAI?

### 🎤 Interview Answer:
> "Embeddings are dense vector representations of text (words, sentences, or documents) in a continuous vector space where semantically similar content is closer together.
>
> In GenAI, embeddings serve two critical purposes:
> 1. **Input representation**: LLMs convert tokens into embeddings before processing through transformer layers
> 2. **Semantic search**: In RAG systems, we embed documents and queries into the same vector space to find relevant information using cosine similarity
>
> Popular embedding models include OpenAI's text-embedding-ada-002, sentence-transformers, and Cohere's embed models. The key difference is dimensionality (768, 1024, 1536) and the training objective (contrastive learning, masked language modeling)."

### 🔍 Follow-up: How do you choose the right embedding model?

> "I'd consider: task domain (general vs specialized), dimensionality (higher = more expressive but more storage), benchmarks like MTEB leaderboard, and whether I need multilingual support. For production, I also factor in latency and cost. Fine-tuned domain-specific embeddings often outperform general ones."

---

## Q4: Explain Tokenization in LLMs

### 🎤 Interview Answer:
> "Tokenization is how we break text into units the model can process. LLMs don't see raw text — they see token IDs.
>
> **Common approaches:**
> - **BPE (Byte Pair Encoding)**: Used by GPT. Starts with characters and iteratively merges the most frequent pairs. Handles unknown words by breaking them into known subwords.
> - **WordPiece**: Used by BERT. Similar to BPE but uses likelihood instead of frequency.
> - **SentencePiece**: Used by LLaMA/T5. Language-agnostic, operates on raw text including spaces.
>
> **Why it matters**: Token count affects cost (API pricing is per token), context window utilization, and how well the model handles domain-specific terms. A word like 'transformers' might be one token while 'pneumonoultramicroscopicsilicovolcanoconiosis' could be 8+ tokens."

---

# 📌 SECTION 2: RAG (Retrieval-Augmented Generation) — MOST ASKED TOPIC

---

## Q5: What is RAG and why do we need it?

### 🎤 Interview Answer:
> "RAG combines a retrieval system with a generative model. Instead of relying solely on the LLM's parametric knowledge (what it learned during training), we first retrieve relevant documents from an external knowledge base and pass them as context to the LLM.
>
> **Why RAG is needed:**
> 1. **Knowledge cutoff**: LLMs don't know about events after training
> 2. **Hallucination reduction**: Grounding responses in retrieved facts
> 3. **Domain specificity**: Company-specific data that wasn't in training
> 4. **Cost efficiency**: Cheaper than fine-tuning for knowledge updates
> 5. **Transparency**: Can cite sources, enabling verification
>
> The basic pipeline is: **User Query → Embed Query → Retrieve Similar Documents → Augment Prompt with Context → Generate Response**"

### 🔍 Follow-up: Walk me through the end-to-end RAG pipeline

> "**Indexing Phase (Offline):**
> 1. Document Ingestion: Load PDFs, docs, web pages using loaders
> 2. Chunking: Split documents into manageable pieces (512-1024 tokens)
> 3. Embedding: Convert chunks to vectors using an embedding model
> 4. Storage: Store vectors in a vector database (Pinecone, Weaviate, ChromaDB, Qdrant)
>
> **Query Phase (Online):**
> 1. Query Processing: Optionally rewrite/expand the user query
> 2. Retrieval: Embed the query, search vector DB for top-k similar chunks
> 3. Re-ranking: Use a cross-encoder to re-rank retrieved chunks for better relevance
> 4. Augmentation: Construct prompt with retrieved context + original query
> 5. Generation: LLM generates answer grounded in the context
> 6. Post-processing: Validate, add citations, format response"

---

## Q6: Explain Chunking Strategies in RAG

### 🎤 Interview Answer:
> "Chunking is how we split documents into pieces for embedding and retrieval. It's crucial because:
> - LLM context windows have token limits
> - Large chunks dilute the embedding (less precise retrieval)
> - Small chunks lose context (incomplete information)
>
> **Main strategies:**
>
> 1. **Fixed-size chunking**: Split by token count (e.g., 512 tokens) with overlap (e.g., 50 tokens). Simple but may break mid-sentence.
>
> 2. **Recursive Character Splitting**: Uses a hierarchy of separators ['\n\n', '\n', ' ', ',']. Tries to split at paragraph boundaries first, then sentences, then words. This is the most commonly used approach in LangChain.
>
> 3. **Semantic Chunking**: Uses embeddings to detect topic shifts. Groups semantically similar sentences together. More intelligent but computationally expensive.
>
> 4. **Document-structure-aware**: Respects headers, sections, tables. Best for structured documents like PDFs with clear sections.
>
> **Typical sweet spot**: 256-1024 tokens with 10-20% overlap. I'd always experiment and evaluate with the specific dataset."

### 🔍 Follow-up: What happens with too large vs too small chunks?

> "**Too large**: Embedding becomes a vague average of many topics → poor retrieval precision, noise in context, and wasted context window tokens.
> **Too small**: Loss of surrounding context → may retrieve a fragment that's meaningless without its neighbors, and increases the number of retrieval calls needed."

---

## Q7: Explain Vector Databases and Similarity Search

### 🎤 Interview Answer:
> "Vector databases are purpose-built for storing and querying high-dimensional vector embeddings. Unlike traditional databases that match exact values, vector DBs find **semantically similar** content.
>
> **How similarity search works:**
> - Cosine Similarity: Measures the angle between vectors. Most common for text. Range [-1, 1].
> - Euclidean Distance: Measures straight-line distance. Better when magnitude matters.
> - Dot Product: Similar to cosine but doesn't normalize. Faster computation.
>
> **Indexing algorithms for fast search:**
> - **HNSW (Hierarchical Navigable Small World)**: Graph-based. Best accuracy-speed tradeoff. Used by Qdrant, Weaviate.
> - **IVF (Inverted File Index)**: Clusters vectors, searches only relevant clusters. Used by FAISS.
> - **Product Quantization (PQ)**: Compresses vectors for memory efficiency. Trades some accuracy for speed.
>
> These are ANN (Approximate Nearest Neighbor) algorithms — they sacrifice perfect accuracy for massive speed improvements.
>
> **Popular vector DBs**: Pinecone (managed), Weaviate (open source), Qdrant (open source), ChromaDB (lightweight), Milvus (enterprise)."

---

## Q8: What is Hybrid Search and Re-ranking?

### 🎤 Interview Answer:
> "Hybrid search combines two retrieval approaches to get the best of both worlds:
>
> **Sparse Retrieval (BM25/TF-IDF)**: Keyword-based. Excellent for exact term matching, acronyms, product names. Misses semantic meaning.
>
> **Dense Retrieval (Embedding-based)**: Semantic understanding. Captures meaning even with different words. Can miss exact keyword matches.
>
> **Hybrid approach**: Run both searches, then merge results using **Reciprocal Rank Fusion (RRF)**:
> ```
> RRF_score(d) = Σ 1/(k + rank_i(d))
> ```
> where k is typically 60. Documents that rank high in both methods get the highest fused score.
>
> **Re-ranking** happens after hybrid search. We take the top-N results and use a **cross-encoder** model to score each (query, document) pair more accurately. Cross-encoders are more precise than bi-encoders because they see both query and document simultaneously, but they're too slow for initial retrieval over millions of documents."

### 🔍 Follow-up: Why can't we just use cross-encoders for everything?

> "Cross-encoders score one (query, doc) pair at a time. With 1 million documents, that's 1 million forward passes — way too slow. Bi-encoders pre-compute document embeddings once, so retrieval is just a vector similarity lookup (milliseconds). The two-stage approach gives us speed from bi-encoders and accuracy from cross-encoders."

---

## Q9: How do you evaluate a RAG system?

### 🎤 Interview Answer:
> "RAG evaluation has two parts: **retrieval quality** and **generation quality**.
>
> **Retrieval Metrics:**
> - **Precision@k**: Of k retrieved docs, how many are relevant?
> - **Recall@k**: Of all relevant docs, how many did we retrieve?
> - **MRR (Mean Reciprocal Rank)**: How high is the first relevant result?
> - **NDCG (Normalized Discounted Cumulative Gain)**: Considers both relevance and ranking position
> - **MAP (Mean Average Precision)**: Average precision at each relevant document position
>
> **Generation Metrics (using frameworks like RAGAS):**
> - **Faithfulness**: Is the answer actually supported by the retrieved context? (Catches hallucinations)
> - **Answer Relevancy**: Does the answer address the user's question?
> - **Context Relevancy**: Are the retrieved documents relevant to the query?
> - **Context Recall**: Did we retrieve all the information needed to answer?
>
> **Key insight**: A system can have perfect Context Recall but still fail if the LLM hallucinates (low Faithfulness). That's why we need both retrieval AND generation metrics."

---

## Q10: What are Advanced RAG Techniques?

### 🎤 Interview Answer:
> "Beyond basic RAG, several advanced patterns solve real-world problems:
>
> **1. Query Transformation:**
> - **HyDE (Hypothetical Document Embeddings)**: Generate a hypothetical answer first, embed that instead of the query. Often retrieves better results.
> - **Multi-query**: LLM generates multiple query variations, retrieves for each, merges results.
> - **Step-back prompting**: Ask a more general question first to get broader context.
>
> **2. Corrective RAG (CRAG):**
> - After retrieval, an LLM evaluates if documents are relevant
> - If not → triggers web search or alternative retrieval
> - Adds a self-correction loop
>
> **3. Self-RAG:**
> - Model decides whether it even needs retrieval
> - Generates reflection tokens to self-evaluate
> - Iterates if quality is insufficient
>
> **4. Agentic RAG:**
> - An AI agent orchestrates the retrieval pipeline
> - Can decide: which tools to use, when to retrieve, when to search the web
> - More adaptive than fixed pipelines
>
> **5. Graph RAG:**
> - Uses knowledge graphs alongside vector search
> - Better for questions requiring multi-hop reasoning
> - Captures relationships between entities"

---

# 📌 SECTION 3: PROMPT ENGINEERING & FINE-TUNING

---

## Q11: Explain Prompt Engineering Techniques

### 🎤 Interview Answer:
> "Prompt engineering is the art of designing inputs to get the best outputs from LLMs without changing model weights.
>
> **Key techniques (from simple to advanced):**
>
> **1. Zero-shot**: Just give the instruction. 'Classify this review as positive or negative.'
>
> **2. Few-shot**: Provide examples in the prompt. 'Review: Great product → Positive. Review: Terrible → Negative. Review: {input} → ?'
>
> **3. Chain of Thought (CoT)**: 'Think step by step before answering.' Forces the model to show reasoning, dramatically improving accuracy on math/logic tasks.
>
> **4. Tree of Thought (ToT)**: Explores multiple reasoning paths and evaluates which is best. Like CoT but with branching.
>
> **5. ReAct (Reason + Act)**: Interleaves reasoning with tool use. 'Thought: I need to search for X. Action: Search(X). Observation: Y. Thought: Now I know...'
>
> **6. Self-Consistency**: Generate multiple responses with higher temperature, then take the majority vote. Improves reliability.
>
> **7. Structured Output**: Constrain the model to output JSON, XML, or specific schemas for downstream parsing."

### 🔍 Follow-up: How do you choose between prompt engineering and fine-tuning?

> "**Use Prompt Engineering when:**
> - Quick iteration needed
> - Small training data
> - Task is within the model's general capabilities
> - You need flexibility to change instructions frequently
>
> **Use Fine-tuning when:**
> - Consistent specific output format/style needed
> - Domain-specific terminology or behavior
> - Large labeled dataset available
> - Need to reduce prompt size (and cost) for production
> - Prompt engineering has hit its ceiling"

---

## Q12: Explain Fine-tuning approaches for LLMs

### 🎤 Interview Answer:
> "Fine-tuning adapts a pre-trained model to a specific task or domain.
>
> **Full Fine-tuning**: Update all model weights. Expensive, requires lots of GPU memory. Risk of catastrophic forgetting.
>
> **Parameter-Efficient Fine-Tuning (PEFT)** — the practical approach:
>
> **LoRA (Low-Rank Adaptation)**:
> - Instead of updating the full weight matrix W, decompose the update as W + ΔW where ΔW = A × B
> - A and B are low-rank matrices (e.g., rank 8-64)
> - Only trains ~0.1-1% of parameters
> - Memory efficient, can be merged back into base model for zero inference overhead
>
> **QLoRA**:
> - Combines LoRA with quantization (4-bit)
> - Can fine-tune a 65B parameter model on a single 48GB GPU
> - Uses NF4 (Normal Float 4-bit) data type + double quantization
>
> **Adapter layers**: Insert small trainable layers between frozen transformer layers.
>
> **Prefix tuning**: Prepend trainable virtual tokens to the input. Only these tokens are trained."

### 🔍 Follow-up: Explain RLHF (Reinforcement Learning from Human Feedback)

> "RLHF is how models like ChatGPT are aligned with human preferences. Three stages:
> 1. **Supervised Fine-Tuning (SFT)**: Train on high-quality human demonstrations
> 2. **Reward Model Training**: Humans rank multiple model outputs → train a reward model on these preferences
> 3. **PPO (Proximal Policy Optimization)**: Use the reward model to further fine-tune the LLM to generate responses humans prefer
>
> **DPO (Direct Preference Optimization)** is a simpler alternative that skips the reward model entirely — it directly optimizes the policy from preference data."

---

# 📌 SECTION 4: AI AGENTS & FRAMEWORKS

---

## Q13: What are AI Agents and how do they work?

### 🎤 Interview Answer:
> "An AI agent is an LLM-powered system that can **reason**, **plan**, and **take actions** using external tools to accomplish tasks autonomously.
>
> **Key components:**
> 1. **LLM (Brain)**: Reasoning and decision-making
> 2. **Tools**: Functions the agent can call (search, calculator, APIs, code execution)
> 3. **Memory**: Short-term (conversation) and long-term (persistent storage)
> 4. **Planning**: Breaking complex tasks into steps
>
> **Common patterns:**
> - **ReAct**: Thought → Action → Observation loop
> - **Plan-and-Execute**: Create a full plan first, then execute steps
> - **Reflexion**: Agent reviews its own outputs and self-corrects
>
> **Example**: 'Book me a flight to Delhi next Friday under ₹5000'
> → Agent thinks: I need to search flights → calls flight search API → compares options → selects best → asks user for confirmation → books"

### 🔍 Follow-up: What's the difference between LangChain and LangGraph?

> "**LangChain**: A framework for building LLM applications. Provides chains (sequential pipelines), tools, memory, and retrieval components. Great for linear workflows like RAG pipelines.
>
> **LangGraph**: Built on top of LangChain for **stateful, multi-actor** applications. Uses a graph structure where nodes are functions/agents and edges define flow. Supports cycles (agent loops), conditional branching, and human-in-the-loop. Better for complex agent workflows.
>
> **When to use which:**
> - Simple RAG pipeline → LangChain
> - Multi-step agent with decision points and loops → LangGraph
> - Multi-agent collaboration → LangGraph"

---

## Q14: Explain Function Calling / Tool Use in LLMs

### 🎤 Interview Answer:
> "Function calling is the mechanism that allows LLMs to interact with external tools and APIs in a structured way.
>
> **How it works:**
> 1. Define available functions with their names, descriptions, and parameter schemas (usually JSON Schema)
> 2. Send user query + function definitions to the LLM
> 3. LLM decides whether to call a function and which one
> 4. LLM outputs a structured JSON with function name and arguments
> 5. Your code executes the actual function
> 6. Send the result back to the LLM
> 7. LLM generates the final user-facing response
>
> **Key point**: The LLM never actually executes the function — it only generates the intent to call it with the right parameters. The execution happens in your application code. This separation is critical for safety and control."

---

# 📌 SECTION 5: EVALUATION, HALLUCINATION & ETHICS

---

## Q15: What are Hallucinations and how do you mitigate them?

### 🎤 Interview Answer:
> "Hallucinations occur when LLMs generate content that is factually incorrect, fabricated, or unsupported by the input context. They 'confidently make stuff up.'
>
> **Types:**
> - **Intrinsic**: Contradicts the source input
> - **Extrinsic**: Generates information not present in any source (can't be verified)
>
> **Mitigation strategies:**
>
> 1. **RAG**: Ground responses in retrieved facts
> 2. **Temperature reduction**: Lower randomness for factual tasks
> 3. **Chain-of-Thought prompting**: Forces step-by-step reasoning
> 4. **Self-consistency**: Generate multiple answers, take the consensus
> 5. **Output validation**: Use a second LLM call to fact-check the response against the context
> 6. **Constrained generation**: Force structured outputs, limit to known entities
> 7. **Fine-tuning on high-quality data**: Improve the model's factual grounding
> 8. **Confidence scoring**: Ask the model to rate its confidence; flag low-confidence answers
> 9. **Guardrails**: Use systems like NeMo Guardrails or custom validation layers"

---

## Q16: How do you evaluate LLM outputs?

### 🎤 Interview Answer:
> "LLM evaluation is multi-dimensional:
>
> **Automated Metrics:**
> - **BLEU**: N-gram overlap with reference. Common in translation.
> - **ROUGE**: Recall-based overlap. Common in summarization.
> - **BERTScore**: Semantic similarity using BERT embeddings. Better than BLEU/ROUGE for open-ended generation.
> - **Perplexity**: How surprised the model is by the text. Lower = more fluent.
>
> **LLM-as-Judge:**
> - Use a powerful model (GPT-4, Claude) to evaluate outputs on criteria like helpfulness, accuracy, coherence
> - Can score 1-5 or do pairwise comparisons
> - Increasingly popular for production systems
>
> **Human Evaluation:**
> - Gold standard but expensive and slow
> - Use for high-stakes applications
>
> **Domain-Specific:**
> - For RAG: RAGAS framework (Faithfulness, Answer Relevancy, Context metrics)
> - For code: Pass@k (does generated code pass test cases?)
> - For safety: Red-teaming, adversarial testing"

---

## Q17: What are the ethical concerns in GenAI?

### 🎤 Interview Answer:
> "Key ethical concerns I'd highlight:
>
> 1. **Bias amplification**: Models trained on internet data inherit and can amplify societal biases (gender, race, culture). Mitigation: diverse training data, fairness audits, bias benchmarks.
>
> 2. **Deepfakes and misinformation**: Realistic fake content generation. Mitigation: watermarking, detection tools, content authentication.
>
> 3. **Privacy**: Models can memorize and leak training data including PII. Mitigation: differential privacy, data sanitization, output filtering.
>
> 4. **Intellectual property**: Training on copyrighted content raises legal questions about fair use and ownership of generated content.
>
> 5. **Environmental impact**: Training large models requires massive compute and energy.
>
> 6. **Job displacement**: Automation of creative and knowledge work.
>
> As a responsible developer, I'd implement content moderation layers, maintain transparency about AI-generated content, and build human oversight into production systems."

---

# 📌 SECTION 6: SYSTEM DESIGN & SCENARIO-BASED QUESTIONS

---

## Q18: Design a customer support chatbot using GenAI for an e-commerce company

### 🎤 Interview Answer:
> "I'd design this as a **RAG-based agentic system**:
>
> **Architecture:**
>
> **1. Knowledge Base Layer:**
> - Ingest product catalog, FAQs, return policies, shipping info
> - Chunk and embed into vector database (Qdrant/Pinecone)
> - Set up automated refresh pipeline for catalog updates
>
> **2. Retrieval Layer:**
> - Hybrid search: BM25 for product names/SKUs + dense for semantic queries
> - Re-ranking with cross-encoder for top-20 results
>
> **3. Agent Layer:**
> - Router: Classify intent (product query, order status, complaint, return request)
> - Tools: Order lookup API, refund API, escalation to human agent
> - Memory: Track conversation context within session
>
> **4. Generation Layer:**
> - LLM generates response grounded in retrieved context
> - System prompt enforces brand voice, politeness, and guardrails
> - Output validation: Check for hallucinated product features or prices
>
> **5. Safety & Monitoring:**
> - Content moderation layer
> - Confidence threshold — escalate to human if below threshold
> - Log all interactions for quality analysis
> - A/B testing framework for prompt improvements
>
> **Scaling considerations:**
> - Cache frequent queries and their responses
> - Use smaller models (Mistral 7B) for simple FAQs, route complex queries to larger models
> - Rate limiting and queue management"

---

## Q19: Your RAG system is returning irrelevant results. How do you debug it?

### 🎤 Interview Answer:
> "I'd follow a systematic debugging approach:
>
> **Step 1: Isolate the problem** — Is it retrieval or generation?
> - Log the retrieved chunks separately. If chunks are relevant but answer is wrong → generation problem.
> - If chunks themselves are irrelevant → retrieval problem.
>
> **Step 2: If retrieval is the issue:**
> - Check chunking: Are chunks too large/small? Is context being split at bad points?
> - Check embedding model: Is it appropriate for the domain? Try domain-specific embeddings.
> - Check query: Is the user query too vague? Try query expansion or HyDE.
> - Check similarity threshold: Too high = too few results, too low = noise.
> - Try hybrid search if using only dense retrieval (might miss keyword matches).
> - Add re-ranking layer.
>
> **Step 3: If generation is the issue:**
> - Improve the system prompt with clearer instructions
> - Add 'only answer from the provided context' guardrail
> - Reduce temperature
> - Try a more capable model
>
> **Step 4: Evaluate systematically:**
> - Build a test set of (query, expected_answer, relevant_docs) triples
> - Measure retrieval metrics (Precision@k, Recall@k)
> - Measure generation metrics (Faithfulness, Relevancy)
> - Iterate on the weakest component"

---

## Q20: Compare Fine-tuning vs RAG — when to use which?

### 🎤 Interview Answer:

| Aspect | RAG | Fine-tuning |
|--------|-----|-------------|
| **Best for** | Adding/updating knowledge | Changing behavior/style |
| **Knowledge freshness** | Easy to update (just update DB) | Need to retrain |
| **Cost** | Infra cost for vector DB + retrieval | Training compute cost |
| **Hallucination** | Reduces (grounded in docs) | Can still hallucinate |
| **Data needed** | Documents (unlabeled OK) | Labeled training examples |
| **Latency** | Higher (retrieval + generation) | Lower (single inference) |
| **Transparency** | Can cite sources | Black box |

> "In practice, the best production systems often combine both: fine-tune for the desired output style and behavior, and use RAG for up-to-date domain knowledge."

---

# 📌 IMPLEMENTATION CODE SNIPPETS (for hands-on questions)

---

## Basic RAG with LangChain (Python)

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# 1. Load documents
loader = PyPDFLoader("company_docs.pdf")
documents = loader.load()

# 2. Chunk documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)
chunks = text_splitter.split_documents(documents)

# 3. Create embeddings and store in vector DB
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# 4. Create retrieval chain
llm = ChatOpenAI(model="gpt-4", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # stuff = put all docs in context
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)

# 5. Query
result = qa_chain.invoke({"query": "What is the return policy?"})
print(result["result"])
```

## Simple Agent with LangChain

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain import hub

# Define tools
def search_orders(order_id: str) -> str:
    # Mock function - replace with actual API call
    return f"Order {order_id}: Shipped, arriving March 1"

def calculate_refund(amount: str) -> str:
    return f"Refund of ₹{amount} will be processed in 5-7 days"

tools = [
    Tool(name="SearchOrders", func=search_orders,
         description="Search for order status. Input: order ID"),
    Tool(name="CalculateRefund", func=calculate_refund,
         description="Calculate refund amount. Input: amount in INR"),
]

# Create agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run
response = agent_executor.invoke({
    "input": "What's the status of order #12345?"
})
```

## LangGraph Agent (Stateful)

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# Define state
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_step: str

# Define nodes
def classify_intent(state):
    # LLM classifies the user intent
    messages = state["messages"]
    # ... LLM call to classify
    return {"next_step": "retrieval"}  # or "api_call" or "human"

def retrieve_docs(state):
    # RAG retrieval
    # ... vector search
    return {"messages": [{"role": "system", "content": "Retrieved: ..."}]}

def generate_response(state):
    # LLM generates final response
    # ... LLM call with context
    return {"messages": [{"role": "assistant", "content": "Here's your answer..."}]}

# Build graph
graph = StateGraph(AgentState)
graph.add_node("classify", classify_intent)
graph.add_node("retrieve", retrieve_docs)
graph.add_node("generate", generate_response)

graph.set_entry_point("classify")
graph.add_conditional_edges("classify", lambda s: s["next_step"],
    {"retrieval": "retrieve", "direct": "generate"})
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

app = graph.compile()
```

---

# 📌 RAPID-FIRE SHORT ANSWER QUESTIONS

---

**Q: What is the context window?**
> The maximum number of tokens (input + output) the model can process at once. GPT-4 Turbo: 128K, Claude 3.5: 200K, Gemini 1.5: 1M.

**Q: What is Attention Masking?**
> In decoder-only models, causal masking prevents tokens from attending to future tokens during training, ensuring autoregressive generation.

**Q: What are Guardrails?**
> Safety layers around LLMs that filter harmful inputs/outputs, enforce topic boundaries, prevent jailbreaks, and ensure compliance.

**Q: Explain Zero-shot vs Few-shot vs Fine-tuned**
> Zero-shot: No examples, just instruction. Few-shot: Examples in the prompt. Fine-tuned: Model weights actually changed with training data.

**Q: What is Knowledge Distillation?**
> Training a smaller "student" model to mimic a larger "teacher" model. Used to create deployment-friendly models that are faster and cheaper.

**Q: What is Quantization?**
> Reducing model weight precision (FP32 → FP16 → INT8 → INT4) to reduce memory and speed up inference. QLoRA uses 4-bit quantization.

**Q: What is a Vector Index?**
> A data structure that organizes vectors for fast approximate nearest neighbor search. Examples: HNSW (graph-based), IVF (cluster-based), LSH (hash-based).

**Q: What is Model Context Protocol (MCP)?**
> A standard protocol by Anthropic for connecting LLMs to external data sources and tools. Provides a unified interface for tool use across different LLM providers.

**Q: What is an Embedding Model vs a Generative Model?**
> Embedding models convert text to fixed-size vectors (for search/similarity). Generative models produce new text token-by-token. Different architectures and training objectives.

**Q: What is Catastrophic Forgetting?**
> When fine-tuning, the model loses previously learned general knowledge. Mitigated by LoRA (only trains small adapters), low learning rates, or mixing general data.

---

# 📌 RESOURCES FOR QUICK REVISION (Priority Order)

---

## Must-Read (Before Interview):
1. **GitHub - genieincodebottle/generative-ai** — Most comprehensive free GenAI resource with interview PDF
   → https://github.com/genieincodebottle/generative-ai
2. **GitHub - aishwaryanr/awesome-generative-ai-guide** — 60 curated interview questions with answers
   → https://github.com/aishwaryanr/awesome-generative-ai-guide
3. **GitHub - KalyanKS-NLP/RAG-Interview-Questions** — 100+ RAG specific questions
   → https://github.com/KalyanKS-NLP/RAG-Interview-Questions-and-Answers-Hub

## Quick Videos (if time permits):
4. **3Blue1Brown — Attention in Transformers** (YouTube, ~20 min) — Best visual explanation
5. **Andrej Karpathy — Let's build GPT** (YouTube) — Code-level understanding

## For Deep Dives:
6. **LangChain Documentation** — https://python.langchain.com
7. **LlamaIndex Documentation** — https://docs.llamaindex.ai
8. **RAGAS Evaluation Framework** — https://docs.ragas.io
9. **Hugging Face Course** — https://huggingface.co/learn

## Papers (mention in interview for bonus points):
- "Attention Is All You Need" (2017) — Transformers
- "REALM / RAG" (2020) — Original RAG paper
- "LoRA" (2021) — Efficient fine-tuning
- "Chain-of-Thought Prompting" (2022) — Reasoning
- "ReAct" (2022) — Agents
- "Self-RAG" (2023) — Advanced RAG
- "DPO" (2023) — Alignment without reward models

---

# 💡 INTERVIEW TIPS

1. **Always connect theory to practice**: "I used this in my Digital Shelf Operations project where..."
2. **Mention tradeoffs**: Never say one approach is always better. Discuss when to use what.
3. **Draw diagrams**: For system design questions, offer to draw the architecture.
4. **Ask clarifying questions**: "What scale are we talking about? What's the latency requirement?"
5. **Be honest about unknowns**: "I haven't implemented this, but my understanding is..."
6. **Use your GSTN experience**: High-scale systems (14M users, 100K concurrent) is impressive context for production deployment discussions.

---

*Good luck with your interview! You've got this! 🎯*
