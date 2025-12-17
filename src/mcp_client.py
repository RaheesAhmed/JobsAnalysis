import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional


# MCP Server Configuration
MCP_SERVER_URL = "http://127.0.0.1:8080"


def call_mcp_analyze_resume(resume_text: str) -> Dict[str, Any]:
    """
    Call MCP server to analyze resume via HTTP and return request/response data.
    
    Args:
        resume_text: The resume text to analyze
        
    Returns:
        Dictionary containing:
        - request: The MCP request JSON
        - response: The MCP response JSON
        - timestamp: When the request was made
        - duration_ms: How long the request took
    """
    
    # Prepare MCP request (JSON-RPC 2.0 format)
    mcp_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "analyze_resume",
            "arguments": {
                "resume_text": resume_text[:1000]  # Limit to first 1000 chars for display
            }
        }
    }
    
    start_time = datetime.now()
    
    try:
        # Send HTTP POST request to MCP server
        response = requests.post(
            f"{MCP_SERVER_URL}/mcp/v1/messages",
            json=mcp_request,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        end_time = datetime.now()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        # Parse response
        try:
            mcp_response = response.json()
        except json.JSONDecodeError:
            mcp_response = {
                "error": "Failed to parse MCP response",
                "raw_output": response.text[:500],
                "status_code": response.status_code
            }
        
        return {
            "request": mcp_request,
            "response": mcp_response,
            "timestamp": start_time.isoformat(),
            "duration_ms": duration_ms,
            "success": response.status_code == 200 and "error" not in mcp_response
        }
    
    except requests.exceptions.Timeout:
        end_time = datetime.now()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        return {
            "request": mcp_request,
            "response": {"error": "MCP server timeout (30s)"},
            "timestamp": start_time.isoformat(),
            "duration_ms": duration_ms,
            "success": False
        }
    
    except requests.exceptions.ConnectionError:
        end_time = datetime.now()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        return {
            "request": mcp_request,
            "response": {
                "error": f"Cannot connect to MCP server at {MCP_SERVER_URL}",
                "details": "Make sure the MCP server is running: python mcp_server.py"
            },
            "timestamp": start_time.isoformat(),
            "duration_ms": duration_ms,
            "success": False
        }
    
    except Exception as e:
        end_time = datetime.now()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        return {
            "request": mcp_request,
            "response": {"error": f"MCP client error: {str(e)}"},
            "timestamp": start_time.isoformat(),
            "duration_ms": duration_ms,
            "success": False
        }


def call_mcp_fetch_jobs(keywords: str, location: str = "Saudi Arabia") -> Dict[str, Any]:
    """
    Call MCP server to fetch jobs via HTTP.
    
    Args:
        keywords: Job search keywords
        location: Job location
        
    Returns:
        Dictionary containing request/response/metadata
    """
    
    mcp_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "fetch_jobs",
            "arguments": {
                "keywords": keywords,
                "location": location
            }
        }
    }
    
    start_time = datetime.now()
    
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/mcp/v1/messages",
            json=mcp_request,
            headers={"Content-Type": "application/json"},
            timeout=45
        )
        
        end_time = datetime.now()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        try:
            mcp_response = response.json()
        except json.JSONDecodeError:
            mcp_response = {
                "error": "Failed to parse MCP response",
                "raw_output": response.text[:500]
            }
        
        return {
            "request": mcp_request,
            "response": mcp_response,
            "timestamp": start_time.isoformat(),
            "duration_ms": duration_ms,
            "success": response.status_code == 200 and "error" not in mcp_response
        }
    
    except Exception as e:
        end_time = datetime.now()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        return {
            "request": mcp_request,
            "response": {"error": f"MCP client error: {str(e)}"} ,
            "timestamp": start_time.isoformat(),
            "duration_ms": duration_ms,
            "success": False
        }


def format_json_for_display(json_data: Any, indent: int = 2) -> str:
    """Format JSON for pretty display."""
    return json.dumps(json_data, indent=indent, ensure_ascii=False)


# Sample resumes for testing
SAMPLE_RESUMES = {
    "Software Engineer": """John Doe
Software Engineer

EXPERIENCE:
- Developed web applications using Python and JavaScript
- Worked with databases and APIs
- Collaborated with team members

EDUCATION:
- Bachelor's in Computer Science

SKILLS:
- Python, JavaScript, SQL""",
    
    "Data Scientist": """Jane Smith
Data Scientist

EXPERIENCE:
- Analyzed data using Python and R
- Created machine learning models
- Presented findings to stakeholders

EDUCATION:
- Master's in Data Science

SKILLS:
- Python, R, Machine Learning, SQL""",
    
    "Marketing Manager": """Alice Johnson
Marketing Manager

EXPERIENCE:
- Managed marketing campaigns
- Increased brand awareness
- Led team of 5 people

EDUCATION:
- MBA in Marketing

SKILLS:
- Social Media, SEO, Content Strategy"""
}


def get_sample_resume(name: str) -> Optional[str]:
    """Get a sample resume by name."""
    return SAMPLE_RESUMES.get(name)


def get_sample_resume_names() -> list:
    """Get list of available sample resume names."""
    return list(SAMPLE_RESUMES.keys())
