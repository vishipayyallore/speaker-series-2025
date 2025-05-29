# Production Deployment Guide

This guide helps you deploy the Knowledge Worker Agent to production on Azure.

## 🏗️ Architecture Overview

```
Internet → Azure Front Door → Container Apps → Azure Services
                                    ↓
                              Azure Functions
                                    ↓
                        Azure OpenAI + AI Search + Storage
```

## 📋 Pre-Production Checklist

### Security
- [ ] Enable Azure Key Vault for secrets management
- [ ] Configure managed identities (no API keys in code)
- [ ] Set up Azure Front Door with Web Application Firewall
- [ ] Enable Azure Monitor and Application Insights
- [ ] Configure HTTPS/TLS certificates
- [ ] Set up proper RBAC (Role-Based Access Control)

### Scalability
- [ ] Use Azure Container Apps for auto-scaling web interface
- [ ] Configure Azure Functions with appropriate hosting plan
- [ ] Set up Azure AI Search with sufficient replicas
- [ ] Enable Azure OpenAI rate limiting and quotas

### Monitoring
- [ ] Configure Application Insights
- [ ] Set up Azure Monitor alerts
- [ ] Enable logging and tracing
- [ ] Create dashboards for key metrics

## 🚀 Deployment Steps

### 1. Infrastructure Setup

```bash
# Deploy infrastructure using Bicep/ARM templates
az deployment group create \
    --resource-group myapp-prod \
    --template-file infrastructure/main.bicep \
    --parameters environment=prod
```

### 2. Application Deployment

#### Container Apps (Web Interface)
```bash
# Build and push container
docker build -t myregistry.azurecr.io/knowledge-worker:latest .
docker push myregistry.azurecr.io/knowledge-worker:latest

# Deploy to Container Apps
az containerapp update \
    --name knowledge-worker \
    --resource-group myapp-prod \
    --image myregistry.azurecr.io/knowledge-worker:latest
```

#### Azure Functions (Tools)
```bash
# Deploy functions
cd azure-functions
func azure functionapp publish myapp-functions-prod
```

### 3. Security Configuration

#### Key Vault Setup
```bash
# Create Key Vault
az keyvault create \
    --name myapp-keyvault-prod \
    --resource-group myapp-prod \
    --location eastus

# Store secrets
az keyvault secret set --vault-name myapp-keyvault-prod --name "OpenAI-ApiKey" --value "your-key"
az keyvault secret set --vault-name myapp-keyvault-prod --name "Search-ApiKey" --value "your-key"
```

#### Managed Identity
```python
# Update code to use managed identity
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url="https://myapp-keyvault-prod.vault.azure.net/", credential=credential)

openai_key = secret_client.get_secret("OpenAI-ApiKey").value
```

## 📊 Production Configuration

### Environment Variables (.env.prod)
```bash
# Use managed identity instead of API keys
AZURE_OPENAI_ENDPOINT=https://myapp-openai-prod.openai.azure.com/
AZURE_SEARCH_ENDPOINT=https://myapp-search-prod.search.windows.net
AZURE_STORAGE_ACCOUNT_NAME=myappstorprod
AZURE_FUNCTION_APP_URL=https://myapp-functions-prod.azurewebsites.net

# Production settings
ENVIRONMENT=production
LOG_LEVEL=INFO
ENABLE_TELEMETRY=true
MAX_DOCUMENT_SIZE=10485760  # 10MB
MAX_DOCUMENTS_PER_USER=100
RATE_LIMIT_PER_MINUTE=60
```

### Application Settings
```python
# config/production.py
import os

class ProductionConfig:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Azure Services
    AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
    
    # Performance
    MAX_WORKERS = 4
    TIMEOUT_SECONDS = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = 60
    
    # Monitoring
    APPLICATIONINSIGHTS_CONNECTION_STRING = os.environ.get('APPLICATIONINSIGHTS_CONNECTION_STRING')
```

## 🔍 Monitoring and Observability

### Application Insights Integration
```python
# monitoring.py
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

# Configure Azure Monitor
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=os.environ.get('APPLICATIONINSIGHTS_CONNECTION_STRING')))

# Custom telemetry
from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module

# Track custom metrics
request_measure = measure_module.MeasureFloat("requests", "number of requests", "1")
request_view = view_module.View("request_view", "number of requests", [], request_measure, aggregation_module.CountAggregation())

def track_request():
    mmap = stats_module.stats.stats_recorder.new_measurement_map()
    mmap.measure_float_put(request_measure, 1)
    mmap.record()
```

### Health Checks
```python
# health.py
from fastapi import APIRouter
from azure.core.exceptions import ServiceRequestError

router = APIRouter()

@router.get("/health")
async def health_check():
    checks = {
        "status": "healthy",
        "services": {}
    }
    
    # Check Azure OpenAI
    try:
        # Test connection
        checks["services"]["openai"] = "healthy"
    except Exception:
        checks["services"]["openai"] = "unhealthy"
        checks["status"] = "degraded"
    
    # Check Azure Search
    try:
        # Test connection
        checks["services"]["search"] = "healthy"
    except Exception:
        checks["services"]["search"] = "unhealthy"
        checks["status"] = "degraded"
    
    return checks
```

## 🛡️ Security Best Practices

### 1. API Security
```python
# security.py
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
import jwt

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Apply to routes
@app.post("/chat")
async def chat_endpoint(request: ChatRequest, user: dict = Depends(verify_token)):
    # Handle authenticated request
    pass
```

### 2. Rate Limiting
```python
# rate_limiting.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/chat")
@limiter.limit("10/minute")
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    # Rate-limited endpoint
    pass
```

### 3. Input Validation
```python
# validation.py
from pydantic import BaseModel, validator, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_id: Optional[str] = Field(None, regex=r'^[a-zA-Z0-9-]+$')
    
    @validator('message')
    def validate_message(cls, v):
        # Check for malicious content
        forbidden_patterns = ['<script', 'javascript:', 'data:']
        for pattern in forbidden_patterns:
            if pattern.lower() in v.lower():
                raise ValueError('Invalid message content')
        return v
```

## 📈 Performance Optimization

### Caching Strategy
```python
# caching.py
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='myapp-cache-prod.redis.cache.windows.net', port=6380, ssl=True)

def cache_response(expiry=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expiry, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_response(expiry=600)
async def search_documents(query: str):
    # Expensive search operation
    pass
```

### Database Connection Pooling
```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

## 🔄 CI/CD Pipeline

### GitHub Actions (.github/workflows/deploy.yml)
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Run Tests
      run: |
        pip install -r requirements.txt
        pytest tests/
    
    - name: Build Docker Image
      run: |
        docker build -t ${{ secrets.REGISTRY_URL }}/knowledge-worker:${{ github.sha }} .
        docker push ${{ secrets.REGISTRY_URL }}/knowledge-worker:${{ github.sha }}
    
    - name: Deploy to Container Apps
      uses: azure/container-apps-deploy-action@v1
      with:
        resource-group: myapp-prod
        container-app-name: knowledge-worker
        image: ${{ secrets.REGISTRY_URL }}/knowledge-worker:${{ github.sha }}
    
    - name: Deploy Functions
      run: |
        cd azure-functions
        func azure functionapp publish myapp-functions-prod
```

## 💰 Cost Optimization

### Resource Sizing Guidelines
- **Azure OpenAI**: Start with Standard deployment, monitor usage
- **Azure AI Search**: Basic tier for development, Standard for production
- **Container Apps**: Enable auto-scaling with min 0, max 10 replicas
- **Functions**: Consumption plan for variable workloads

### Monitoring Costs
```bash
# Set up budget alerts
az consumption budget create \
    --budget-name "KnowledgeWorker-Monthly" \
    --amount 500 \
    --resource-group myapp-prod \
    --time-grain Monthly
```

## 🚨 Disaster Recovery

### Backup Strategy
- **Azure AI Search**: Export index definition and data
- **Azure Storage**: Enable geo-redundant storage
- **Application Code**: Store in Git with proper branching strategy

### Recovery Procedures
1. **Service Outage**: Multi-region deployment with traffic manager
2. **Data Loss**: Automated backups with point-in-time recovery
3. **Security Incident**: Incident response plan with key rotation

## 📚 Additional Resources

- [Azure Well-Architected Framework](https://docs.microsoft.com/en-us/azure/architecture/framework/)
- [Azure OpenAI Service Best Practices](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/concepts/best-practices)
- [Azure Container Apps Documentation](https://docs.microsoft.com/en-us/azure/container-apps/)
- [Azure Monitor Best Practices](https://docs.microsoft.com/en-us/azure/azure-monitor/best-practices)
