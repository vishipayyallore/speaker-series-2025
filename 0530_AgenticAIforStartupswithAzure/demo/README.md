# Knowledge Worker Agent Demo - Quick Start Guide

## Prerequisites
- Python 3.8+
- Azure account with the following services:
  - Azure OpenAI Service
  - Azure AI Search
  - Azure Storage (optional)
  - Azure Functions (optional)

## Setup Instructions

### 1. Clone and Setup Environment
```bash
cd demo
pip install -r requirements.txt
```

### 2. Configure Azure Services
Copy `.env.example` to `.env` and fill in your Azure service details:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large

# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_API_KEY=your-search-api-key
AZURE_SEARCH_INDEX_NAME=knowledge-base

# Azure Storage (Optional)
AZURE_STORAGE_ACCOUNT_NAME=your-storage-account
AZURE_STORAGE_ACCOUNT_KEY=your-storage-key
AZURE_STORAGE_CONTAINER_NAME=documents
```

### 3. Start the Demo
```bash
python web_interface.py
```

Navigate to `http://localhost:8000` to access the demo interface.

### 4. Initialize the Search Index
Click "Setup Demo Data" in the web interface to create the search index.

## Demo Features

### 📄 Document Processing
- Upload PDF, DOCX, TXT, or HTML files
- Process web content from URLs
- Automatic text extraction and indexing
- Vector embeddings for semantic search

### 🤖 Intelligent Chat
- Natural language question answering
- Document-based responses with citations
- Function calling for actions
- Conversation history

### 🔧 Azure Functions Integration
- **send_email**: Email notifications and summaries
- **create_task**: Task management integration
- **generate_report**: Automated report generation

### 🔍 Advanced Search
- Hybrid search (vector + keyword)
- Semantic ranking
- Source attribution
- Category filtering

## Sample Questions to Try

### Basic Interaction
- "What are your capabilities?"
- "How can you help me with document analysis?"

### Document Analysis
- "What are the main topics in the uploaded documents?"
- "Summarize the key findings from [document name]"
- "What recommendations are mentioned across all documents?"

### Action Requests
- "Send an email summary to team@company.com"
- "Create a task to follow up on the budget review"
- "Generate a detailed analysis report"

## Architecture Overview

```
User Input → FastAPI → Knowledge Worker Agent
                            ↓
            Azure OpenAI (GPT-4o) ← Function Tools
                            ↓
            Azure AI Search (RAG) ← Document Store
                            ↓
            Structured Response → User Interface
```

## File Structure
```
demo/
├── web_interface.py              # FastAPI web application
├── knowledge_worker_agent.py     # Main agent implementation
├── azure_search_service.py       # Azure AI Search integration
├── document_processor.py         # Document processing pipeline
├── requirements.txt              # Python dependencies
├── .env.example                 # Environment configuration template
├── templates/
│   └── index.html               # Web interface
└── azure-functions/             # Azure Functions code
    ├── send_email/
    ├── create_task/
    └── generate_report/
```

## Troubleshooting

### Common Issues

**Connection Errors:**
- Verify Azure service endpoints and API keys
- Check network connectivity
- Ensure services are properly provisioned

**Search Index Errors:**
- Run the setup endpoint to create the index
- Verify Azure AI Search service permissions
- Check index name configuration

**Function Call Failures:**
- Azure Functions are optional for the demo
- The agent will work without them configured
- Functions can be deployed separately if needed

**Performance Issues:**
- First-time embedding generation takes longer
- Large documents may take time to process
- Consider document size limits for demo

### Getting Help
- Check the console logs for detailed error messages
- Verify all environment variables are set correctly
- Ensure Azure services are in the same region for best performance

## Extending the Demo

### Adding New Document Types
Modify `document_processor.py` to support additional file formats.

### Custom Functions
Add new Azure Functions in the `azure-functions` directory following the existing pattern.

### UI Customization
Modify `templates/index.html` to customize the interface.

### Advanced Features
- Add user authentication
- Implement conversation persistence
- Add real-time notifications
- Integrate with external APIs

## Production Considerations

### Security
- Use Azure Key Vault for secrets management
- Implement proper RBAC
- Enable private endpoints
- Add input validation and sanitization

### Scalability
- Monitor token usage and costs
- Implement rate limiting
- Use Azure Application Insights for monitoring
- Consider connection pooling for high load

### Reliability
- Add retry logic with exponential backoff
- Implement health checks
- Plan for disaster recovery
- Monitor service dependencies

## Cost Optimization

### Azure OpenAI
- Monitor token usage
- Use streaming for long responses
- Implement caching for repeated queries
- Consider using smaller models for simple tasks

### Azure AI Search
- Optimize index size
- Use appropriate pricing tier
- Monitor search unit usage
- Implement query optimization

### Azure Functions
- Use consumption plan for variable workloads
- Optimize function execution time
- Implement proper error handling
- Monitor execution metrics
