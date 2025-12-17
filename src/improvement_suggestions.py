from src.helper import ask_openai


def get_improvement_suggestions(resume_text: str) -> dict:
    """
    Analyze resume and provide before/after improvement suggestions.
    
    Args:
        resume_text: The resume text to analyze
        
    Returns:
        Dictionary with 'current_issues' and 'suggested_improvements'
    """
    prompt = f"""Analyze this resume and provide specific improvement suggestions.

Format your response EXACTLY as follows:

CURRENT ISSUES:
- [List 5-7 specific issues with the resume]

SUGGESTED IMPROVEMENTS:
- [List 5-7 specific actionable improvements]

Focus on:
- Missing quantifiable achievements
- Weak action verbs
- ATS keyword optimization
- Formatting issues
- Missing important sections
- Grammar and clarity

Resume:
{resume_text}"""

    response = ask_openai(prompt, max_tokens=600)
    
    # Parse the response
    try:
        parts = response.split("SUGGESTED IMPROVEMENTS:")
        
        current_issues = ""
        suggested_improvements = ""
        
        if len(parts) >= 2:
            issues_section = parts[0].replace("CURRENT ISSUES:", "").strip()
            improvements_section = parts[1].strip()
            
            current_issues = issues_section
            suggested_improvements = improvements_section
        else:
            # Fallback if parsing fails
            current_issues = response[:len(response)//2]
            suggested_improvements = response[len(response)//2:]
        
        return {
            "current_issues": current_issues,
            "suggested_improvements": suggested_improvements
        }
    
    except Exception as e:
        print(f"Error parsing improvement suggestions: {e}")
        return {
            "current_issues": "Unable to analyze issues at this time.",
            "suggested_improvements": response
        }


def get_formatted_issues_html(issues: str) -> str:
    """Format current issues as HTML for display."""
    return f"""
    <div style="background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); 
                padding: 1.5rem; border-radius: 12px; border-left: 5px solid #e53935;
                margin: 1rem 0;">
        <h3 style="color: #c62828; margin-bottom: 1rem; font-size: 1.3rem;">
            ❌ Current Issues
        </h3>
        <div style="color: #2c3e50; line-height: 1.8; white-space: pre-wrap;">
{issues}
        </div>
    </div>
    """


def get_formatted_improvements_html(improvements: str) -> str:
    """Format suggested improvements as HTML for display."""
    return f"""
    <div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
                padding: 1.5rem; border-radius: 12px; border-left: 5px solid #43a047;
                margin: 1rem 0;">
        <h3 style="color: #2e7d32; margin-bottom: 1rem; font-size: 1.3rem;">
            ✅ Suggested Improvements
        </h3>
        <div style="color: #2c3e50; line-height: 1.8; white-space: pre-wrap;">
{improvements}
        </div>
    </div>
    """
