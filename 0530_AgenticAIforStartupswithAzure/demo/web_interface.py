"""
Web Interface for the Knowledge Worker Agent Demo
FastAPI-based interface for demonstrating the Azure AI capabilities
"""
import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
from pathlib import Path

# FastAPI and related imports
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import our custom modules
from knowledge_worker_agent import KnowledgeWorkerAgent
from document_processor import DocumentProcessor
from azure_search_service import AzureSearchService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Knowledge Worker Agent Demo",
    description="Azure AI-powered document analysis and question answering",
    version="1.0.0"
)

# Initialize services
agent = KnowledgeWorkerAgent()
doc_processor = DocumentProcessor()
search_service = AzureSearchService()

# Templates and static files
templates = Jinja2Templates(directory="templates")

# Pydantic models for API
class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    success: bool
    response: str
    function_calls: List[Dict[str, Any]] = []
    timestamp: str
    error: Optional[str] = None

class DocumentUploadResponse(BaseModel):
    success: bool
    document_id: Optional[str] = None
    filename: str
    error: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    top_results: int = 5

# API Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main demo interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/status")
async def get_status():
    """Get the status of all Azure services"""
    try:
        status = agent.get_agent_status()
        return JSONResponse(content=status)
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the knowledge worker agent"""
    try:
        result = agent.chat(
            user_message=request.message,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        return ChatResponse(
            success=False,
            response="",
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.post("/api/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("general")
):
    """Upload and process a document"""
    try:
        # Read file content
        file_content = await file.read()
        
        # Process the document
        result = doc_processor.process_file(
            file_content=file_content,
            filename=file.filename,
            category=category
        )
        
        if result["success"]:
            return DocumentUploadResponse(
                success=True,
                document_id=result["document_id"],
                filename=file.filename
            )
        else:
            return DocumentUploadResponse(
                success=False,
                filename=file.filename,
                error=result["error"]
            )
            
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        return DocumentUploadResponse(
            success=False,
            filename=file.filename if file else "unknown",
            error=str(e)
        )

@app.post("/api/url")
async def process_url(url: str = Form(...), category: str = Form("web")):
    """Process content from a URL"""
    try:
        result = doc_processor.process_url(url=url, category=category)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error processing URL: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
async def search_documents(request: SearchRequest):
    """Search through indexed documents"""
    try:
        result = agent.search_documents(
            query=request.query,
            top_results=request.top_results
        )
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents/stats")
async def get_document_stats():
    """Get statistics about processed documents"""
    try:
        stats = doc_processor.get_processing_statistics()
        return JSONResponse(content=stats)
    except Exception as e:
        logger.error(f"Error getting document stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/setup")
async def setup_search_index():
    """Initialize the search index (for demo setup)"""
    try:
        success = search_service.create_search_index()
        return JSONResponse(content={
            "success": success,
            "message": "Search index created successfully" if success else "Failed to create search index"
        })
    except Exception as e:
        logger.error(f"Error setting up search index: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

if __name__ == "__main__":
    # Create templates directory if it doesn't exist
    Path("templates").mkdir(exist_ok=True)
    
    print("🚀 Starting Knowledge Worker Agent Demo")
    print("📖 Open http://localhost:8000 to access the demo")
    print("📊 API documentation available at http://localhost:8000/docs")
    
    uvicorn.run(
        "web_interface:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
