"""
Azure Function: Send Email
Demonstrates tool-based functionality for the Knowledge Worker Agent
"""
import logging
import json
import azure.functions as func
from datetime import datetime
from typing import Dict, Any

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function to simulate sending emails based on agent requests
    This would integrate with services like SendGrid, Azure Communication Services, etc.
    """
    logging.info('Send Email function processed a request.')

    try:
        # Parse the request body
        req_body = req.get_json()
        
        if not req_body:
            return func.HttpResponse(
                json.dumps({"error": "Request body is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Extract email parameters
        to_email = req_body.get('to_email')
        subject = req_body.get('subject')
        body = req_body.get('body')
        cc_emails = req_body.get('cc_emails', [])
        attachments = req_body.get('attachments', [])
        
        # Validate required fields
        if not all([to_email, subject, body]):
            return func.HttpResponse(
                json.dumps({"error": "to_email, subject, and body are required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Simulate email sending (in a real implementation, integrate with email service)
        email_result = {
            "success": True,
            "message_id": f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "to": to_email,
            "cc": cc_emails,
            "subject": subject,
            "body_preview": body[:100] + "..." if len(body) > 100 else body,
            "attachment_count": len(attachments),
            "sent_at": datetime.now().isoformat(),
            "service": "demo_email_service",
            "status": "delivered"
        }
        
        logging.info(f"Email sent successfully to {to_email}")
        
        return func.HttpResponse(
            json.dumps(email_result),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": f"Failed to send email: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )
