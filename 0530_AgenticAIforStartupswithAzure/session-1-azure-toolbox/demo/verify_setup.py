#!/usr/bin/env python3
"""
Setup Verification Script for Azure Toolbox Demo
Validates that all Azure services are properly configured and accessible.
"""

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
import requests

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_status(service, status, message=""):
    color = Colors.GREEN if status else Colors.RED
    status_text = "✅ PASS" if status else "❌ FAIL"
    print(f"{color}{status_text}{Colors.ENDC} {Colors.BOLD}{service}{Colors.ENDC}: {message}")

def verify_azure_openai():
    """Verify Azure OpenAI Service connectivity and models."""
    print(f"\n{Colors.BLUE}🧠 Verifying Azure OpenAI Service...{Colors.ENDC}")
    
    try:
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
        embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
        
        if not all([endpoint, api_key]):
            print_status("Azure OpenAI", False, "Missing endpoint or API key in environment")
            return False
        
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version="2024-06-01"
        )
        
        # Test chat completion
        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": "Hello, this is a test."}],
            max_tokens=10
        )
        print_status("GPT Model", True, f"Deployment '{deployment}' is accessible")
        
        # Test embeddings
        embedding_response = client.embeddings.create(
            model=embedding_deployment,
            input="Test embedding"
        )
        print_status("Embedding Model", True, f"Deployment '{embedding_deployment}' is accessible")
        
        return True
        
    except Exception as e:
        print_status("Azure OpenAI", False, f"Connection failed: {str(e)}")
        return False

def verify_azure_search():
    """Verify Azure AI Search connectivity."""
    print(f"\n{Colors.BLUE}🔍 Verifying Azure AI Search...{Colors.ENDC}")
    
    try:
        endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        api_key = os.getenv("AZURE_SEARCH_API_KEY")
        index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "knowledge-base")
        
        if not all([endpoint, api_key]):
            print_status("Azure Search", False, "Missing endpoint or API key in environment")
            return False
        
        # Test connection with a simple request to the service
        headers = {
            'api-key': api_key,
            'Content-Type': 'application/json'
        }
        
        # Check service status
        response = requests.get(f"{endpoint}/servicestats?api-version=2023-11-01", headers=headers)
        if response.status_code == 200:
            print_status("Search Service", True, "Service is accessible")
        else:
            print_status("Search Service", False, f"HTTP {response.status_code}")
            return False
        
        # Check if index exists
        response = requests.get(f"{endpoint}/indexes/{index_name}?api-version=2023-11-01", headers=headers)
        if response.status_code == 200:
            print_status("Search Index", True, f"Index '{index_name}' exists")
        elif response.status_code == 404:
            print_status("Search Index", False, f"Index '{index_name}' not found - will be created during demo")
        else:
            print_status("Search Index", False, f"HTTP {response.status_code}")
        
        return True
        
    except Exception as e:
        print_status("Azure Search", False, f"Connection failed: {str(e)}")
        return False

def verify_azure_storage():
    """Verify Azure Storage connectivity."""
    print(f"\n{Colors.BLUE}💾 Verifying Azure Storage...{Colors.ENDC}")
    
    try:
        account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
        container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "documents")
        
        if not all([account_name, account_key]):
            print_status("Azure Storage", False, "Missing account name or key in environment")
            return False
        
        # Create blob service client
        blob_service_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=account_key
        )
        
        # Test connection
        account_info = blob_service_client.get_account_information()
        print_status("Storage Account", True, f"Account '{account_name}' is accessible")
        
        # Check container
        try:
            container_client = blob_service_client.get_container_client(container_name)
            container_client.get_container_properties()
            print_status("Storage Container", True, f"Container '{container_name}' exists")
        except Exception:
            print_status("Storage Container", False, f"Container '{container_name}' not found")
        
        return True
        
    except Exception as e:
        print_status("Azure Storage", False, f"Connection failed: {str(e)}")
        return False

def verify_azure_functions():
    """Verify Azure Functions connectivity."""
    print(f"\n{Colors.BLUE}⚡ Verifying Azure Functions...{Colors.ENDC}")
    
    try:
        function_app_url = os.getenv("AZURE_FUNCTION_APP_URL")
        function_key = os.getenv("AZURE_FUNCTION_KEY")
        
        if not function_app_url:
            print_status("Azure Functions", False, "Missing function app URL in environment")
            return False
        
        # Test if function app is accessible
        try:
            response = requests.get(f"{function_app_url}/api/send_email", timeout=10)
            if response.status_code in [200, 401, 404]:  # Any response means it's accessible
                print_status("Function App", True, "Function app is accessible")
            else:
                print_status("Function App", False, f"HTTP {response.status_code}")
        except requests.exceptions.RequestException:
            print_status("Function App", False, "Function app not accessible (may not be deployed yet)")
        
        return True
        
    except Exception as e:
        print_status("Azure Functions", False, f"Connection failed: {str(e)}")
        return False

def verify_dependencies():
    """Verify Python dependencies are installed."""
    print(f"\n{Colors.BLUE}📦 Verifying Dependencies...{Colors.ENDC}")
    
    # Package name mappings for import vs pip install names
    required_packages = {
        "openai": "openai",
        "azure-search-documents": "azure.search.documents", 
        "azure-storage-blob": "azure.storage.blob",
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "python-dotenv": "dotenv",
        "PyPDF2": "PyPDF2",
        "python-docx": "docx",
        "beautifulsoup4": "bs4",
        "requests": "requests"
    }
    
    all_installed = True
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print_status("Package", True, f"{package_name} is installed")
        except ImportError:
            print_status("Package", False, f"{package_name} is missing")
            all_installed = False
    
    return all_installed

async def main():
    """Run all verification tests."""
    print(f"{Colors.BOLD}🚀 Azure Toolbox Demo - Setup Verification{Colors.ENDC}")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print(f"{Colors.YELLOW}⚠️  Warning: .env file not found. Using .env.example as reference.{Colors.ENDC}")
        if os.path.exists(".env.example"):
            print(f"Please copy .env.example to .env and update with your Azure credentials.")
        return
    
    results = []
    
    # Run all verification tests
    results.append(verify_dependencies())
    results.append(verify_azure_openai())  # No longer async
    results.append(verify_azure_search())
    results.append(verify_azure_storage())
    results.append(verify_azure_functions())
    
    # Print summary
    print(f"\n{Colors.BOLD}📊 Verification Summary{Colors.ENDC}")
    print("=" * 30)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"{Colors.GREEN}✅ All checks passed! ({passed}/{total}){Colors.ENDC}")
        print(f"{Colors.GREEN}🎉 Your demo environment is ready!{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}⚠️  {passed}/{total} checks passed{Colors.ENDC}")
        print(f"{Colors.YELLOW}Please fix the failing components before running the demo.{Colors.ENDC}")
    
    print(f"\n{Colors.BLUE}Next Steps:{Colors.ENDC}")
    print("1. Run: python web_interface.py")
    print("2. Open: http://localhost:8000")
    print("3. Upload documents and start chatting!")

if __name__ == "__main__":
    asyncio.run(main())
