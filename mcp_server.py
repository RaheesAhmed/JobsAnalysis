from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_rapidapi_jobs, fetch_linkedin_jobs
from src.helper import extract_text_from_pdf, ask_openai
import os

# Initialize MCP server
mcp = FastMCP("Job Recommender")


@mcp.tool()
async def analyze_resume_from_file(file_path: str) -> dict:
    """
    Analyzes a resume PDF file and returns summary, skill gaps, roadmap, ATS score, and keywords.
    
    Args:
        file_path: Full path to the PDF resume file (e.g., C:/Users/name/resume.pdf)
        
    Returns:
        Dictionary with analysis results
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
        
        # Extract text from PDF
        with open(file_path, 'rb') as file:
            resume_text = extract_text_from_pdf(file)
        
        if not resume_text or len(resume_text.strip()) < 50:
            return {"error": "Could not extract text from PDF or text is too short"}
        
        # Now analyze the extracted text
        return await analyze_resume(resume_text)
        
    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}

@mcp.tool()
async def analyze_resume(resume_text: str) -> dict:
    """
    Analyzes resume text and returns summary, skill gaps, roadmap, ATS score, and keywords.
    
    Args:
        resume_text: The text content of the resume
        
    Returns:
        Dictionary with analysis results
    """
    try:
        # Get summary
        summary = ask_openai(
            f"Summarize this resume highlighting the skills, education, and experience: \n\n{resume_text}", 
            max_tokens=500
        )
        
        # Get skill gaps
        gaps = ask_openai(
            f"Analyze this resume and highlight missing skills, certifications, and experiences: \n\n{resume_text}", 
            max_tokens=400
        )
        
        # Get roadmap
        roadmap = ask_openai(
            f"Based on this resume, suggest a future roadmap: \n\n{resume_text}", 
            max_tokens=400
        )
        
        # Get ATS score
        ats_analysis = ask_openai(
            f"""Analyze this resume for ATS compatibility.
Provide: ATS Score (0-100), Explanation, and Recommendations.

Resume: {resume_text}""", 
            max_tokens=600
        )
        
        # Get keywords
        keywords = ask_openai(
            f"Based on this resume, suggest job search keywords (comma-separated only):\n\n{summary}",
            max_tokens=100
        )
        
        # Extract score
        try:
            score_line = ats_analysis.split('\n')[0]
            ats_score = ''.join(filter(str.isdigit, score_line))
        except:
            ats_score = "N/A"
        
        return {
            "summary": summary,
            "skill_gaps": gaps,
            "career_roadmap": roadmap,
            "ats_score": ats_score,
            "ats_analysis": ats_analysis,
            "job_keywords": keywords.strip()
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def fetch_jobs(keywords: str, location: str = "Saudi Arabia") -> dict:
    """
    Fetches job listings from RapidAPI and LinkedIn.
    
    Args:
        keywords: Job search keywords (e.g., "Data Scientist, Machine Learning")
        location: Job location (default: "Saudi Arabia")
        
    Returns:
        Dictionary with job listings from both sources
    """
    try:
        rapidapi_jobs = fetch_rapidapi_jobs(keywords, location=location, rows=10)
        linkedin_jobs = fetch_linkedin_jobs(keywords, location=location, rows=10)
        
        return {
            "rapidapi_jobs": {
                "total": len(rapidapi_jobs),
                "jobs": rapidapi_jobs
            },
            "linkedin_jobs": {
                "total": len(linkedin_jobs),
                "jobs": linkedin_jobs
            }
        }
    except Exception as e:
        return {"error": str(e)}
    
@mcp.prompt()
def system_prompt() -> str: 
    """
    System instructions for Job Recommender MCP server
    """
    script_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(script_dir, "prompts", "system_instructions.md")

    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":
    mcp.run(transport='stdio')






