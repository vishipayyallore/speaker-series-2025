# Azure AI-102 S27 Demo Setup Script
# Custom Skills in Azure AI Search Demo Resources

param(
    [Parameter(Mandatory=$true)]
    [string]$SubscriptionId,
    
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroupName = "rg-ai102-customskills-demo",
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "eastus",
    
    [Parameter(Mandatory=$false)]
    [string]$SearchServiceName = "search-ai102-s27-demo",
    
    [Parameter(Mandatory=$false)]
    [string]$StorageAccountName = "stai102s27demo",
    
    [Parameter(Mandatory=$false)]
    [string]$FunctionAppName = "func-ai102-contract-analyzer"
)

Write-Host "🚀 Setting up Azure AI Search Custom Skills Demo Environment" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Login and set subscription
Write-Host "📋 Setting up Azure subscription..." -ForegroundColor Yellow
try {
    az account set --subscription $SubscriptionId
    $currentSub = az account show --query name -o tsv
    Write-Host "✅ Connected to subscription: $currentSub" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to set subscription. Please run 'az login' first." -ForegroundColor Red
    exit 1
}

# Create Resource Group
Write-Host "📁 Creating resource group: $ResourceGroupName..." -ForegroundColor Yellow
az group create --name $ResourceGroupName --location $Location --output table

# Create Storage Account for documents
Write-Host "💾 Creating storage account: $StorageAccountName..." -ForegroundColor Yellow
az storage account create `
    --name $StorageAccountName `
    --resource-group $ResourceGroupName `
    --location $Location `
    --sku Standard_LRS `
    --output table

# Create blob container for sample documents
Write-Host "📄 Creating blob container for sample documents..." -ForegroundColor Yellow
$storageKey = az storage account keys list --resource-group $ResourceGroupName --account-name $StorageAccountName --query "[0].value" -o tsv
az storage container create `
    --name "legal-documents" `
    --account-name $StorageAccountName `
    --account-key $storageKey `
    --public-access off

# Upload sample documents
Write-Host "📤 Uploading sample contract documents..." -ForegroundColor Yellow
$dataFolder = ".\Data"
if (Test-Path $dataFolder) {
    Get-ChildItem "$dataFolder\*.txt" | ForEach-Object {
        Write-Host "   Uploading: $($_.Name)" -ForegroundColor Cyan
        az storage blob upload `
            --account-name $StorageAccountName `
            --account-key $storageKey `
            --container-name "legal-documents" `
            --name $_.Name `
            --file $_.FullName `
            --overwrite
    }
} else {
    Write-Host "⚠️  Data folder not found. Please run this script from the session folder." -ForegroundColor Yellow
}

# Create Azure AI Search Service
Write-Host "🔍 Creating Azure AI Search service: $SearchServiceName..." -ForegroundColor Yellow
az search service create `
    --name $SearchServiceName `
    --resource-group $ResourceGroupName `
    --location $Location `
    --sku Basic `
    --output table

# Create Azure Function App
Write-Host "⚡ Creating Azure Function App: $FunctionAppName..." -ForegroundColor Yellow
az functionapp create `
    --resource-group $ResourceGroupName `
    --consumption-plan-location $Location `
    --runtime dotnet `
    --functions-version 4 `
    --name $FunctionAppName `
    --storage-account $StorageAccountName `
    --output table

# Get connection information
Write-Host "📊 Retrieving connection information..." -ForegroundColor Yellow

$searchAdminKey = az search admin-key show --resource-group $ResourceGroupName --service-name $SearchServiceName --query primaryKey -o tsv
$searchQueryKey = az search query-key list --resource-group $ResourceGroupName --service-name $SearchServiceName --query "[0].key" -o tsv
$storageConnectionString = az storage account show-connection-string --resource-group $ResourceGroupName --name $StorageAccountName --query connectionString -o tsv
$functionAppUrl = az functionapp show --resource-group $ResourceGroupName --name $FunctionAppName --query defaultHostName -o tsv

Write-Host "`n🎯 Demo Environment Setup Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "📋 Connection Details:" -ForegroundColor Cyan
Write-Host "   Resource Group: $ResourceGroupName" -ForegroundColor White
Write-Host "   Search Service: https://$SearchServiceName.search.windows.net" -ForegroundColor White
Write-Host "   Search Admin Key: $searchAdminKey" -ForegroundColor White  
Write-Host "   Search Query Key: $searchQueryKey" -ForegroundColor White
Write-Host "   Storage Account: $StorageAccountName" -ForegroundColor White
Write-Host "   Function App: https://$functionAppUrl" -ForegroundColor White
Write-Host "`n💡 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Deploy your custom skill function to: $FunctionAppName" -ForegroundColor White
Write-Host "   2. Create search index and skillset using the provided examples" -ForegroundColor White
Write-Host "   3. Test the enrichment pipeline with sample documents" -ForegroundColor White

# Save configuration for easy reference
$config = @{
    ResourceGroup = $ResourceGroupName
    SearchService = $SearchServiceName
    SearchEndpoint = "https://$SearchServiceName.search.windows.net"
    SearchAdminKey = $searchAdminKey
    SearchQueryKey = $searchQueryKey
    StorageAccount = $StorageAccountName
    StorageConnectionString = $storageConnectionString
    FunctionApp = $FunctionAppName
    FunctionAppUrl = "https://$functionAppUrl"
    Location = $Location
}

$config | ConvertTo-Json -Depth 2 | Out-File "demo-config.json" -Encoding UTF8
Write-Host "`n💾 Configuration saved to: demo-config.json" -ForegroundColor Green

Write-Host "`n🧹 Cleanup Command (run after demo):" -ForegroundColor Red
Write-Host "   az group delete --name $ResourceGroupName --yes --no-wait" -ForegroundColor White
