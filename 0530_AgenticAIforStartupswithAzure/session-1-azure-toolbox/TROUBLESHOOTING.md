# Troubleshooting Guide - Azure Toolbox for Smart Agents

This guide helps you resolve common issues when setting up and running the Azure AI agent demo.

## 🔧 Quick Diagnostics

Run the setup verification script first:
```bash
python verify_setup.py
```

## 🚨 Common Issues and Solutions

### 1. Azure OpenAI Connection Issues

#### Error: "Invalid API key"
**Symptoms:**
- `openai.AuthenticationError: Invalid API key provided`
- HTTP 401 responses

**Solutions:**
1. **Check API Key Format**
   ```bash
   # Verify your key starts with correct prefix
   echo $AZURE_OPENAI_API_KEY | cut -c1-10
   # Should show something like "1234567890" (32+ character hex string)
   ```

2. **Verify Endpoint URL**
   ```bash
   # Should end with .openai.azure.com/
   echo $AZURE_OPENAI_ENDPOINT
   # Example: https://myresource.openai.azure.com/
   ```

3. **Check Resource Access**
   ```bash
   # Test with curl
   curl -H "api-key: $AZURE_OPENAI_API_KEY" \
        "$AZURE_OPENAI_ENDPOINT/openai/deployments?api-version=2024-06-01"
   ```

#### Error: "Deployment not found"
**Symptoms:**
- `openai.NotFoundError: The deployment 'gpt-4o' was not found`

**Solutions:**
1. **List Available Deployments**
   ```bash
   curl -H "api-key: $AZURE_OPENAI_API_KEY" \
        "$AZURE_OPENAI_ENDPOINT/openai/deployments?api-version=2024-06-01"
   ```

2. **Update Deployment Name**
   ```bash
   # In your .env file, use the exact deployment name
   AZURE_OPENAI_DEPLOYMENT_NAME=your-actual-deployment-name
   ```

#### Error: "Rate limit exceeded"
**Symptoms:**
- `openai.RateLimitError: Rate limit reached`
- HTTP 429 responses

**Solutions:**
1. **Check Quota Usage**
   - Go to Azure Portal → Your OpenAI Resource → Model deployments
   - Verify your quota limits

2. **Implement Retry Logic**
   ```python
   import time
   import random
   
   async def call_openai_with_retry(client, **kwargs):
       for attempt in range(3):
           try:
               return await client.chat.completions.create(**kwargs)
           except openai.RateLimitError:
               wait_time = (2 ** attempt) + random.uniform(0, 1)
               await asyncio.sleep(wait_time)
       raise Exception("Max retries exceeded")
   ```

### 2. Azure AI Search Issues

#### Error: "Search service not found"
**Symptoms:**
- `azure.core.exceptions.ResourceNotFoundError`
- HTTP 404 on search requests

**Solutions:**
1. **Verify Service Name**
   ```bash
   # Extract service name from endpoint
   echo $AZURE_SEARCH_ENDPOINT | sed 's/https:\/\///' | sed 's/\.search\.windows\.net//'
   ```

2. **Check Service Status**
   ```bash
   curl -H "api-key: $AZURE_SEARCH_API_KEY" \
        "$AZURE_SEARCH_ENDPOINT/servicestats?api-version=2023-11-01"
   ```

#### Error: "Index not found"
**Symptoms:**
- `azure.search.documents._exceptions.RequestEntityTooLargeError`
- Empty search results

**Solutions:**
1. **Create Index Manually**
   ```python
   from azure_search_service import AzureSearchService
   
   search_service = AzureSearchService()
   await search_service.create_index()
   ```

2. **Check Index Status**
   ```bash
   curl -H "api-key: $AZURE_SEARCH_API_KEY" \
        "$AZURE_SEARCH_ENDPOINT/indexes/knowledge-base?api-version=2023-11-01"
   ```

#### Error: "Vector search not working"
**Symptoms:**
- Search returns no results for semantic queries
- Vector field errors

**Solutions:**
1. **Verify Vector Configuration**
   ```python
   # Check if embeddings are being generated
   from knowledge_worker_agent import KnowledgeWorkerAgent
   
   agent = KnowledgeWorkerAgent()
   embedding = await agent.get_embedding("test query")
   print(f"Embedding length: {len(embedding)}")  # Should be 1536 for text-embedding-3-large
   ```

2. **Recreate Index with Vector Fields**
   ```python
   # Delete and recreate index
   search_service = AzureSearchService()
   await search_service.delete_index()
   await search_service.create_index()
   ```

### 3. Document Processing Issues

#### Error: "Failed to extract text from PDF"
**Symptoms:**
- `PyPDF2.errors.PdfReadError`
- Empty text extraction

**Solutions:**
1. **Install Additional Dependencies**
   ```bash
   pip install PyMuPDF  # Alternative PDF library
   pip install pdfplumber  # Another alternative
   ```

2. **Try Alternative Extraction**
   ```python
   import fitz  # PyMuPDF
   
   def extract_text_with_pymupdf(pdf_path):
       doc = fitz.open(pdf_path)
       text = ""
       for page in doc:
           text += page.get_text()
       return text
   ```

#### Error: "Document too large"
**Symptoms:**
- Memory errors during processing
- Timeout errors

**Solutions:**
1. **Process in Chunks**
   ```python
   def chunk_text(text, chunk_size=1000, overlap=100):
       chunks = []
       for i in range(0, len(text), chunk_size - overlap):
           chunk = text[i:i + chunk_size]
           chunks.append(chunk)
       return chunks
   ```

2. **Increase Memory Limits**
   ```python
   # In web_interface.py
   from fastapi import FastAPI, File, UploadFile
   
   app = FastAPI()
   app.add_middleware(
       HTTPSizeMiddleware,
       max_size=50 * 1024 * 1024  # 50MB
   )
   ```

### 4. Web Interface Issues

#### Error: "Port already in use"
**Symptoms:**
- `OSError: [Errno 48] Address already in use`

**Solutions:**
1. **Find and Kill Process**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   
   # Kill the process
   kill -9 <PID>
   ```

2. **Use Different Port**
   ```bash
   uvicorn web_interface:app --host 0.0.0.0 --port 8001
   ```

#### Error: "CORS issues in browser"
**Symptoms:**
- Console errors about CORS
- Failed fetch requests

**Solutions:**
1. **Update CORS Settings**
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # More restrictive in production
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

### 5. Azure Functions Issues

#### Error: "Function app not found"
**Symptoms:**
- HTTP 404 when calling functions
- Connection timeout

**Solutions:**
1. **Check Function App Status**
   ```bash
   az functionapp show --name myapp-functions --resource-group myapp-rg
   ```

2. **Deploy Functions**
   ```bash
   cd azure-functions
   func azure functionapp publish myapp-functions
   ```

#### Error: "Function execution timeout"
**Symptoms:**
- HTTP 500 errors
- Timeout exceptions

**Solutions:**
1. **Increase Timeout**
   ```json
   // In host.json
   {
     "version": "2.0",
     "functionTimeout": "00:05:00",
     "extensions": {
       "http": {
         "routePrefix": "api"
       }
     }
   }
   ```

2. **Optimize Function Code**
   ```python
   # Use async/await properly
   import asyncio
   
   async def main(req: func.HttpRequest) -> func.HttpResponse:
       try:
           # Your function logic here
           return func.HttpResponse("Success", status_code=200)
       except Exception as e:
           logging.error(f"Function failed: {str(e)}")
           return func.HttpResponse("Error", status_code=500)
   ```

## 🔍 Debugging Tools

### 1. Enable Detailed Logging
```python
import logging

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable Azure SDK logging
logging.getLogger('azure').setLevel(logging.DEBUG)
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.DEBUG)
```

### 2. Test Individual Components
```python
# Test Azure OpenAI
async def test_openai():
    from knowledge_worker_agent import KnowledgeWorkerAgent
    agent = KnowledgeWorkerAgent()
    response = await agent.chat("Hello, this is a test")
    print(f"Response: {response}")

# Test Azure Search
async def test_search():
    from azure_search_service import AzureSearchService
    search = AzureSearchService()
    results = await search.search("test query")
    print(f"Results: {len(results)}")

# Run tests
import asyncio
asyncio.run(test_openai())
asyncio.run(test_search())
```

### 3. Network Connectivity
```bash
# Test connectivity to Azure services
nslookup your-openai-resource.openai.azure.com
nslookup your-search-service.search.windows.net

# Test HTTP connectivity
curl -I https://your-openai-resource.openai.azure.com/
curl -I https://your-search-service.search.windows.net/
```

## 🛠️ Development Tools

### VS Code Configuration
Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Web Interface",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/web_interface.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

### Environment Validation Script
```bash
#!/bin/bash
# validate_env.sh

echo "🔍 Validating Azure Environment..."

# Check required environment variables
required_vars=(
    "AZURE_OPENAI_ENDPOINT"
    "AZURE_OPENAI_API_KEY"
    "AZURE_SEARCH_ENDPOINT"
    "AZURE_SEARCH_API_KEY"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Missing: $var"
        exit 1
    else
        echo "✅ Found: $var"
    fi
done

echo "🎉 Environment validation complete!"
```

## 📊 Performance Monitoring

### Add Performance Metrics
```python
import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@measure_time
async def search_documents(query):
    # Your search logic
    pass
```

## 🆘 Getting Help

### Log Collection
Before asking for help, collect these logs:
```bash
# Application logs
tail -f app.log

# Azure CLI logs
az account show
az group list

# Python environment
pip list
python --version
```

### Support Channels
1. **Azure Support**: For Azure service issues
2. **GitHub Issues**: For demo code issues
3. **Stack Overflow**: For general development questions
4. **Azure Community**: For best practices and patterns

### Demo Day Backup Plan
If major issues occur during the demo:

1. **Use Pre-recorded Demo**: Have a backup video ready
2. **Switch to Local Mode**: Use OpenAI API instead of Azure
3. **Static Results**: Show pre-generated responses
4. **Architecture Discussion**: Focus on concepts vs. live coding

Remember: The goal is to teach concepts, not perfect execution!
