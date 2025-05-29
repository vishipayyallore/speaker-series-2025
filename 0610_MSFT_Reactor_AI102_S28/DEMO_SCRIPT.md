# Demo Script: Custom Skills in Azure AI Search
## Session: AI-102 - Implementing Custom Skills in Azure AI Search
### Date: 27-May-2025 at 03:30 PM IST

---

## Pre-Demo Setup (30 minutes before session)

### Prerequisites Checklist
- [ ] Azure Subscription with sufficient credits
- [ ] Visual Studio Code with Azure Functions extension
- [ ] .NET 8 SDK installed
- [ ] Azure CLI installed and logged in
- [ ] Postman or similar REST client
- [ ] Sample documents in blob storage

### Environment Setup

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "your-subscription-id"

# Create resource group
az group create --name rg-ai102-customskills --location eastus

# Create storage account for documents
az storage account create \
  --name stai102demo \
  --resource-group rg-ai102-customskills \
  --location eastus \
  --sku Standard_LRS

# Create Azure AI Search service
az search service create \
  --name search-ai102-demo \
  --resource-group rg-ai102-customskills \
  --location eastus \
  --sku Basic
```

---

## Demo Flow (1 hour)

### Part 1: Introduction (10 minutes)

#### Opening Hook
> "Imagine you're a legal firm with thousands of contracts. Built-in AI can extract text and detect language, but what if you need to identify specific contract types, extract custom clauses, or calculate risk scores? That's where custom skills shine!"

#### Demo Scenario Setup
- **Company**: TechLegal Solutions
- **Challenge**: Process legal documents with custom business logic
- **Goal**: Build custom skills for contract analysis

#### Show Example Document
```text
CONTRACT AGREEMENT

This Software License Agreement ("Agreement") is entered into on March 15, 2024, 
between TechCorp Inc. ("Licensor") and ClientCorp Ltd. ("Licensee").

TERMS:
- License Duration: 3 years
- Payment: $50,000 annually
- Territory: North America
- Renewal: Automatic unless terminated

Contact: legal@techcorp.com, billing@clientcorp.com

CONFIDENTIALITY CLAUSE:
Both parties agree to maintain confidentiality of proprietary information...
```

### Part 2: Understanding Custom Skills Architecture (10 minutes)

#### Visual Explanation
```
Document → Built-in Skills → Custom Skills → Index → Search Results
    ↓            ↓               ↓            ↓         ↓
  PDF Text   Language      Contract      Enhanced    Better
  Content    Detection     Analysis      Metadata    Queries
```

#### Live Demo: REST API Contract
Show in Postman/VS Code:

**Input Example:**
```json
{
  "values": [
    {
      "recordId": "contract1",
      "data": {
        "text": "This Software License Agreement...",
        "languageCode": "en"
      }
    }
  ]
}
```

**Expected Output:**
```json
{
  "values": [
    {
      "recordId": "contract1",
      "data": {
        "contractType": "Software License",
        "duration": "3 years",
        "annualValue": 50000,
        "riskScore": 0.2
      },
      "errors": [],
      "warnings": []
    }
  ]
}
```

### Part 3: Building the Custom Skill Function (20 minutes)

#### Step 1: Create Azure Function (5 minutes)
```bash
# Create function app
az functionapp create \
  --resource-group rg-ai102-customskills \
  --consumption-plan-location eastus \
  --runtime dotnet \
  --functions-version 4 \
  --name func-contract-analyzer \
  --storage-account stai102demo
```

#### Step 2: Code the Contract Analyzer (10 minutes)
**Live Coding Session** - Create `ContractAnalyzer.cs`:

```csharp
[FunctionName("analyzecontract")]
public static async Task<IActionResult> Run(
    [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequest req,
    ILogger log)
{
    // Show live coding with explanation
    log.LogInformation("Contract analysis skill triggered");
    
    // Read and parse request
    string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
    var request = JsonConvert.DeserializeObject<CustomSkillRequest>(requestBody);
    
    var response = new CustomSkillResponse { Values = new List<CustomSkillResponseRecord>() };
    
    foreach (var record in request.Values)
    {
        var outputRecord = new CustomSkillResponseRecord
        {
            RecordId = record.RecordId,
            Data = new Dictionary<string, object>()
        };
        
        try
        {
            string text = record.Data["text"].ToString();
            
            // Contract analysis logic
            var analysis = AnalyzeContract(text);
            
            outputRecord.Data["contractType"] = analysis.Type;
            outputRecord.Data["duration"] = analysis.Duration;
            outputRecord.Data["annualValue"] = analysis.AnnualValue;
            outputRecord.Data["riskScore"] = analysis.RiskScore;
            outputRecord.Data["emails"] = analysis.Emails;
        }
        catch (Exception ex)
        {
            outputRecord.Errors.Add($"Analysis failed: {ex.Message}");
        }
        
        response.Values.Add(outputRecord);
    }
    
    return new OkObjectResult(response);
}

private static ContractAnalysis AnalyzeContract(string text)
{
    var analysis = new ContractAnalysis();
    
    // Contract type detection
    if (text.ToLower().Contains("license agreement"))
        analysis.Type = "Software License";
    else if (text.ToLower().Contains("service agreement"))
        analysis.Type = "Service Agreement";
    else
        analysis.Type = "General Contract";
    
    // Duration extraction
    var durationMatch = Regex.Match(text, @"(\d+)\s+(year|month)s?", RegexOptions.IgnoreCase);
    analysis.Duration = durationMatch.Success ? durationMatch.Value : "Not specified";
    
    // Value extraction
    var valueMatch = Regex.Match(text, @"\$(\d{1,3}(?:,\d{3})*)", RegexOptions.IgnoreCase);
    analysis.AnnualValue = valueMatch.Success ? int.Parse(valueMatch.Groups[1].Value.Replace(",", "")) : 0;
    
    // Risk assessment (simplified)
    analysis.RiskScore = CalculateRiskScore(text);
    
    // Email extraction
    analysis.Emails = ExtractEmails(text);
    
    return analysis;
}
```

#### Step 3: Test Function Locally (5 minutes)
```bash
# Start function locally
func start

# Test with curl
curl -X POST "http://localhost:7071/api/analyzecontract" \
  -H "Content-Type: application/json" \
  -d '{
    "values": [
      {
        "recordId": "test1",
        "data": {
          "text": "This Software License Agreement is for 3 years at $50,000 annually. Contact: legal@techcorp.com"
        }
      }
    ]
  }'
```

**Expected Response:**
```json
{
  "values": [
    {
      "recordId": "test1",
      "data": {
        "contractType": "Software License",
        "duration": "3 years",
        "annualValue": 50000,
        "riskScore": 0.2,
        "emails": ["legal@techcorp.com"]
      },
      "errors": [],
      "warnings": []
    }
  ]
}
```

### Part 4: Integration with Azure AI Search (15 minutes)

#### Step 1: Deploy Function to Azure (3 minutes)
```bash
# Deploy function
func azure functionapp publish func-contract-analyzer

# Get function URL
az functionapp function show \
  --name func-contract-analyzer \
  --resource-group rg-ai102-customskills \
  --function-name analyzecontract
```

#### Step 2: Create Enhanced Skillset (7 minutes)
**Live Demo in Azure Portal or REST API:**

```json
{
  "name": "legal-document-skillset",
  "description": "Skillset with custom contract analysis",
  "skills": [
    {
      "@odata.type": "#Microsoft.Skills.Text.LanguageDetectionSkill",
      "context": "/document",
      "inputs": [{"name": "text", "source": "/document/content"}],
      "outputs": [{"name": "languageCode", "targetName": "languageCode"}]
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.KeyPhraseExtractionSkill",
      "context": "/document",
      "inputs": [
        {"name": "text", "source": "/document/content"},
        {"name": "languageCode", "source": "/document/languageCode"}
      ],
      "outputs": [{"name": "keyPhrases", "targetName": "keyPhrases"}]
    },
    {
      "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
      "name": "contractAnalyzer",
      "description": "Analyze contract content",
      "uri": "https://func-contract-analyzer.azurewebsites.net/api/analyzecontract?code=your-function-key",
      "httpMethod": "POST",
      "timeout": "PT30S",
      "context": "/document",
      "batchSize": 5,
      "inputs": [
        {"name": "text", "source": "/document/content"}
      ],
      "outputs": [
        {"name": "contractType", "targetName": "contractType"},
        {"name": "duration", "targetName": "contractDuration"},
        {"name": "annualValue", "targetName": "annualValue"},
        {"name": "riskScore", "targetName": "riskScore"},
        {"name": "emails", "targetName": "contactEmails"}
      ]
    }
  ]
}
```

#### Step 3: Update Index Schema (3 minutes)
```json
{
  "fields": [
    {"name": "id", "type": "Edm.String", "key": true},
    {"name": "content", "type": "Edm.String", "searchable": true},
    {"name": "contractType", "type": "Edm.String", "searchable": true, "filterable": true, "facetable": true},
    {"name": "contractDuration", "type": "Edm.String", "filterable": true},
    {"name": "annualValue", "type": "Edm.Int32", "filterable": true, "sortable": true},
    {"name": "riskScore", "type": "Edm.Double", "filterable": true, "sortable": true},
    {"name": "contactEmails", "type": "Collection(Edm.String)", "searchable": true, "filterable": true}
  ]
}
```

#### Step 4: Run Indexer and Show Results (2 minutes)
```bash
# Trigger indexer run
curl -X POST "https://search-ai102-demo.search.windows.net/indexers/legal-indexer/run?api-version=2021-04-30-Preview" \
  -H "api-key: your-admin-key"

# Check indexer status
curl -X GET "https://search-ai102-demo.search.windows.net/indexers/legal-indexer/status?api-version=2021-04-30-Preview" \
  -H "api-key: your-admin-key"
```

### Part 5: Advanced Queries with Custom Fields (5 minutes)

#### Demo Queries
```bash
# Find high-value software licenses
curl -X GET "https://search-ai102-demo.search.windows.net/indexes/legal-index/docs?api-version=2021-04-30-Preview" \
  -H "api-key: your-query-key" \
  --data-urlencode "search=*" \
  --data-urlencode "\$filter=contractType eq 'Software License' and annualValue gt 30000" \
  --data-urlencode "\$orderby=annualValue desc"

# Find contracts with high risk scores
curl -X GET "https://search-ai102-demo.search.windows.net/indexes/legal-index/docs?api-version=2021-04-30-Preview" \
  -H "api-key: your-query-key" \
  --data-urlencode "search=*" \
  --data-urlencode "\$filter=riskScore gt 0.7" \
  --data-urlencode "facet=contractType"

# Search by contact email domain
curl -X GET "https://search-ai102-demo.search.windows.net/indexes/legal-index/docs?api-version=2021-04-30-Preview" \
  -H "api-key: your-query-key" \
  --data-urlencode "search=contactEmails:techcorp.com"
```

#### Show Results in Search Explorer
Navigate to Azure Portal → Search Service → Search Explorer and demonstrate:
1. Filter by contract type
2. Sort by annual value
3. Facet navigation
4. Full-text search combining built-in and custom fields

---

## Live Coding Session: Email Extraction Skill (Bonus Demo - 10 minutes)

### Quick Implementation
```csharp
[FunctionName("extractemails")]
public static async Task<IActionResult> ExtractEmails(
    [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequest req,
    ILogger log)
{
    // ... standard custom skill boilerplate ...
    
    foreach (var record in request.Values)
    {
        try
        {
            string text = record.Data["text"].ToString();
            
            // Email extraction with regex
            var emailPattern = @"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b";
            var matches = Regex.Matches(text, emailPattern);
            var emails = matches.Cast<Match>().Select(m => m.Value.ToLower()).Distinct().ToList();
            
            // Domain classification
            var personalDomains = new[] { "gmail.com", "yahoo.com", "hotmail.com", "outlook.com" };
            var businessEmails = emails.Where(e => !personalDomains.Contains(e.Split('@')[1])).ToList();
            var personalEmails = emails.Where(e => personalDomains.Contains(e.Split('@')[1])).ToList();
            
            outputRecord.Data["allEmails"] = emails;
            outputRecord.Data["businessEmails"] = businessEmails;
            outputRecord.Data["personalEmails"] = personalEmails;
            outputRecord.Data["emailCount"] = emails.Count;
            outputRecord.Data["hasBusinessContact"] = businessEmails.Any();
        }
        catch (Exception ex)
        {
            outputRecord.Errors.Add(ex.Message);
        }
    }
    
    // ... return response ...
}
```

---

## Q&A Preparation

### Common Questions & Answers

**Q: How do custom skills affect indexing performance?**
A: Custom skills add latency to the enrichment pipeline. Optimize by:
- Using async processing
- Implementing batching (batchSize parameter)
- Caching expensive operations
- Setting appropriate timeouts

**Q: Can custom skills call external APIs?**
A: Yes! Examples:
- Translation services
- Third-party ML models
- CRM systems for entity enrichment
- Compliance checking services

**Q: How do you handle errors in custom skills?**
A: Best practices:
- Return errors in the `errors` array
- Use warnings for non-critical issues
- Implement retry logic
- Log detailed error information
- Provide fallback values when possible

**Q: What are the cost implications?**
A: Consider:
- Azure Function execution time and memory
- External API calls
- Increased index size from additional fields
- Processing time impact on indexer runs

**Q: Can you modify existing skillsets?**
A: Yes, but:
- Existing data won't be re-enriched automatically
- Reset and re-run the indexer to apply changes
- Consider versioning your custom skills
- Test changes in a development environment first

### Demo Troubleshooting

**If Function deployment fails:**
- Check resource group permissions
- Verify storage account exists
- Try different function app name (globally unique)

**If custom skill returns errors:**
- Check function logs in Application Insights
- Verify input/output schema matches exactly
- Test function endpoint independently with Postman
- Check authentication (function keys)

**If indexer fails:**
- Review indexer execution history
- Check skillset definition for syntax errors
- Verify custom skill URI is accessible
- Monitor function app logs during indexer runs

---

## Wrap-up Points (5 minutes)

### Key Takeaways
1. **Custom skills extend Azure AI Search beyond built-in capabilities**
2. **Follow the input/output contract strictly**
3. **Design for performance and error handling**
4. **Test skills independently before integration**
5. **Monitor and log for troubleshooting**

### Next Steps for Attendees
1. Try the hands-on exercise
2. Explore Azure ML integration
3. Build skills for your specific domain
4. Consider performance optimization techniques
5. Join the Azure AI Search community

### Resources
- GitHub repo with complete code samples
- Azure AI Search documentation
- Custom skills best practices guide
- Community forums and support channels

---

## Post-Demo Cleanup

```bash
# Optional: Clean up resources to avoid charges
az group delete --name rg-ai102-customskills --yes --no-wait
```

---

## Technical Notes

### Function App Settings
```bash
# Required app settings
az functionapp config appsettings set \
  --name func-contract-analyzer \
  --resource-group rg-ai102-customskills \
  --settings \
    "FUNCTIONS_WORKER_RUNTIME=dotnet" \
    "AzureWebJobsStorage=your-storage-connection-string"
```

### Security Considerations
- Use managed identity when possible
- Rotate function keys regularly
- Validate all inputs in custom skills
- Log security events appropriately
- Consider rate limiting for public endpoints

### Performance Tips
- Implement connection pooling
- Use async/await consistently
- Cache expensive computations
- Batch process when possible
- Monitor memory usage in functions
