# Demo Script: Azure Toolbox for Smart Agents

## Pre-Demo Setup (5 minutes)

### Azure Services Configuration
1. **Azure OpenAI Service**
   ```bash
   # Check your .env file has these values configured:
   AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
   ```

2. **Azure AI Search**
   ```bash
   AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
   AZURE_SEARCH_API_KEY=your-search-api-key
   AZURE_SEARCH_INDEX_NAME=knowledge-base
   ```

3. **Azure Storage (Optional)**
   ```bash
   AZURE_STORAGE_ACCOUNT_NAME=your-storage-account
   AZURE_STORAGE_ACCOUNT_KEY=your-storage-key
   AZURE_STORAGE_CONTAINER_NAME=documents
   ```

### Start the Demo
```bash
cd demo
pip install -r requirements.txt
python web_interface.py
```

## Demo Flow (45 minutes)

### 1. Introduction (5 minutes)
**Opening Statement:**
"Today we're building a complete AI agent using Azure's AI toolkit. This isn't just a chatbot - it's a knowledge worker that can understand documents, answer questions, and take actions."

**Show the Architecture:**
```
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

**Demonstrate Function Calling:**
1. "Send an email summary of the key findings to john@example.com"
2. "Create a task to follow up on the recommendations"
3. "Generate a detailed report based on the analyzed documents"

**Explain Each Function:**
- **send_email**: Integrates with communication services
- **create_task**: Project management integration
- **generate_report**: Document generation pipeline

**Show the JSON responses** to demonstrate structured data handling

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

### 8. Q&A and Wrap-up (10 minutes)

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

**Q: Can this integrate with our existing systems?**
A: Yes! The agent can:
- Connect to your databases via Azure Functions
- Integrate with Microsoft 365, Salesforce, etc.
- Use Logic Apps for no-code integrations
- Custom APIs through HTTP triggers

**Q: How do we prevent hallucinations?**
A: Multiple strategies:
- RAG grounds responses in your data
- Content safety filters
- Confidence scoring
- Human-in-the-loop workflows for critical decisions

## Live Demo Troubleshooting

### Common Issues:
1. **API Key Issues**: Double-check .env configuration
2. **Search Index Not Found**: Run the setup endpoint first
3. **Slow Responses**: Expected for first-time embedding generation
4. **Function Calls Failing**: Check Azure Functions configuration

### Backup Demo Data:
If live upload fails, have pre-indexed sample documents ready:
- Company policy document
- Technical specification
- Market research report
- Financial analysis

### Demo Tips:
- Keep questions focused and specific
- Explain what's happening "under the hood"
- Show both successful and error cases
- Emphasize real-world applications

## Post-Demo Follow-up

### Resources to Share:
1. GitHub repository with complete code
2. Azure AI documentation links
3. Cost calculator for planning
4. Architecture decision templates

### Next Steps for Attendees:
1. Sign up for Azure free tier
2. Clone the demo repository
3. Follow the setup guide
4. Join the Azure AI community

### Success Metrics:
- Audience engagement during Q&A
- Number of follow-up questions
- Requests for code repository access
- Sign-ups for Azure accounts

## Technical Deep-Dive Notes

### Azure OpenAI Best Practices:
- Use system prompts for consistency
- Implement retry logic with exponential backoff
- Monitor token usage and costs
- Use streaming for real-time responses

### Search Index Optimization:
- Design appropriate field mappings
- Use semantic ranking for better results
- Implement proper chunking strategies
- Monitor search analytics

### Function Design Patterns:
- Keep functions stateless
- Implement proper error handling
- Use managed identity for authentication
- Design for idempotency

### Production Considerations:
- Implement rate limiting
- Add comprehensive logging
- Use Application Insights for monitoring
- Plan for disaster recovery
