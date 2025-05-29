# Session 1: The Azure Toolbox for Smart Agents

This folder contains all materials for **Session 1** of the "Agentic AI for Startups with Azure" speaker series.

## 📁 Folder Contents

### 📄 Core Documentation

- **`The Azure Toolbox for Smart Agents.md`** - Main session content and learning materials
- **`presentation_outline.md`** - Slide deck structure and talking points
- **`PRODUCTION_GUIDE.md`** - Guide for taking the demo to production
- **`TROUBLESHOOTING.md`** - Common issues and solutions
- **`SESSION_COMPLETE.md`** - Summary of completed work and next steps

### 💻 Demo Application (`demo/`)

Complete working Knowledge Worker Agent with:

- **Web Interface** (`web_interface.py`) - FastAPI-based chat application
- **AI Agent** (`knowledge_worker_agent.py`) - OpenAI integration with function calling
- **Document Processing** (`document_processor.py`) - Multi-format document ingestion
- **Azure Search** (`azure_search_service.py`) - Vector search and RAG implementation
- **Azure Functions** (`azure-functions/`) - Serverless action execution
- **Deployment Tools** - Docker, setup scripts, and Azure resource deployment

### 📚 Sample Content (`sample-documents/`)

- AI strategy document for demo purposes
- Market research report for testing
- Example documents to demonstrate the agent's capabilities

## 🚀 Quick Start

1. **Navigate to the demo folder:**

   ```bash
   cd demo
   ```

2. **Run the setup script:**

   ```bash
   python setup.py
   ```

3. **Configure your Azure credentials:**

   ```bash
   # Edit .env file with your Azure service details
   ```

4. **Verify everything works:**

   ```bash
   python verify_setup.py
   ```

5. **Start the demo:**

   ```bash
   python web_interface.py
   ```

6. **Open your browser:**
   ```
   http://localhost:8000
   ```

## 🎯 Session Overview

**Duration:** 60 minutes
**Target Audience:** Startup founders, developers, and technical leaders
**Difficulty Level:** Intermediate

### Learning Objectives

- Understand Azure AI services for building agents
- Implement RAG (Retrieval-Augmented Generation) patterns
- Build API-based tools with Azure Functions
- Create production-ready AI agents

### Key Technologies

- Azure OpenAI Service (GPT-4o, embeddings)
- Azure AI Search (vector search, hybrid search)
- Azure Functions (serverless compute)
- FastAPI (web framework)
- Docker (containerization)

## 🏗️ Architecture

```
📄 Documents → 🔍 Azure AI Search → 🤖 Azure OpenAI → 🛠️ Azure Functions → 📊 Response
```

The demo showcases a complete AI agent workflow:

1. **Document Ingestion** - Upload and process various file formats
2. **Vector Indexing** - Create searchable embeddings in Azure AI Search
3. **Intelligent Q&A** - RAG-powered responses with source citations
4. **Action Execution** - Function calling for business tasks

## 📋 Prerequisites

### Azure Services Required

- Azure OpenAI Service (with GPT-4o and text-embedding-3-large deployments)
- Azure AI Search (Standard tier recommended)
- Azure Storage Account (for document storage)
- Azure Function App (for action execution)

### Development Environment

- Python 3.11+
- Azure CLI (optional, for deployment)
- Docker (optional, for containerization)

## 💡 Demo Scenarios

### Primary Demo Flow

1. **Upload a document** (use provided sample documents)
2. **Ask questions** about the content
3. **Show citations** and source attribution
4. **Demonstrate function calling** (create tasks, send emails)
5. **Explain production considerations**

### Sample Questions for Demo

- "What is our AI strategy?"
- "Summarize our competitive landscape"
- "Create a task to review our market position"
- "What are the key risks mentioned in the documents?"

## 🔧 Troubleshooting

If you encounter issues:

1. Check `TROUBLESHOOTING.md` for common problems
2. Run `verify_setup.py` to validate Azure connectivity
3. Ensure all environment variables are set correctly
4. Verify Azure service quotas and permissions

## 📈 Production Deployment

For production deployment guidance, see:

- `PRODUCTION_GUIDE.md` - Comprehensive deployment strategies
- `demo/deploy_azure_resources.ps1` - Automated resource provisioning
- `demo/Dockerfile` and `docker-compose.yml` - Containerization

## 🎉 Success!

This session demonstrates how startups can rapidly build sophisticated AI agents using Azure services, with a clear path from prototype to production.

---

**Part of:** Agentic AI for Startups with Azure Speaker Series  
**Session:** 2 of 4  
**Next:** Session 2 - Scaling & Deploying on Azure
