# Test Azure Functions - PowerShell Script
# Run this from the demo directory

# Function URLs and Authentication
$baseUrl = "https://rg-agentic-ai-dev-001-functions.azurewebsites.net/api"
$functionKey = "YourFunctionKeyHere"  # Replace with your actual function key

Write-Host "🧪 Testing Azure Functions with Authentication..." -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

# Test 1: Create Task Function
Write-Host "`n📋 Testing Create Task Function..." -ForegroundColor Yellow
$createTaskPayload = @{
    title       = "Review AI Strategy Document"
    description = "Analyze the uploaded AI strategy document and identify key action items"
    priority    = "high"
    due_date    = "2025-06-15"
    assigned_to = "project-manager@company.com"
} | ConvertTo-Json

try {
    $response1 = Invoke-RestMethod -Uri "$baseUrl/create_task?code=$functionKey" -Method POST -Body $createTaskPayload -ContentType "application/json"
    Write-Host "✅ Success:" -ForegroundColor Green
    $response1 | ConvertTo-Json -Depth 3 | Write-Host
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Send Email Function
Write-Host "`n📧 Testing Send Email Function..." -ForegroundColor Yellow
$sendEmailPayload = @{
    to_email   = "john.doe@example.com"
    subject    = "AI Strategy Analysis Complete"
    body       = "The AI strategy document has been analyzed. Please find the key recommendations attached."
    from_email = "ai-agent@company.com"
} | ConvertTo-Json

try {
    $response2 = Invoke-RestMethod -Uri "$baseUrl/send_email?code=$functionKey" -Method POST -Body $sendEmailPayload -ContentType "application/json"
    Write-Host "✅ Success:" -ForegroundColor Green
    $response2 | ConvertTo-Json -Depth 3 | Write-Host
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Generate Report Function
Write-Host "`n📊 Testing Generate Report Function..." -ForegroundColor Yellow
$generateReportPayload = @{
    report_type    = "analysis_summary"
    title          = "AI Strategy Analysis Report"
    content        = "Based on the analyzed documents, here are the key findings and recommendations for implementing AI in our startup."
    format         = "pdf"
    include_charts = $true
} | ConvertTo-Json

try {
    $response3 = Invoke-RestMethod -Uri "$baseUrl/generate_report?code=$functionKey" -Method POST -Body $generateReportPayload -ContentType "application/json"
    Write-Host "✅ Success:" -ForegroundColor Green
    $response3 | ConvertTo-Json -Depth 3 | Write-Host
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 Function testing complete!" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray
