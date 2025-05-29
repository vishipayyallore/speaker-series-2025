#!/usr/bin/env python3
"""
End-to-end test script for the Knowledge Worker Agent Demo
Tests document upload, processing, and search index creation
"""

import os
import sys
import requests
import json
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from azure_search_service import AzureSearchService
from document_processor import DocumentProcessor

def test_search_index_creation():
    """Test creating the search index if it doesn't exist"""
    print("🔍 Testing search index creation...")
    
    try:
        search_service = AzureSearchService()
        result = search_service.create_search_index()
        print(f"✅ Search index creation result: {result}")
        return True
    except Exception as e:
        print(f"❌ Search index creation failed: {e}")
        return False

def test_document_upload():
    """Test document upload via API"""
    print("\n📄 Testing document upload...")
    
    # Test data
    test_files = [
        {
            "name": "test_markdown.md",
            "content": """# Test Markdown Document

This is a test markdown document for the Knowledge Worker Agent Demo.

## Introduction

This document contains sample content to test the markdown processing functionality.

### Key Features

- Markdown support
- Title extraction
- Content processing
- Search indexing

### Conclusion

This test document should be processed successfully by the system.
""",
            "type": "text/markdown"
        },
        {
            "name": "test_pdf_content.txt", 
            "content": "This is a test document that simulates PDF content processing.",
            "type": "text/plain"
        }
    ]
    
    base_url = "http://localhost:8000"
    upload_url = f"{base_url}/api/upload"
    
    for test_file in test_files:
        try:
            print(f"  📤 Uploading {test_file['name']}...")
            
            files = {
                'file': (test_file['name'], test_file['content'], test_file['type'])
            }
            
            response = requests.post(upload_url, files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ Upload successful: {result}")
            else:
                print(f"  ❌ Upload failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"  ❌ Upload error for {test_file['name']}: {e}")
    
    return True

def test_document_processing():
    """Test document processing directly"""
    print("\n🔧 Testing document processing...")
    
    try:
        processor = DocumentProcessor()
        
        # Create a test markdown file
        test_file_path = Path("test_sample.md")
        test_content = """# Sample Test Document

This is a test document to verify markdown processing.

## Section 1

Content for section 1.

## Section 2

Content for section 2.
"""
        
        test_file_path.write_text(test_content, encoding='utf-8')
        
        # Process the file
        result = processor.process_file(test_content.encode('utf-8'), "test_sample.md")
        
        print(f"✅ Processing result: {result}")
        
        # Clean up
        test_file_path.unlink()
        
        return True
        
    except Exception as e:
        print(f"❌ Document processing failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔗 Testing API endpoints...")
    
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/",
        "/docs",
        "/health"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"  ✅ {endpoint}: OK")
            else:
                print(f"  ❌ {endpoint}: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {endpoint}: Error - {e}")

def main():
    """Run all tests"""
    print("🚀 Running End-to-End Tests for Knowledge Worker Agent Demo")
    print("=" * 60)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    tests = [
        test_api_endpoints,
        test_search_index_creation,
        test_document_processing,
        test_document_upload
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result if result is not None else False)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"✅ Passed: {sum(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("\n🎉 All tests passed! The application is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
