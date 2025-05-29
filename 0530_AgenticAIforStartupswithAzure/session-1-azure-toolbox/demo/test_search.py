#!/usr/bin/env python3
"""
Test script to search for documents in Azure Search
Tests search functionality after successfully uploading documents
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from azure_search_service import AzureSearchService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_search():
    """Test searching for documents in Azure Search"""
    logger.info("Testing search functionality...")
    
    search_service = AzureSearchService()
    
    # Search for Dubai-related content
    search_query = "Dubai"
    logger.info(f"Searching for: '{search_query}'")
    
    results = search_service.search_documents(search_query)
    
    if not results:
        logger.error("❌ No results found")
        return False
    
    logger.info(f"✅ Found {len(results)} results")
      # Print the results
    for i, result in enumerate(results, 1):
        logger.info(f"Result #{i}:")
        logger.info(f"  Title: {result.get('title')}")
        logger.info(f"  Source: {result.get('source')}")
        logger.info(f"  Category: {result.get('category')}")
        logger.info(f"  Score: {result.get('score')}")
        
        # Print captions if available (semantic search highlights)
        if 'captions' in result:
            logger.info("  Relevant passages:")
            for j, caption in enumerate(result['captions'], 1):
                logger.info(f"    {j}. {caption}")
        
        # Print a snippet of content
        content = result.get('content', '')
        snippet = content[:150] + "..." if len(content) > 150 else content
        logger.info(f"  Content snippet: {snippet}")
        logger.info("-" * 50)
    
    return True

def main():
    """Run the search test"""
    logger.info("🔍 Testing Azure Search Functionality")
    logger.info("=" * 50)
    
    success = test_search()
    
    logger.info("\n📊 Test Results:")
    logger.info(f"Search: {'✅ PASS' if success else '❌ FAIL'}")
    
    if success:
        logger.info("🎉 Search is working correctly!")
    else:
        logger.error("❌ Search failed. Check the logs above for details.")

if __name__ == "__main__":
    main()
