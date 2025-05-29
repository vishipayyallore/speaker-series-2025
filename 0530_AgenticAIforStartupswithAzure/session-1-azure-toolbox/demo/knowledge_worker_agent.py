"""
Knowledge Worker Agent - Core AI Agent Implementation
Integrates Azure OpenAI, Azure AI Search, and Azure Functions for intelligent document processing
"""
import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from openai import AzureOpenAI
from azure_search_service import AzureSearchService
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeWorkerAgent:
    """Intelligent agent for knowledge work tasks using Azure AI services"""
    
    def __init__(self):
        """Initialize the knowledge worker agent"""
        # Initialize Azure OpenAI client
        self.openai_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
        
        # Initialize Azure Search service
        self.search_service = AzureSearchService()
        
        # Azure Functions configuration
        self.function_app_url = os.getenv("AZURE_FUNCTION_APP_URL")
        self.function_key = os.getenv("AZURE_FUNCTION_KEY")
        
        # Agent system prompt
        self.system_prompt = """You are a knowledgeable AI assistant that helps users find and analyze information from documents. 
        
        Your capabilities include:
        1. Searching through indexed documents to find relevant information
        2. Providing detailed answers with proper citations
        3. Summarizing complex documents
        4. Executing specific actions when requested
        
        Always:
        - Provide accurate information based on the retrieved documents
        - Include citations with source information
        - Be helpful and professional
        - Acknowledge when you don't have enough information
        
        When users ask questions, search for relevant documents first, then provide comprehensive answers based on the retrieved content."""
        
        # Available tools for function calling
        self.available_tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_documents",
                    "description": "Search through indexed documents to find relevant information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query to find relevant documents"
                            },
                            "top_results": {
                                "type": "integer",
                                "description": "Number of top results to return (default: 5)",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "summarize_document",
                    "description": "Provide a detailed summary of a specific document",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "document_id": {
                                "type": "string",
                                "description": "The ID of the document to summarize"
                            }
                        },
                        "required": ["document_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_action",
                    "description": "Execute a specific action using Azure Functions",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action_type": {
                                "type": "string",
                                "description": "The type of action to execute (e.g., 'send_email', 'create_task', 'generate_report')"
                            },
                            "parameters": {
                                "type": "object",
                                "description": "Parameters required for the action"
                            }
                        },
                        "required": ["action_type", "parameters"]
                    }
                }
            }
        ]
    
    def search_documents(self, query: str, top_results: int = 5) -> Dict[str, Any]:
        """Search for relevant documents using Azure AI Search"""
        try:
            results = self.search_service.search_documents(query, top=top_results)
            
            return {
                "success": True,
                "results": results,
                "total_found": len(results),
                "query": query
            }
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "results": [],
                "total_found": 0,
                "query": query
            }
    
    def summarize_document(self, document_id: str) -> Dict[str, Any]:
        """Get and summarize a specific document"""
        try:
            # Search for the specific document
            results = self.search_service.search_documents(f"id:{document_id}", top=1)
            
            if not results:
                return {
                    "success": False,
                    "error": f"Document with ID '{document_id}' not found"
                }
            
            document = results[0]
            
            # Generate summary using OpenAI
            summary_prompt = f"""Please provide a comprehensive summary of the following document:

Title: {document.get('title', 'N/A')}
Content: {document.get('content', '')[:4000]}  # Limit content for token management

Provide a structured summary including:
1. Main topics covered
2. Key insights or findings
3. Important details
4. Actionable items (if any)"""

            response = self.openai_client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are a professional document analyst. Provide clear, structured summaries."},
                    {"role": "user", "content": summary_prompt}
                ],
                temperature=0.3
            )
            
            return {
                "success": True,
                "document_id": document_id,
                "title": document.get('title'),
                "source": document.get('source'),
                "summary": response.choices[0].message.content
            }
            
        except Exception as e:
            logger.error(f"Error summarizing document: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def execute_action(self, action_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action using Azure Functions"""
        try:
            if not self.function_app_url or not self.function_key:
                return {
                    "success": False,
                    "error": "Azure Functions not configured"
                }
            
            # Prepare the request to Azure Function
            function_url = f"{self.function_app_url}/api/{action_type}"
            headers = {
                "Content-Type": "application/json",
                "x-functions-key": self.function_key
            }
            
            response = requests.post(
                function_url,
                headers=headers,
                json=parameters,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "action_type": action_type,
                    "result": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"Function execution failed: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            logger.error(f"Error executing action: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def process_function_call(self, function_call) -> Dict[str, Any]:
        """Process a function call from the AI model"""
        function_name = function_call.name
        arguments = json.loads(function_call.arguments)
        
        if function_name == "search_documents":
            return self.search_documents(
                query=arguments["query"],
                top_results=arguments.get("top_results", 5)
            )
        elif function_name == "summarize_document":
            return self.summarize_document(arguments["document_id"])
        elif function_name == "execute_action":
            return self.execute_action(
                action_type=arguments["action_type"],
                parameters=arguments["parameters"]
            )
        else:
            return {
                "success": False,
                "error": f"Unknown function: {function_name}"
            }
    
    def chat(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Main chat interface for the knowledge worker agent"""
        try:
            # Prepare conversation history
            if conversation_history is None:
                conversation_history = []
            
            # Build messages array
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(conversation_history)
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI with function calling
            response = self.openai_client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                tools=self.available_tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1500
            )
            
            message = response.choices[0].message
            
            # Check if the model wants to call a function
            if message.tool_calls:
                # Process function calls
                function_results = []
                for tool_call in message.tool_calls:
                    function_result = self.process_function_call(tool_call.function)
                    function_results.append({
                        "tool_call_id": tool_call.id,
                        "result": function_result
                    })
                    
                    # Add function result to conversation
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(function_result),
                        "tool_call_id": tool_call.id
                    })
                
                # Get final response after function calls
                final_response = self.openai_client.chat.completions.create(
                    model=self.deployment_name,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1500
                )
                
                final_message = final_response.choices[0].message.content
                
                return {
                    "success": True,
                    "response": final_message,
                    "function_calls": function_results,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # Direct response without function calls
                return {
                    "success": True,
                    "response": message.content,
                    "function_calls": [],
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get the current status of the agent and its services"""
        try:
            # Check search service
            search_stats = self.search_service.get_index_statistics()
            
            # Check OpenAI connectivity
            openai_status = "connected"
            try:
                self.openai_client.chat.completions.create(
                    model=self.deployment_name,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1
                )
            except:
                openai_status = "error"
            
            return {
                "agent_status": "healthy",
                "services": {
                    "azure_openai": {
                        "status": openai_status,
                        "deployment": self.deployment_name
                    },
                    "azure_search": {
                        "status": "connected" if search_stats else "error",
                        "document_count": search_stats.get("document_count", 0),
                        "index_name": self.search_service.index_name
                    },
                    "azure_functions": {
                        "status": "configured" if self.function_app_url else "not_configured",
                        "url": self.function_app_url
                    }
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting agent status: {str(e)}")
            return {
                "agent_status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
