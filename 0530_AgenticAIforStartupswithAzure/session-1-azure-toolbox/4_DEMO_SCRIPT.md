# Demo Script: Azure Toolbox for Smart Agents

## Pre-Demo Setup (5 minutes)

### Execution Order Summary

Execute these steps in the **exact order** shown:

1. **Prerequisites Check** - Verify tools are installed
2. **Azure Resource Creation** - Deploy cloud infrastructure
3. **Local Environment Setup** - Configure Python environment
4. **Service Configuration** - Connect local app to Azure services
5. **Azure Functions Deployment** - Deploy function tools
6. **Verification & Demo Start** - Validate setup and launch demo

---

### Step 1: Prerequisites Check

Ensure you have the following installed:

- **Azure CLI** - [Install Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Azure Functions Core Tools** - `npm install -g azure-functions-core-tools@4`

**Login to Azure:**

```powershell
az login
# Get your subscription ID
az account show --query id -o tsv
# Set the subscription (replace with your actual subscription ID)
az account set --subscription "your-subscription-id"

$SubscriptionId="Your-Subscription-ID"
$ResourceGroupName="rg-agentic-ai-dev-001"
$Location="East US"
```

**Important**: Replace `"your-subscription-id"` with your actual Azure subscription ID from `az account show --query id -o tsv`

---

### Step 2: Azure Resource Creation

#### Option A: Automated Deployment (Recommended)

**Use the automated deployment script:**

```powershell
cd demo
.\deploy_azure_resources.ps1 -ResourceGroupName $ResourceGroupName -Location $Location -SubscriptionId $SubscriptionId
```

This script will:

- Create all required Azure resources
- Deploy AI models (GPT-4o and text-embedding-3-large)
- Output connection strings for your .env file

#### Option B: Manual Setup (If needed)

<details>
<summary>Click to expand manual setup commands</summary>

**Create Resource Group:**

```powershell
az group create --name $ResourceGroupName --location $Location
```

**Create Azure OpenAI Service:**

```powershell
# Create OpenAI resource
az cognitiveservices account create `
  --name "$ResourceGroupName-openai" `
  --resource-group $ResourceGroupName `
  --location $Location `
  --kind "OpenAI" `
  --sku "S0"

# Deploy GPT-4o model
az cognitiveservices account deployment create `
  --resource-group $ResourceGroupName `
  --name "$ResourceGroupName-openai" `
  --deployment-name "gpt-4o" `
  --model-name "gpt-4o" `
  --model-version "2024-08-06" `
  --model-format "OpenAI" `
  --scale-type "Standard" `
  --capacity 10

# Deploy embedding model
az cognitiveservices account deployment create `
  --resource-group $ResourceGroupName `
  --name "$ResourceGroupName-openai" `
  --deployment-name "text-embedding-3-large" `
  --model-name "text-embedding-3-large" `
  --model-version "1" `
  --model-format "OpenAI" `
  --scale-type "Standard" `
  --capacity 10
```

**Create Azure AI Search:**

```powershell
az search service create `
  --name "$ResourceGroupName-search" `
  --resource-group $ResourceGroupName `
  --location $Location `
  --sku "Standard" `
  --partition-count 1 `
  --replica-count 1
```

**Create Storage Account:**

```powershell
$storageAccountName = ($ResourceGroupName -replace '[^a-zA-Z0-9]', '').ToLower() + "storage"
az storage account create `
  --name $storageAccountName `
  --resource-group $ResourceGroupName `
  --location $Location `
  --sku "Standard_LRS" `
  --kind "StorageV2"

az storage container create `
  --name "documents" `
  --account-name $storageAccountName `
  --auth-mode login
```

**Create Function App:**

```powershell
az functionapp create `
  --name "$ResourceGroupName-functions" `
  --resource-group $ResourceGroupName `
  --consumption-plan-location "eastus" `
  --runtime "python" `
  --runtime-version "3.11" `
  --functions-version "4" `
  --storage-account "agenticstorage1234" `
  --os-type "Linux"
```

</details>

---

### Step 3: Local Environment Setup

#### Option A: Automated Setup (Recommended)

```powershell
cd demo
python setup.py
```

This script will:

- Create Python virtual environment
- Install required dependencies
- Create .env file from template
- Display next steps

#### Option B: Manual Setup

```powershell
cd demo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

---

### Step 4: Service Configuration

**Update your .env file** with the values output from Step 2:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://rg-agentic-ai-dev-001-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-openai-api-key-from-deployment
AZURE_OPENAI_API_VERSION=2024-06-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large

# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT=https://rg-agentic-ai-dev-001-search.search.windows.net
AZURE_SEARCH_API_KEY=your-search-api-key-from-deployment
AZURE_SEARCH_INDEX_NAME=knowledge-base

# Azure Storage Configuration
AZURE_STORAGE_ACCOUNT_NAME=rgagenticaidev001storage
AZURE_STORAGE_ACCOUNT_KEY=your-storage-key-from-deployment
AZURE_STORAGE_CONTAINER_NAME=documents

# Azure Function App Configuration
AZURE_FUNCTION_APP_URL=https://rg-agentic-ai-dev-001-functions.azurewebsites.net
AZURE_FUNCTION_KEY=your-function-key

# Get function key with: az functionapp keys list --name rg-agentic-ai-dev-001-functions --resource-group rg-agentic-ai-dev-001
```

---

### Step 5: Deploy Azure Functions

```powershell
cd demo/azure-functions
func azure functionapp publish rg-agentic-ai-dev-001-functions --python
```

**Expected Output:**
After successful deployment, you should see:
```
Functions in rg-agentic-ai-dev-001-functions:
    create_task - [httpTrigger]
        Invoke url: https://rg-agentic-ai-dev-001-functions.azurewebsites.net/api/create_task
    generate_report - [httpTrigger]
        Invoke url: https://rg-agentic-ai-dev-001-functions.azurewebsites.net/api/generate_report
    send_email - [httpTrigger]
        Invoke url: https://rg-agentic-ai-dev-001-functions.azurewebsites.net/api/send_email
```

**Note:** If you encounter language detection issues, the required configuration files (`local.settings.json` and `.funcignore`) are already included in the project.

---

### Step 6: Verification & Demo Start

**Test Azure Functions:**

```powershell
cd demo
.\test-functions.ps1
```

**Expected Output:**
```text
🧪 Testing Azure Functions with Authentication...
📋 Testing Create Task Function...
✅ Success: Task ID: TASK-20250529-180621
📧 Testing Send Email Function...  
✅ Success: Message ID: msg_20250529_180622
📊 Testing Generate Report Function...
✅ Success: Report ID: RPT-20250529-180622
🎉 Function testing complete!
```

**Verify Python setup:**

```powershell
python verify_setup.py
```

**Start the demo:**

```powershell
python web_interface.py
```

**Access the demo:** Open your browser to `http://localhost:8000`

---

## Demo Flow (45 minutes)

### 1. Introduction (5 minutes)

**Opening Statement:**
"Today we're building a complete AI agent using Azure's AI toolkit. This isn't just a chatbot - it's a knowledge worker that can understand documents, answer questions, and take actions."

**Show the Architecture:**

```text
📄 Documents → 🔍 Azure AI Search → 🤖 GPT-4 → 🛠️ Azure Functions → 📊 Response
```

### 2. Azure OpenAI Service Demo (10 minutes)

**Key Points to Cover:**

- GPT-4o for advanced reasoning
- Function calling capabilities
- Built-in content safety

**Live Demo:**

1. Open the web interface at `http://localhost:8000`
2. Show the status indicator confirming Azure connections
3. Ask a simple question: "What can you help me with?"
4. Explain how the agent uses system prompts and function calling

**Sample Questions to Ask:**

- "What are your capabilities?"
- "How do you process information?"
- "Tell me about the TechStart Inc. AI strategy" (using sample documents)
- "What are the main challenges mentioned in our strategy document?"

### 3. Document Processing Pipeline (10 minutes)

**Upload Documents:**

1. Upload a PDF document (use a sample business document)
2. Show the real-time processing feedback
3. Explain the embedding generation process

**Process Web Content:**

1. Enter a URL (e.g., a technical blog post or documentation)
2. Show how it extracts and indexes web content
3. Demonstrate the automatic categorization

**Key Technical Points:**

- Vector embeddings for semantic search
- Automatic text extraction from multiple formats
- Metadata preservation for source attribution

### 4. RAG (Retrieval-Augmented Generation) in Action (10 minutes)

**Ask Document-Specific Questions:**

1. "What are the main topics covered in the uploaded documents?"
2. "Can you summarize the key findings from [specific document]?"
3. "What recommendations are made regarding [specific topic]?"

**Show the Technical Process:**

1. Point out how the agent calls the `search_documents` function
2. Explain the hybrid search (vector + keyword)
3. Demonstrate source attribution in responses

**Advanced Questions:**

- "Compare the approaches mentioned in different documents"
- "What are the potential risks mentioned across all documents?"

### 5. Azure Functions as Agent Tools (8 minutes)

**Pre-Demo Validation:**
Before starting the demo, run the test script to verify all functions are working:
```powershell
.\demo\test-functions.ps1
```

**Demonstrate Function Calling:**

1. "Send an email summary of the key findings to john@example.com"
2. "Create a task to follow up on the recommendations"  
3. "Generate a detailed report based on the analyzed documents"

**Show Live Function Testing:**
During the demo, you can also show the actual HTTP calls:

1. Open the test script results
2. Show the structured JSON responses:
   - **Task Creation**: `TASK-{timestamp}` with assignee, priority, due date
   - **Email Service**: Message ID with delivery confirmation
   - **Report Generation**: Report ID with download URLs and metadata

**Explain Each Function:**

- **send_email**: Integrates with communication services (SendGrid, Azure Communication Services)
- **create_task**: Project management integration (Azure DevOps, Microsoft Planner)
- **generate_report**: Document generation pipeline (Power BI, custom templates)

**Technical Details to Highlight:**
- Functions use HTTP triggers with JSON payloads
- Authentication via function keys for security
- Scalable serverless execution model
- Integration-ready responses with proper error handling

### 6. Azure AI Studio Integration (7 minutes)

**Explain the Benefits:**

- Visual workflow design with Prompt Flow
- Model management and versioning
- Built-in evaluation tools
- Enterprise deployment options

**Show Concepts:**

1. How prompt engineering works at scale
2. A/B testing different agent configurations
3. Monitoring and analytics for production agents

### 7. Business Value Demonstration (3 minutes)

**ROI Scenarios:**

- "This agent processed 50 documents in minutes vs. hours of manual work"
- "Consistent, accurate responses reduce training overhead"
- "Automatic task creation streamlines workflows"

**Startup-Specific Benefits:**

- Pay-per-use scaling
- No infrastructure management
- Enterprise-grade security and compliance
- Rapid prototyping to production

### 8. Q&A and Wrap-up (2 minutes)

**Common Questions & Answers:**

**Q: How much does this cost?**
A: Azure OpenAI pricing is token-based. For a typical startup:

- ~$50-200/month for moderate usage
- AI Search: ~$25-100/month depending on document volume
- Functions: Nearly free for most use cases

**Q: How secure is this?**
A: Azure provides enterprise-grade security:

- Data encryption at rest and in transit
- RBAC for fine-grained access control
- Compliance with SOC, GDPR, HIPAA
- Private endpoints for network isolation

---

## Live Demo Troubleshooting

### Common Issues

1. **API Key Issues**: Double-check .env configuration
2. **Search Index Not Found**: Run the setup endpoint first
3. **Slow Responses**: Expected for first-time embedding generation
4. **Function Calls Failing**: Check Azure Functions configuration
5. **Azure Functions Deployment Issues**:
   - If you get "Can't determine project language", ensure `local.settings.json` exists with `FUNCTIONS_WORKER_RUNTIME: python`
   - Use `--python` flag: `func azure functionapp publish your-function-app --python`
   - Verify Python version compatibility (local vs Azure)
6. **Azure Functions Testing Issues**:
   - **401 Unauthorized**: Add function key to URL: `?code=YOUR_FUNCTION_KEY`
   - **Function not found**: Verify function app name and deployment success
   - **Get function keys**: `az functionapp keys list --name your-function-app --resource-group your-rg`

**Test Functions Independently:**
Use the provided test script to validate all functions:

```powershell
cd demo
.\test-functions.ps1
```

This script tests all three functions with proper authentication and provides detailed response validation.

### Backup Demo Data

If live upload fails, have pre-indexed sample documents ready from the `sample-documents/` folder:

- **AI Strategy**: `markdowns/ai-strategy-document.md` - Company AI strategy and implementation plans
- **Market Research**: `markdowns/market-research-report.md` - Industry analysis and competitor research
- **Travel Brochures**: `collateral/*.pdf` - Sample marketing materials (Dubai, Las Vegas, London, etc.)
- **Monthly Reviews**: `reviews/201801.pdf` through `reviews/201852.pdf` - Historical business reviews

**Pro tip**: Upload the AI strategy document first as it contains comprehensive business context perfect for demonstrating RAG capabilities.

### Function Testing Backup

If the main demo app fails, use the standalone function test script:

```powershell
.\demo\test-functions.ps1
```

**Show these successful responses:**
- **Create Task**: Generates task ID `TASK-{timestamp}` with full project management metadata
- **Send Email**: Returns message ID `msg_{timestamp}` with delivery status
- **Generate Report**: Creates report ID `RPT-{timestamp}` with download URLs

This provides concrete proof that the Azure Functions integration is working and ready for agent tool calling.

### Demo Tips

- Keep questions focused and specific
- Explain what's happening "under the hood"
- Show both successful and error cases
- Emphasize real-world applications

---

## Post-Demo Follow-up

### Resources to Share

1. GitHub repository with complete code
2. Azure AI documentation links
3. Cost calculator for planning
4. Architecture decision templates

### Next Steps for Attendees

1. Sign up for Azure free tier
2. Clone the demo repository
3. Follow the setup guide
4. Join the Azure AI community

### Success Metrics

- Audience engagement during Q&A
- Number of follow-up questions
- Requests for code repository access
- Sign-ups for Azure accounts
