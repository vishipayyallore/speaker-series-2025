# Azure OpenAI Python Implementation Matrix

## Complete AI Agent Architecture → Code Mapping

_This matrix maps every Azure OpenAI capability used in the AI Agent to the actual Python implementation code, providing a comprehensive reference for developers building production AI agents._

---

## 🏗️ AI Agent Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        AI Agent Architecture                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  👤 User Input (Natural Language)                                   │
│       │                                                             │
│       ▼                                                             │
│  🧠 Azure OpenAI (GPT-4o) ← Core Reasoning Engine                  │
│       │ ┌─────────────────────────────────────────────────────┐    │
│       ├─│ • Natural Language Understanding                    │    │
│       │ │ • Function Calling & Tool Selection                 │    │
│       │ │ • Multi-turn Conversation Management                │    │
│       │ │ • Context-Aware Response Generation                 │    │
│       │ └─────────────────────────────────────────────────────┘    │
│       │                                                             │
│       ▼                                                             │
│  🛠️ Tool Execution Layer                                           │
│       ├─── 🔍 Azure AI Search (Knowledge Retrieval)               │
│       ├─── ⚡ Azure Functions (Action Execution)                  │
│       └─── 📊 Document Processing (Content Analysis)              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Matrix: Azure OpenAI Capability → Python Implementation

### 1. 🧠 **Core AI Reasoning & Chat Completion**

| **Azure OpenAI Capability**  | **Python Implementation**               | **File Location**                  | **Key Code**                                                                                                                                                                                                                                                                                 |
| ---------------------------- | --------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GPT-4o Chat Completion**   | `AzureOpenAI.chat.completions.create()` | `knowledge_worker_agent.py:94-120` | `python<br/>response = self.client.chat.completions.create(<br/>    model=self.deployment_name,<br/>    messages=conversation_history,<br/>    functions=functions,<br/>    function_call="auto",<br/>    temperature=0.7,<br/>    max_tokens=1500<br/>)`                                    |
| **System Prompt Management** | Built-in system message handling        | `knowledge_worker_agent.py:26-45`  | `python<br/>self.system_prompt = """You are an intelligent knowledge worker agent...<br/>Your capabilities include:<br/>1. Document analysis and search<br/>2. Question answering with citations<br/>3. Task creation and management<br/>4. Email notifications<br/>5. Report generation"""` |
| **Multi-turn Conversation**  | Message history management              | `knowledge_worker_agent.py:94-97`  | `python<br/>conversation_history = [<br/>    {"role": "system", "content": self.system_prompt},<br/>    {"role": "user", "content": message}<br/>]`                                                                                                                                          |

### 2. 🎯 **Function Calling & Tool Integration**

| **Azure OpenAI Capability**    | **Python Implementation**         | **File Location**                   | **Key Code**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------ | --------------------------------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Function Schema Definition** | JSON schema for tool capabilities | `knowledge_worker_agent.py:46-93`   | `python<br/>def get_available_functions(self):<br/>    return [<br/>        {<br/>            "name": "search_documents",<br/>            "description": "Search through uploaded documents",<br/>            "parameters": {<br/>                "type": "object",<br/>                "properties": {<br/>                    "query": {"type": "string", "description": "Search query"},<br/>                    "top_results": {"type": "integer", "description": "Number of results"}<br/>                }<br/>            }<br/>        }]` |
| **Function Call Detection**    | Tool call response parsing        | `knowledge_worker_agent.py:121-130` | `python<br/>if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:<br/>    # Process each tool call<br/>    for tool_call in response.choices[0].message.tool_calls:<br/>        function_result = self.process_function_call(tool_call.function)`                                                                                                                                                                                                                                                      |
| **Function Execution Routing** | Dynamic function dispatcher       | `knowledge_worker_agent.py:231-253` | `python<br/>def process_function_call(self, function_call):<br/>    function_name = function_call.name<br/>    arguments = json.loads(function_call.arguments)<br/>    <br/>    if function_name == "search_documents":<br/>        return self.search_documents(...)<br/>    elif function_name == "execute_action":<br/>        return self.execute_action(...)`                                                                                                                                                                                 |

### 3. 🔍 **Knowledge Retrieval & RAG Implementation**

| **Azure OpenAI Capability**   | **Python Implementation**          | **File Location**                   | **Key Code**                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ----------------------------- | ---------------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Embedding Generation**      | Text embedding for semantic search | `document_processor.py:89-97`       | `python<br/>response = self.openai_client.embeddings.create(<br/>    model=self.embedding_deployment,<br/>    input=text<br/>)<br/>return response.data[0].embedding`                                                                                                                                                                                                                                                                                      |
| **Vector Search Integration** | Azure AI Search with embeddings    | `azure_search_service.py:84-106`    | `python<br/>search_results = self.search_client.search(<br/>    search_text=query,<br/>    vector_queries=[VectorizedQuery(<br/>        vector=query_vector,<br/>        k_nearest_neighbors=top_k,<br/>        fields="content_vector"<br/>    )]<br/>)`                                                                                                                                                                                                  |
| **Context Injection**         | RAG pattern implementation         | `knowledge_worker_agent.py:162-189` | `python<br/>def search_documents(self, query: str, top_results: int = 5):<br/>    search_results = await self.search_service.search(<br/>        query=query, top_k=top_results<br/>    )<br/>    <br/>    # Format results for AI context<br/>    formatted_results = [{<br/>        "content": result["content"],<br/>        "source": result["title"],<br/>        "relevance_score": result["@search.score"]<br/>    } for result in search_results]` |

### 4. ⚡ **Azure Functions Integration (Tool Execution)**

| **Azure OpenAI Capability** | **Python Implementation**     | **File Location**                                   | **Key Code**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------------- | ----------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **HTTP Function Calls**     | REST API integration          | `knowledge_worker_agent.py:191-229`                 | `python<br/>def execute_action(self, action_type: str, parameters: Dict[str, Any]):<br/>    function_url = f"{self.function_app_url}/api/{action_type}"<br/>    headers = {<br/>        "Content-Type": "application/json",<br/>        "x-functions-key": self.function_key<br/>    }<br/>    <br/>    response = requests.post(<br/>        function_url, headers=headers,<br/>        json=parameters, timeout=30<br/>    )`                                                                      |
| **Task Creation Tool**      | Azure Function implementation | `azure-functions/create_task/__init__.py:11-74`     | `python<br/>def main(req: func.HttpRequest) -> func.HttpResponse:<br/>    req_body = req.get_json()<br/>    <br/>    # Generate task ID<br/>    task_id = f"TASK-{datetime.now().strftime('%Y%m%d-%H%M%S')}"<br/>    <br/>    # Create task object<br/>    task = {<br/>        "success": True,<br/>        "task_id": task_id,<br/>        "title": req_body.get('title'),<br/>        "assignee": req_body.get('assignee'),<br/>        "priority": req_body.get('priority', 'medium')<br/>    }` |
| **Email Service Tool**      | Communication integration     | `azure-functions/send_email/__init__.py:11-83`      | `python<br/>def main(req: func.HttpRequest) -> func.HttpResponse:<br/>    req_body = req.get_json()<br/>    <br/>    # Simulate email sending<br/>    message_id = f"msg_{int(datetime.now().timestamp())}"<br/>    <br/>    email_response = {<br/>        "success": True,<br/>        "message_id": message_id,<br/>        "to_email": req_body.get('to_email'),<br/>        "subject": req_body.get('subject'),<br/>        "delivery_status": "sent"<br/>    }`                                |
| **Report Generation Tool**  | Document generation service   | `azure-functions/generate_report/__init__.py:11-89` | `python<br/>def main(req: func.HttpRequest) -> func.HttpResponse:<br/>    req_body = req.get_json()<br/>    <br/>    # Generate report ID<br/>    report_id = f"RPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"<br/>    <br/>    report_response = {<br/>        "success": True,<br/>        "report_id": report_id,<br/>        "title": req_body.get('title'),<br/>        "download_url": f"https://reports.example.com/{report_id}.pdf"<br/>    }`                                              |

### 5. 📄 **Document Processing & Analysis**

| **Azure OpenAI Capability** | **Python Implementation**         | **File Location**               | **Key Code**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| --------------------------- | --------------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Content Extraction**      | Multi-format document processing  | `document_processor.py:27-60`   | `python<br/>def extract_text_from_file(self, file_path: str, content_type: str):<br/>    if content_type == 'application/pdf':<br/>        return self._extract_from_pdf(file_path)<br/>    elif content_type in ['application/vnd.openxmlformats...']:<br/>        return self._extract_from_docx(file_path)<br/>    elif content_type == 'text/plain':<br/>        return self._extract_from_txt(file_path)`                                                                                                                                                                                     |
| **Text Chunking**           | Intelligent content segmentation  | `document_processor.py:105-125` | `python<br/>def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200):<br/>    chunks = []<br/>    start = 0<br/>    <br/>    while start < len(text):<br/>        end = start + chunk_size<br/>        chunk = text[start:end]<br/>        chunks.append(chunk)<br/>        start = end - overlap<br/>    <br/>    return chunks`                                                                                                                                                                                                                                               |
| **Document Indexing**       | Vector storage in Azure AI Search | `document_processor.py:127-165` | `python<br/>async def process_and_index_document(self, file_path: str, content_type: str):<br/>    # Extract text<br/>    text_content = self.extract_text_from_file(file_path, content_type)<br/>    <br/>    # Create chunks<br/>    chunks = self.chunk_text(text_content)<br/>    <br/>    # Generate embeddings and index<br/>    for i, chunk in enumerate(chunks):<br/>        embedding = self.generate_embedding(chunk)<br/>        document = {<br/>            "id": f"{document_id}_{i}",<br/>            "content": chunk,<br/>            "content_vector": embedding<br/>        }` |

### 6. 🌐 **Web Interface & API Layer**

| **Azure OpenAI Capability** | **Python Implementation**        | **File Location**          | **Key Code**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| --------------------------- | -------------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Chat API Endpoint**       | FastAPI route for chat interface | `web_interface.py:54-76`   | `python<br/>@app.post("/chat")<br/>async def chat_endpoint(request: ChatRequest):<br/>    agent = KnowledgeWorkerAgent()<br/>    <br/>    try:<br/>        response = await agent.chat(request.message)<br/>        return {"response": response}<br/>    except Exception as e:<br/>        raise HTTPException(status_code=500, detail=str(e))`                                                                                                                                                                                 |
| **Document Upload**         | File processing endpoint         | `web_interface.py:78-106`  | `python<br/>@app.post("/upload")<br/>async def upload_document(file: UploadFile = File(...)):<br/>    processor = DocumentProcessor()<br/>    <br/>    try:<br/>        # Save uploaded file<br/>        file_path = f"uploads/{file.filename}"<br/>        with open(file_path, "wb") as buffer:<br/>            shutil.copyfileobj(file.file, buffer)<br/>        <br/>        # Process and index<br/>        result = await processor.process_and_index_document(<br/>            file_path, file.content_type<br/>        )` |
| **Health Check**            | Service status validation        | `web_interface.py:108-124` | `python<br/>@app.get("/health")<br/>async def health_check():<br/>    agent = KnowledgeWorkerAgent()<br/>    search_service = AzureSearchService()<br/>    <br/>    status = {<br/>        "openai": await agent._test_openai_connection(),<br/>        "search": await search_service._test_connection(),<br/>        "functions": agent.function_app_url is not None<br/>    }`                                                                                                                                                 |

---

## 🔧 **Environment Configuration & Setup**

### Azure Service Configuration

| **Service**         | **Environment Variables**                                                                                                     | **Configuration File** | **Usage in Code**                                                                                                                                                                                                  |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Azure OpenAI**    | `AZURE_OPENAI_ENDPOINT`<br/>`AZURE_OPENAI_API_KEY`<br/>`AZURE_OPENAI_DEPLOYMENT_NAME`<br/>`AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | `.env`                 | `python<br/>self.client = AzureOpenAI(<br/>    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),<br/>    api_key=os.getenv("AZURE_OPENAI_API_KEY"),<br/>    api_version="2024-06-01"<br/>)`                       |
| **Azure AI Search** | `AZURE_SEARCH_ENDPOINT`<br/>`AZURE_SEARCH_API_KEY`<br/>`AZURE_SEARCH_INDEX_NAME`                                              | `.env`                 | `python<br/>self.search_client = SearchClient(<br/>    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),<br/>    index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),<br/>    credential=AzureKeyCredential(api_key)<br/>)` |
| **Azure Functions** | `AZURE_FUNCTION_APP_URL`<br/>`AZURE_FUNCTION_KEY`                                                                             | `.env`                 | `python<br/>function_url = f"{self.function_app_url}/api/{action_type}"<br/>headers = {"x-functions-key": self.function_key}`                                                                                      |

---

## 🚀 **Production Deployment Patterns**

### 1. **Scalability Configuration**

```python
# knowledge_worker_agent.py - Production settings
class KnowledgeWorkerAgent:
    def __init__(self):
        # Connection pooling for high throughput
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version="2024-06-01",
            max_retries=3,
            timeout=30.0
        )

        # Async operation support
        self.async_client = AsyncAzureOpenAI(...)
```

### 2. **Error Handling & Resilience**

```python
# knowledge_worker_agent.py - Robust error handling
async def chat(self, message: str) -> str:
    try:
        response = await self.client.chat.completions.create(...)
        return response.choices[0].message.content
    except RateLimitError:
        # Implement exponential backoff
        await asyncio.sleep(2 ** retry_count)
        return await self.chat(message)
    except APIConnectionError:
        # Fallback to cached responses
        return self._get_cached_response(message)
```

### 3. **Performance Optimization**

```python
# azure_search_service.py - Optimized search
class AzureSearchService:
    async def search(self, query: str, top_k: int = 5):
        # Use semantic ranking for better results
        search_results = await self.search_client.search(
            search_text=query,
            query_type=QueryType.SEMANTIC,
            semantic_configuration_name="default",
            top=top_k,
            select=["content", "title", "url"]
        )
```

---

## 📊 **Monitoring & Analytics Integration**

### Application Insights Integration

```python
# knowledge_worker_agent.py - Telemetry
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
))

class KnowledgeWorkerAgent:
    async def chat(self, message: str) -> str:
        # Track usage metrics
        logger.info(f"Chat request received", extra={
            'custom_dimensions': {
                'message_length': len(message),
                'user_id': self.current_user_id,
                'timestamp': datetime.now().isoformat()
            }
        })
```

---

## 🔒 **Security Implementation**

### 1. **Authentication & Authorization**

```python
# web_interface.py - Security middleware
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    # Validate JWT token with Azure AD
    try:
        payload = jwt.decode(token.credentials, verify=True)
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/chat")
async def chat_endpoint(request: ChatRequest, user: dict = Depends(verify_token)):
    # User context available for personalization
    agent = KnowledgeWorkerAgent(user_context=user)
    return await agent.chat(request.message)
```

### 2. **Data Privacy & Compliance**

```python
# document_processor.py - PII Detection
class DocumentProcessor:
    def sanitize_content(self, text: str) -> str:
        # Remove PII before indexing
        import re

        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)

        # Remove phone numbers
        text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[PHONE]', text)

        return text
```

---

## 🎯 **Key Implementation Insights**

### 1. **Function Calling Protocol**

- **Azure OpenAI expects specific message structure**: `assistant` message with `tool_calls` must precede `tool` response messages
- **JSON schema validation**: Function parameters must match exact schema definitions
- **Error handling**: Graceful degradation when tools are unavailable

### 2. **RAG Pattern Optimization**

- **Chunking strategy**: 1000 characters with 200 character overlap for context preservation
- **Embedding caching**: Store embeddings to avoid regeneration costs
- **Hybrid search**: Combine vector and keyword search for better results

### 3. **Production Considerations**

- **Token monitoring**: Track usage across all OpenAI calls
- **Rate limiting**: Implement client-side throttling
- **Async operations**: Use async/await for concurrent processing
- **Caching strategy**: Cache frequent queries and embeddings

---

## 📈 **Cost Optimization Strategies**

### Token Usage Monitoring

```python
# knowledge_worker_agent.py - Cost tracking
class KnowledgeWorkerAgent:
    def __init__(self):
        self.token_usage_tracker = {
            'prompt_tokens': 0,
            'completion_tokens': 0,
            'total_cost': 0.0
        }

    async def chat(self, message: str) -> str:
        response = await self.client.chat.completions.create(...)

        # Track token usage
        usage = response.usage
        self.token_usage_tracker['prompt_tokens'] += usage.prompt_tokens
        self.token_usage_tracker['completion_tokens'] += usage.completion_tokens

        # Calculate cost (GPT-4o pricing)
        prompt_cost = (usage.prompt_tokens / 1000) * 0.03
        completion_cost = (usage.completion_tokens / 1000) * 0.06
        self.token_usage_tracker['total_cost'] += prompt_cost + completion_cost
```

---

This matrix provides a complete reference for implementing production-grade AI Agents using Azure OpenAI. Each capability is mapped to actual working Python code from the demo, making it easy to understand both the concepts and their practical implementation.

**Next Steps for Implementation:**

1. 🔧 **Setup**: Use the environment configuration patterns
2. 🧠 **Core AI**: Implement the chat completion patterns
3. 🛠️ **Tools**: Add Azure Functions following the provided templates
4. 🔍 **Knowledge**: Integrate RAG using Azure AI Search patterns
5. 📊 **Production**: Apply monitoring, security, and optimization strategies

The complete demo code is available in the repository and demonstrates these patterns in a fully functional AI Agent implementation.
