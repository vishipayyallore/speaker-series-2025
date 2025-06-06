# Building AI Agents for Startups with Azure - Speaker Series 2025

This repository contains materials for the "Building AI Agents for Startups with Azure" speaker series, featuring production-ready AI agent implementations using Azure services.

## 📁 Repository Structure

### 🤖 Session 1: The Azure Toolbox for Smart Agents

**Location:** `session-1-azure-toolbox/`
**Status:** ✅ Complete and ready for delivery
**Duration:** 60 minutes

Complete implementation of an **AI Agent** (Knowledge Worker Agent) showcasing:

- **Autonomous reasoning** with Azure OpenAI Service (GPT-4)
- **Knowledge retrieval** using Azure AI Search with RAG capabilities
- **Tool execution** via Azure Functions for actions
- **Multi-modal document processing** (PDF, Markdown, Web content)
- **Interactive chat interface** for natural language interaction
- Production-ready web application with comprehensive guides

[📖 View Session 1 Materials →](./session-1-azure-toolbox/)

### 🚀 Session 2: Scaling & Deploying on Azure

**Location:** `session-2-scaling-deploying/`
**Status:** 📋 Outlined (ready for development)
**Duration:** 45 minutes

Session focuses on production deployment topics:

- Deployment options: Azure Container Apps, Azure Functions
- Monitoring with Azure Monitor and Application Insights
- Cost management and smart scaling strategies
- Real-world insights and resource planning

[📖 View Session 2 Materials →](./session-2-scaling-deploying/)

## 🎯 Speaker Series Overview

This series is designed for startup founders, developers, and technical leaders who want to implement **AI Agents** using Azure services.

The demos showcase production-ready AI agents that can:

- **Reason** and make autonomous decisions
- **Access and process** knowledge from documents
- **Execute actions** in response to user requests
- **Learn and adapt** through conversation context
- **Scale** for enterprise workloads

### 🤖 Core AI Agent Capabilities

Our implementation demonstrates all the key characteristics of modern AI Agents:

- **🧠 Autonomous Decision Making** - The agent decides when to search documents, summarize content, or execute actions based on user queries
- **🛠️ Tool Use** - It can call multiple tools (search, summarization, action execution)
- **💾 Memory & Context** - Maintains conversation history and context
- **🎯 Goal-Oriented Behavior** - Works toward fulfilling user requests
- **📄 Multi-Modal Capabilities** - Processes different document types (PDF, Markdown)
- **⚡ Reasoning** - Uses Azure OpenAI to understand queries and formulate responses

### 🏗️ AI Agent Architecture

Our AI Agent implements a complete autonomous reasoning system:

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        AI Agent Architecture                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  👤 User Input                                                      │
│       │                                                             │
│       ▼                                                             │
│  🧠 Azure OpenAI (GPT-4)                                           │
│       │ ┌─────────────────────────────────────────────────────┐    │
│       ├─│ • Natural Language Understanding                    │    │
│       │ │ • Reasoning & Decision Making                       │    │
│       │ │ • Tool Selection & Orchestration                    │    │
│       │ └─────────────────────────────────────────────────────┘    │
│       │                                                             │
│       ▼                                                             │
│  🛠️ Tool Execution Layer                                           │
│       │                                                             │
│   ┌───┴────┐  ┌─────────────┐  ┌──────────────┐                   │
│   │ Search │  │ Summarize   │  │ Execute      │                   │
│   │ Docs   │  │ Content     │  │ Actions      │                   │
│   └───┬────┘  └─────┬───────┘  └──────┬───────┘                   │
│       │             │                 │                           │
│       ▼             ▼                 ▼                           │
│  📚 Azure AI Search  📄 Doc Processor  ⚡ Azure Functions         │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐      │
│  │ • Vector Search │ │ • PDF Extract   │ │ • Email Tasks   │      │
│  │ • RAG Pipeline  │ │ • Markdown Parse│ │ • Report Gen    │      │
│  │ • Reranking     │ │ • Chunking      │ │ • Integrations  │      │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘      │
│                                                                     │
│  💾 Knowledge & Memory                                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ • Conversation History • Document Embeddings                │   │
│  │ • Context Management   • Source Citations                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  🌐 Web Interface                                                   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ • Interactive Chat • Document Upload • Real-time Responses │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Session Topics

1. **Session 1** - Building AI Agents: The Azure Toolbox for Smart Agents ✅
2. **Session 2** - Production AI Agents: Scaling & Deploying on Azure 📋

### Target Audience

- Startup founders exploring AI Agent implementation
- Developers building AI-powered autonomous systems
- Technical leaders planning AI Agent strategy
- Anyone interested in production-ready Azure AI services

## 🚀 Quick Start

### Deploy Your First AI Agent (Session 1)

```bash
cd session-1-azure-toolbox/demo
python setup.py
# Edit .env with your Azure credentials
python verify_setup.py
python -m uvicorn web_interface:app --host 0.0.0.0 --port 8001 --reload
# Open http://localhost:8001 and chat with your AI Agent
```

### For Session 2 Development

Session 2 materials are outlined in `session-2-scaling-deploying/` and ready for development.

## 🛠️ Prerequisites

### Azure Services

- Azure OpenAI Service
- Azure AI Search
- Azure Storage Account
- Azure Function App
- Azure Container Apps (for Session 2)

### Development Environment

- Python 3.11+
- Azure CLI
- Docker (optional)
- VS Code (recommended)

## 📚 Additional Resources

### Documentation

- [Azure OpenAI Service Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Azure AI Search Documentation](https://docs.microsoft.com/en-us/azure/search/)
- [Azure Functions Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/)

### Support

- Check individual session folders for troubleshooting guides
- Review production deployment guides for enterprise considerations
- Use verification scripts to validate Azure connectivity

## 🎉 Contributing

This repository contains presentation materials and demo code. If you're attending the sessions:

1. **Follow along** with the live demos
2. **Take the code home** and experiment
3. **Deploy to your Azure subscription** for hands-on learning
4. **Share feedback** to improve future sessions

## 📅 Schedule

- **May 30, 2025** - Session 1: The Azure Toolbox for Smart Agents (Ready!)
- **TBD** - Session 2: Scaling & Deploying on Azure (In Development)

---

Happy coding with Azure AI Agents! 🌟
