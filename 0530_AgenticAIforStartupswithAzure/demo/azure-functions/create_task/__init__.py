"""
Azure Function: Create Task
Demonstrates task management functionality for the Knowledge Worker Agent
"""
import logging
import json
import azure.functions as func
from datetime import datetime, timedelta
from typing import Dict, Any, List

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function to create and manage tasks based on agent requests
    This would integrate with project management tools like Azure DevOps, Microsoft Planner, etc.
    """
    logging.info('Create Task function processed a request.')

    try:
        # Parse the request body
        req_body = req.get_json()
        
        if not req_body:
            return func.HttpResponse(
                json.dumps({"error": "Request body is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Extract task parameters
        title = req_body.get('title')
        description = req_body.get('description', '')
        assignee = req_body.get('assignee')
        priority = req_body.get('priority', 'medium')
        due_date = req_body.get('due_date')
        project = req_body.get('project', 'General')
        tags = req_body.get('tags', [])
        
        # Validate required fields
        if not title:
            return func.HttpResponse(
                json.dumps({"error": "title is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Generate task ID
        task_id = f"TASK-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Set default due date if not provided (7 days from now)
        if not due_date:
            due_date = (datetime.now() + timedelta(days=7)).isoformat()
        
        # Create task object
        task = {
            "success": True,
            "task_id": task_id,
            "title": title,
            "description": description,
            "assignee": assignee,
            "priority": priority,
            "status": "open",
            "project": project,
            "tags": tags,
            "due_date": due_date,
            "created_at": datetime.now().isoformat(),
            "created_by": "knowledge_worker_agent",
            "url": f"https://tasks.example.com/task/{task_id}",
            "estimated_hours": req_body.get('estimated_hours'),
            "dependencies": req_body.get('dependencies', [])
        }
        
        logging.info(f"Task created successfully: {task_id}")
        
        return func.HttpResponse(
            json.dumps(task),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error creating task: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": f"Failed to create task: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )
