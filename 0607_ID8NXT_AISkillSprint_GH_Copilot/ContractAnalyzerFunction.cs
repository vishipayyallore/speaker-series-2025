using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace ContractAnalyzer
{
    public static class ContractAnalysisSkill
    {
        [FunctionName("analyzecontract")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("Contract analysis custom skill triggered");

            try
            {
                // Read and parse the request
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
                        string text = record.Data.ContainsKey("text") ? record.Data["text"].ToString() : "";
                        
                        // Analyze the contract content
                        var analysis = AnalyzeContract(text);
                        
                        // Add results to output
                        outputRecord.Data["contractType"] = analysis.Type;
                        outputRecord.Data["duration"] = analysis.Duration;
                        outputRecord.Data["annualValue"] = analysis.AnnualValue;
                        outputRecord.Data["riskScore"] = analysis.RiskScore;
                        outputRecord.Data["contactEmails"] = analysis.Emails;
                        outputRecord.Data["keyTerms"] = analysis.KeyTerms;
                        outputRecord.Data["hasConfidentialityClause"] = analysis.HasConfidentialityClause;
                        outputRecord.Data["paymentTerms"] = analysis.PaymentTerms;
                    }
                    catch (Exception ex)
                    {
                        outputRecord.Errors.Add($"Analysis failed: {ex.Message}");
                        log.LogError(ex, "Error processing record {RecordId}", record.RecordId);
                    }

                    response.Values.Add(outputRecord);
                }

                return new OkObjectResult(response);
            }
            catch (Exception ex)
            {
                log.LogError(ex, "Error processing custom skill request");
                return new StatusCodeResult(500);
            }
        }

        private static ContractAnalysis AnalyzeContract(string text)
        {
            var analysis = new ContractAnalysis();
            text = text.ToLower();

            // Contract type detection
            if (text.Contains("license agreement") || text.Contains("software license"))
                analysis.Type = "Software License";
            else if (text.Contains("service agreement") || text.Contains("professional services"))
                analysis.Type = "Service Agreement";
            else if (text.Contains("consulting agreement"))
                analysis.Type = "Consulting Agreement";
            else if (text.Contains("employment agreement"))
                analysis.Type = "Employment Agreement";
            else
                analysis.Type = "General Contract";

            // Duration extraction
            var durationPatterns = new[]
            {
                @"(\d+)\s+(year|years)",
                @"(\d+)\s+(month|months)",
                @"duration[:\s]+(\d+)\s+(year|month)",
                @"period[:\s]+(\d+)\s+(year|month)"
            };

            foreach (var pattern in durationPatterns)
            {
                var match = Regex.Match(text, pattern, RegexOptions.IgnoreCase);
                if (match.Success)
                {
                    analysis.Duration = match.Value;
                    break;
                }
            }
            
            if (string.IsNullOrEmpty(analysis.Duration))
                analysis.Duration = "Not specified";

            // Value extraction (looking for dollar amounts)
            var valuePatterns = new[]
            {
                @"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",
                @"(\d{1,3}(?:,\d{3})*)\s*dollars?",
                @"value[:\s]+\$?(\d{1,3}(?:,\d{3})*)"
            };

            foreach (var pattern in valuePatterns)
            {
                var match = Regex.Match(text, pattern, RegexOptions.IgnoreCase);
                if (match.Success)
                {
                    string valueStr = match.Groups[1].Value.Replace(",", "");
                    if (int.TryParse(valueStr, out int value))
                    {
                        analysis.AnnualValue = value;
                        break;
                    }
                }
            }

            // Email extraction
            analysis.Emails = ExtractEmails(text);

            // Key terms extraction
            analysis.KeyTerms = ExtractKeyTerms(text);

            // Risk assessment (simplified scoring)
            analysis.RiskScore = CalculateRiskScore(text, analysis);

            // Check for confidentiality clause
            analysis.HasConfidentialityClause = text.Contains("confidential") || 
                                               text.Contains("non-disclosure") || 
                                               text.Contains("proprietary");

            // Payment terms detection
            if (text.Contains("net 30"))
                analysis.PaymentTerms = "Net 30 days";
            else if (text.Contains("net 60"))
                analysis.PaymentTerms = "Net 60 days";
            else if (text.Contains("monthly"))
                analysis.PaymentTerms = "Monthly";
            else if (text.Contains("annual"))
                analysis.PaymentTerms = "Annual";
            else
                analysis.PaymentTerms = "Not specified";

            return analysis;
        }

        private static List<string> ExtractEmails(string text)
        {
            var emailPattern = @"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b";
            var matches = Regex.Matches(text, emailPattern);
            return matches.Cast<Match>()
                         .Select(m => m.Value.ToLower())
                         .Distinct()
                         .ToList();
        }

        private static List<string> ExtractKeyTerms(string text)
        {
            var keyTermPatterns = new[]
            {
                "liability",
                "termination",
                "renewal",
                "intellectual property",
                "confidentiality",
                "payment terms",
                "deliverables",
                "warranty",
                "indemnification",
                "force majeure"
            };

            return keyTermPatterns.Where(term => text.Contains(term))
                                 .ToList();
        }

        private static double CalculateRiskScore(string text, ContractAnalysis analysis)
        {
            double riskScore = 0.0;

            // Base risk factors
            if (analysis.AnnualValue > 100000) riskScore += 0.2;
            if (analysis.Duration.Contains("year") && 
                Regex.Match(analysis.Duration, @"\d+").Success &&
                int.Parse(Regex.Match(analysis.Duration, @"\d+").Value) > 2) 
                riskScore += 0.2;

            // Risk indicators in text
            var riskIndicators = new[]
            {
                "penalty", "liquidated damages", "unlimited liability",
                "personal guarantee", "non-compete", "exclusive"
            };

            foreach (var indicator in riskIndicators)
            {
                if (text.Contains(indicator))
                    riskScore += 0.15;
            }

            // Protective clauses reduce risk
            var protectiveTerms = new[]
            {
                "limitation of liability", "warranty disclaimer",
                "force majeure", "termination for convenience"
            };

            foreach (var term in protectiveTerms)
            {
                if (text.Contains(term))
                    riskScore -= 0.1;
            }

            return Math.Min(Math.Max(riskScore, 0.0), 1.0); // Clamp between 0 and 1
        }
    }

    // Data Models
    public class CustomSkillRequest
    {
        public List<CustomSkillRequestRecord> Values { get; set; }
    }

    public class CustomSkillRequestRecord
    {
        public string RecordId { get; set; }
        public Dictionary<string, object> Data { get; set; }
    }

    public class CustomSkillResponse
    {
        public List<CustomSkillResponseRecord> Values { get; set; }
    }

    public class CustomSkillResponseRecord
    {
        public string RecordId { get; set; }
        public Dictionary<string, object> Data { get; set; } = new Dictionary<string, object>();
        public List<string> Errors { get; set; } = new List<string>();
        public List<string> Warnings { get; set; } = new List<string>();
    }

    public class ContractAnalysis
    {
        public string Type { get; set; } = "Unknown";
        public string Duration { get; set; } = "Not specified";
        public int AnnualValue { get; set; } = 0;
        public double RiskScore { get; set; } = 0.0;
        public List<string> Emails { get; set; } = new List<string>();
        public List<string> KeyTerms { get; set; } = new List<string>();
        public bool HasConfidentialityClause { get; set; } = false;
        public string PaymentTerms { get; set; } = "Not specified";
    }
}
