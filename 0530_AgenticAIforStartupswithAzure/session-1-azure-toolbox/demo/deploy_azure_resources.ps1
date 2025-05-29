# Deploy Azure Resources for Knowledge Worker Agent Demo
# This script creates the necessary Azure resources for the demo

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$true)]
    [string]$Location = "East US",
    
    [Parameter(Mandatory=$true)]
    [string]$SubscriptionId
)

# Set the subscription
Write-Host "Setting subscription to $SubscriptionId..." -ForegroundColor Green
az account set --subscription $SubscriptionId

# Create resource group
Write-Host "Creating resource group $ResourceGroupName..." -ForegroundColor Green
az group create --name $ResourceGroupName --location $Location

# Create Azure OpenAI Service
$openaiServiceName = "$ResourceGroupName-openai"
Write-Host "Creating Azure OpenAI Service: $openaiServiceName..." -ForegroundColor Green
az cognitiveservices account create `
    --name $openaiServiceName `
    --resource-group $ResourceGroupName `
    --location $Location `
    --kind OpenAI `
    --sku S0 `
    --custom-domain $openaiServiceName

# Deploy GPT-4o model
Write-Host "Deploying GPT-4o model..." -ForegroundColor Green
az cognitiveservices account deployment create `
    --name $openaiServiceName `
    --resource-group $ResourceGroupName `
    --deployment-name "gpt-4o" `
    --model-name "gpt-4o" `
    --model-version "2024-08-06" `
    --model-format OpenAI `
    --sku-capacity 10 `
    --sku-name "Standard"

# Deploy text embedding model
Write-Host "Deploying text embedding model..." -ForegroundColor Green
az cognitiveservices account deployment create `
    --name $openaiServiceName `
    --resource-group $ResourceGroupName `
    --deployment-name "text-embedding-3-large" `
    --model-name "text-embedding-3-large" `
    --model-version "1" `
    --model-format OpenAI `
    --sku-capacity 10 `
    --sku-name "Standard"

# Create Azure AI Search Service
$searchServiceName = "$ResourceGroupName-search"
Write-Host "Creating Azure AI Search Service: $searchServiceName..." -ForegroundColor Green
az search service create `
    --name $searchServiceName `
    --resource-group $ResourceGroupName `
    --location $Location `
    --sku Standard `
    --partition-count 1 `
    --replica-count 1

# Create Storage Account
$storageAccountName = ($ResourceGroupName -replace '[^a-zA-Z0-9]', '').ToLower() + "storage"
Write-Host "Creating Storage Account: $storageAccountName..." -ForegroundColor Green
az storage account create `
    --name $storageAccountName `
    --resource-group $ResourceGroupName `
    --location $Location `
    --sku Standard_LRS `
    --kind StorageV2

# Create blob container
Write-Host "Creating blob container..." -ForegroundColor Green
az storage container create `
    --name "documents" `
    --account-name $storageAccountName

# Create Function App
$functionAppName = "$ResourceGroupName-functions"
Write-Host "Creating Function App: $functionAppName..." -ForegroundColor Green
# Convert location to lowercase for Function App consumption plan
$consumptionLocation = $Location.ToLower().Replace(" ", "")
az functionapp create `
    --resource-group $ResourceGroupName `
    --consumption-plan-location $consumptionLocation `
    --runtime python `
    --runtime-version 3.11 `
    --functions-version 4 `
    --name $functionAppName `
    --storage-account $storageAccountName `
    --os-type Linux

# Get connection information
Write-Host "`n=== RESOURCE INFORMATION ===" -ForegroundColor Yellow

# OpenAI Service
$openaiEndpoint = az cognitiveservices account show --name $openaiServiceName --resource-group $ResourceGroupName --query "properties.endpoint" --output tsv
$openaiKey = az cognitiveservices account keys list --name $openaiServiceName --resource-group $ResourceGroupName --query "key1" --output tsv

# Search Service
$searchEndpoint = "https://$searchServiceName.search.windows.net"
$searchKey = az search admin-key show --service-name $searchServiceName --resource-group $ResourceGroupName --query "primaryKey" --output tsv

# Storage Account
$storageKey = az storage account keys list --account-name $storageAccountName --resource-group $ResourceGroupName --query "[0].value" --output tsv

# Function App
$functionAppUrl = "https://$functionAppName.azurewebsites.net"

Write-Host "`nUpdate your .env file with these values:" -ForegroundColor Green
Write-Host "AZURE_OPENAI_ENDPOINT=$openaiEndpoint"
Write-Host "AZURE_OPENAI_API_KEY=$openaiKey"
Write-Host "AZURE_SEARCH_ENDPOINT=$searchEndpoint"
Write-Host "AZURE_SEARCH_API_KEY=$searchKey"
Write-Host "AZURE_STORAGE_ACCOUNT_NAME=$storageAccountName"
Write-Host "AZURE_STORAGE_ACCOUNT_KEY=$storageKey"
Write-Host "AZURE_FUNCTION_APP_URL=$functionAppUrl"

Write-Host "`nDeployment completed successfully!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update your .env file with the values above"
Write-Host "2. Deploy the Azure Functions using 'func azure functionapp publish $functionAppName'"
Write-Host "3. Run the demo application"
