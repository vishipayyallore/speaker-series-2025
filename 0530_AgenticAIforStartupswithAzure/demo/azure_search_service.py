"""
Azure AI Search integration for the Knowledge Worker Agent
Handles document indexing and vector search capabilities
"""
import os
import logging
from typing import List, Dict, Any, Optional
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.models import VectorizedQuery
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticConfiguration,
    SemanticSearch,
    SemanticPrioritizedFields,
    SemanticField
)
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureSearchService:
    """Service for managing Azure AI Search operations"""
    
    def __init__(self):
        """Initialize the Azure Search service with configuration"""
        self.search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.search_key = os.getenv("AZURE_SEARCH_API_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "knowledge-base")
        
        if not all([self.search_endpoint, self.search_key]):
            raise ValueError("Azure Search configuration is missing")
        
        # Initialize clients
        self.credential = AzureKeyCredential(self.search_key)
        self.search_client = SearchClient(
            endpoint=self.search_endpoint,
            index_name=self.index_name,
            credential=self.credential
        )
        self.index_client = SearchIndexClient(
            endpoint=self.search_endpoint,
            credential=self.credential
        )
        
        # Initialize OpenAI client for embeddings
        self.openai_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
    
    def create_search_index(self) -> bool:
        """Create the search index with vector search capabilities"""
        try:
            # Define the search index schema
            fields = [
                SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                SearchableField(name="title", type=SearchFieldDataType.String),
                SearchableField(name="content", type=SearchFieldDataType.String),
                SearchField(name="content_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                           searchable=True, vector_search_dimensions=3072, vector_search_profile_name="default"),
                SimpleField(name="source", type=SearchFieldDataType.String, filterable=True, facetable=True),
                SimpleField(name="category", type=SearchFieldDataType.String, filterable=True, facetable=True),
                SimpleField(name="created_date", type=SearchFieldDataType.DateTimeOffset, filterable=True, sortable=True),
                SearchableField(name="metadata", type=SearchFieldDataType.String)
            ]
            
            # Configure vector search
            vector_search = VectorSearch(
                algorithms=[
                    HnswAlgorithmConfiguration(name="default")
                ],
                profiles=[
                    VectorSearchProfile(
                        name="default",
                        algorithm_configuration_name="default"
                    )
                ]
            )
            
            # Configure semantic search
            semantic_config = SemanticConfiguration(
                name="default",
                prioritized_fields=SemanticPrioritizedFields(
                    title_field=SemanticField(field_name="title"),
                    content_fields=[SemanticField(field_name="content")]
                )
            )
            
            semantic_search = SemanticSearch(configurations=[semantic_config])
            
            # Create the index
            index = SearchIndex(
                name=self.index_name,
                fields=fields,
                vector_search=vector_search,
                semantic_search=semantic_search
            )
            
            result = self.index_client.create_or_update_index(index)
            logger.info(f"Search index '{self.index_name}' created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating search index: {str(e)}")
            return False
    
    def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings using Azure OpenAI"""
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model=self.embedding_deployment
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def index_document(self, document: Dict[str, Any]) -> bool:
        """Index a single document with vector embeddings"""
        try:
            # Generate embeddings for the content
            content_embedding = self.generate_embeddings(document.get("content", ""))
            
            # Prepare the document for indexing
            search_document = {
                "id": document.get("id"),
                "title": document.get("title", ""),
                "content": document.get("content", ""),
                "content_vector": content_embedding,
                "source": document.get("source", ""),
                "category": document.get("category", "general"),
                "created_date": document.get("created_date"),
                "metadata": json.dumps(document.get("metadata", {}))
            }
            
            # Upload to search index
            result = self.search_client.upload_documents([search_document])
            logger.info(f"Document '{document.get('id')}' indexed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error indexing document: {str(e)}")
            return False
    
    def search_documents(self, query: str, top: int = 5, use_semantic_search: bool = True) -> List[Dict[str, Any]]:
        """Perform hybrid search (vector + keyword) with optional semantic ranking"""
        try:
            # Generate query embedding
            query_embedding = self.generate_embeddings(query)
            
            # Create vector query
            vector_query = VectorizedQuery(
                vector=query_embedding,
                k_nearest_neighbors=top,
                fields="content_vector"
            )
            
            # Perform search
            search_kwargs = {
                "search_text": query,
                "vector_queries": [vector_query],
                "top": top,
                "select": ["id", "title", "content", "source", "category", "metadata"]
            }
            
            if use_semantic_search:
                search_kwargs.update({
                    "query_type": "semantic",
                    "semantic_configuration_name": "default",
                    "query_caption": "extractive",
                    "query_answer": "extractive"
                })
            
            results = self.search_client.search(**search_kwargs)
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_result = {
                    "id": result.get("id"),
                    "title": result.get("title"),
                    "content": result.get("content"),
                    "source": result.get("source"),
                    "category": result.get("category"),
                    "metadata": json.loads(result.get("metadata", "{}")),
                    "score": result.get("@search.score", 0),
                    "reranker_score": result.get("@search.reranker_score")
                }
                
                # Add semantic captions and answers if available
                if hasattr(result, '@search.captions'):
                    formatted_result["captions"] = [caption.text for caption in result['@search.captions']]
                
                formatted_results.append(formatted_result)
            
            logger.info(f"Found {len(formatted_results)} results for query: {query}")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document from the search index"""
        try:
            result = self.search_client.delete_documents([{"id": document_id}])
            logger.info(f"Document '{document_id}' deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False
    
    def get_index_statistics(self) -> Dict[str, Any]:
        """Get statistics about the search index"""
        try:
            stats = self.index_client.get_index_statistics(self.index_name)
            return {
                "document_count": stats.document_count,
                "storage_size": stats.storage_size
            }
        except Exception as e:
            logger.error(f"Error getting index statistics: {str(e)}")
            return {}
