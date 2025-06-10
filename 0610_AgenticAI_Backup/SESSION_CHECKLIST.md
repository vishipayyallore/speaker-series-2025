# Session Delivery Checklist: AI-102 S27 Custom Skills
## Date: 27-May-2025 at 03:30 PM IST

---

## 📋 Pre-Session Preparation (Day Before)

### Technical Setup
- [ ] **Azure Resources**: Run `setup-demo-environment.ps1` to provision all resources
- [ ] **Function Deployment**: Deploy `ContractAnalyzerFunction.cs` to Azure Functions
- [ ] **Test Function**: Verify custom skill endpoint responds correctly
- [ ] **Sample Data**: Confirm all sample documents are uploaded to blob storage
- [ ] **Credentials**: Save all connection strings and keys in secure location

### Presentation Setup
- [ ] **Slides**: Prepare architecture diagrams for custom skills flow
- [ ] **VS Code**: Open demo project with all files ready
- [ ] **Browser Tabs**: 
  - Azure Portal (Search Service, Function App, Storage)
  - Postman/REST Client for API testing
  - Documentation tabs for reference
- [ ] **Screen Recording**: Test screen sharing and recording setup

---

## ⏱️ Session Timing Guide (1 hour 6 minutes)

### Opening (5 minutes) - 3:30-3:35 PM
- [ ] Welcome and introductions
- [ ] Session agenda overview
- [ ] Prerequisite check with audience

### Part 1: Introduction (10 minutes) - 3:35-3:45 PM
- [ ] Business scenario presentation (TechLegal Solutions)
- [ ] Show sample contract document
- [ ] Explain limitations of built-in skills
- [ ] **Demo**: Show basic vs enhanced search results

### Part 2: Architecture Deep Dive (10 minutes) - 3:45-3:55 PM
- [ ] Custom skills pipeline diagram
- [ ] REST API contract explanation
- [ ] Input/output schema walkthrough
- [ ] **Demo**: Show API request/response in Postman

### Part 3: Live Coding (25 minutes) - 3:55-4:20 PM
- [ ] **5 min**: Function structure and dependencies
- [ ] **10 min**: Core analysis logic implementation
- [ ] **5 min**: Error handling and logging
- [ ] **5 min**: Test function locally with sample data

### Part 4: Integration Demo (10 minutes) - 4:20-4:30 PM
- [ ] Deploy function to Azure
- [ ] Create/update skillset with custom skill
- [ ] Run indexer and show enriched documents
- [ ] **Demo**: Enhanced search queries

### Part 5: Advanced Topics (5 minutes) - 4:30-4:35 PM
- [ ] ML model integration patterns
- [ ] Scaling considerations
- [ ] Best practices overview

### Q&A Session (6 minutes) - 4:35-4:41 PM
- [ ] Common troubleshooting scenarios
- [ ] Performance optimization tips
- [ ] Production deployment considerations

---

## 🛠️ Emergency Backup Plans

### If Azure Services Fail
- [ ] **Backup Demo**: Pre-recorded video of working demo
- [ ] **Local Testing**: Run function locally with ngrok for external access
- [ ] **Screenshots**: Prepared images of expected results

### If Code Compilation Issues
- [ ] **Pre-built Function**: Have deployed function ready as backup
- [ ] **Code Snippets**: Key code sections in separate files for easy copy-paste

### If Network Issues
- [ ] **Offline Slides**: Full presentation downloaded locally
- [ ] **Local Documentation**: Key Azure docs saved offline

---

## 📚 Key Talking Points

### Why Custom Skills Matter
> "Built-in cognitive skills are powerful, but every business has unique requirements. Custom skills let you integrate your domain expertise directly into the AI enrichment pipeline."

### Architecture Benefits
> "Custom skills are just HTTP endpoints. This means you can use any technology stack, integrate with existing systems, and scale independently."

### Real-World Applications
- Legal document classification
- Medical record analysis
- Financial document processing
- Custom entity extraction
- Compliance checking

---

## 🎯 Success Metrics

### Audience Engagement
- [ ] Questions during Q&A
- [ ] Follow-up requests for code/resources
- [ ] Feedback on practical applicability

### Technical Demonstration
- [ ] Successful live function deployment
- [ ] Working end-to-end search pipeline
- [ ] Clear before/after search results comparison

### Knowledge Transfer
- [ ] Audience understands custom skill architecture
- [ ] Clear path from demo to production implementation
- [ ] Awareness of best practices and pitfalls

---

## 📞 Emergency Contacts

- **Microsoft Technical Support**: [Support Portal]
- **Azure Documentation**: https://docs.microsoft.com/azure/search/cognitive-search-custom-skill-interface
- **Sample Code Repository**: https://github.com/Azure-Samples/azure-search-power-skills

---

## 🔗 Post-Session Resources

### Share with Audience
- [ ] Complete demo code repository
- [ ] Setup script for their own testing
- [ ] Recommended learning paths
- [ ] Advanced samples and patterns

### Follow-up Actions
- [ ] Upload recording to YouTube
- [ ] Share slide deck
- [ ] Post summary on LinkedIn/blog
- [ ] Update documentation based on feedback

---

**Remember**: The goal is to show practical value and empower the audience to implement custom skills in their own projects. Focus on the business problem first, then the technical solution.
