# Agentic AI for Startups with Azure - Speaker Series 2025

This repository contains materials for the "Agentic AI for Startups with Azure" speaker series, part of the 2025 technical presentation series.

## 📁 Repository Structure

### 🤖 Session 1: The Azure Toolbox for Smart Agents

**Location:** `session-1-azure-toolbox/`
**Status:** ✅ Complete and ready for delivery
**Duration:** 60 minutes

Complete implementation of a Knowledge Worker Agent demo showcasing:

- Azure OpenAI Service integration
- Azure AI Search with RAG capabilities
- Azure Functions for action execution
- Production-ready web application
- Comprehensive documentation and deployment guides

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

This series is designed for startup founders, developers, and technical leaders who want to implement AI agents using Azure services.

### Session Topics

1. **Session 1** - The Azure Toolbox for Smart Agents ✅
2. **Session 2** - Scaling & Deploying on Azure 📋

### Target Audience

- Startup founders exploring AI implementation
- Developers building AI-powered applications
- Technical leaders planning AI strategy
- Anyone interested in Azure AI services

## 🚀 Quick Start

### For Session 1 Demo

```bash
cd session-1-azure-toolbox/demo
python setup.py
# Edit .env with your Azure credentials  
python verify_setup.py
python web_interface.py
# Open http://localhost:8000
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

Happy coding with Azure AI! 🌟


 python -m uvicorn web_interface:app --host 0.0.0.0 --port 8000 --reload