#!/usr/bin/env python3
"""
Test script for document upload functionality
Tests both PDF and Markdown file uploads to verify the fixes
"""

import os
import requests
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_pdf_upload():
    """Test PDF file upload"""
    logger.info("Testing PDF file upload...")
      # Find a PDF file in the sample documents
    pdf_path = Path("../sample-documents/collateral/Dubai Brochure.pdf")
    if not pdf_path.exists():
        logger.error(f"PDF file not found: {pdf_path}")
        return False
    
    base_url = "http://localhost:8001"  # Using port 8001 to match running server
    upload_url = f"{base_url}/api/upload"
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': (pdf_path.name, f, 'application/pdf')}
            response = requests.post(upload_url, files=files)
            
        if response.status_code == 200:
            result = response.json()
            logger.info(f"PDF upload successful: {result}")
            return True
        else:
            logger.error(f"PDF upload failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error uploading PDF: {str(e)}")
        return False

def test_markdown_upload():
    """Test Markdown file upload"""
    logger.info("Testing Markdown file upload...")
    
    # Find a markdown file in the sample documents
    md_path = Path("../sample-documents/markdowns/ai-strategy-document.md")
    if not md_path.exists():
        logger.error(f"Markdown file not found: {md_path}")
        return False
    
    base_url = "http://localhost:8001"  # Using port 8001 to match running server
    upload_url = f"{base_url}/api/upload"
    
    try:
        with open(md_path, 'rb') as f:
            files = {'file': (md_path.name, f, 'text/markdown')}
            response = requests.post(upload_url, files=files)
            
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Markdown upload successful: {result}")
            return True
        else:
            logger.error(f"Markdown upload failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error uploading Markdown: {str(e)}")
        return False

def main():
    """Run all tests"""
    logger.info("🧪 Testing Document Upload Functionality")
    logger.info("=" * 50)
    
    # Test PDF upload
    pdf_success = test_pdf_upload()
    
    # Test Markdown upload
    md_success = test_markdown_upload()
    
    # Summary
    logger.info("\n📊 Test Results:")
    logger.info(f"PDF Upload: {'✅ PASS' if pdf_success else '❌ FAIL'}")
    logger.info(f"Markdown Upload: {'✅ PASS' if md_success else '❌ FAIL'}")
    
    if pdf_success and md_success:
        logger.info("🎉 All tests passed! Document upload functionality is working correctly.")
        return True
    else:
        logger.error("❌ Some tests failed. Check the logs above for details.")
        return False

if __name__ == "__main__":
    main()
