import json
import os
from datetime import datetime
from typing import Dict, List, Any


ANALYTICS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "analytics.json")


def _load_analytics() -> Dict[str, Any]:
    """Load analytics data from JSON file."""
    try:
        if os.path.exists(ANALYTICS_FILE):
            with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"analyses": [], "created_at": datetime.now().isoformat(), "version": "1.0"}
    except Exception as e:
        print(f"Error loading analytics: {e}")
        return {"analyses": [], "created_at": datetime.now().isoformat(), "version": "1.0"}


def _save_analytics(data: Dict[str, Any]) -> None:
    """Save analytics data to JSON file."""
    try:
        os.makedirs(os.path.dirname(ANALYTICS_FILE), exist_ok=True)
        with open(ANALYTICS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving analytics: {e}")


def save_analysis(ats_score: int, skill_gaps: List[str], keywords: List[str], job_count: int = 0) -> None:
    """
    Save a new analysis to the analytics database.
    
    Args:
        ats_score: ATS score (0-100)
        skill_gaps: List of identified skill gaps
        keywords: List of job keywords
        job_count: Number of jobs recommended
    """
    data = _load_analytics()
    
    analysis_entry = {
        "timestamp": datetime.now().isoformat(),
        "ats_score": int(ats_score) if ats_score and str(ats_score).isdigit() else 0,
        "skill_gaps": skill_gaps[:10],  # Store max 10 gaps
        "keywords": keywords[:10],  # Store max 10 keywords
        "job_count": job_count
    }
    
    data["analyses"].append(analysis_entry)
    _save_analytics(data)


def get_total_count() -> int:
    """Get total number of resumes analyzed."""
    data = _load_analytics()
    return len(data.get("analyses", []))


def get_average_ats() -> float:
    """Get average ATS score across all analyses."""
    data = _load_analytics()
    analyses = data.get("analyses", [])
    
    if not analyses:
        return 0.0
    
    scores = [a["ats_score"] for a in analyses if a.get("ats_score", 0) > 0]
    return round(sum(scores) / len(scores), 1) if scores else 0.0


def get_top_skill_gaps(n: int = 5) -> List[tuple]:
    """
    Get most common skill gaps.
    
    Args:
        n: Number of top gaps to return
        
    Returns:
        List of tuples (skill_name, count)
    """
    data = _load_analytics()
    analyses = data.get("analyses", [])
    
    gap_counts = {}
    for analysis in analyses:
        for gap in analysis.get("skill_gaps", []):
            gap_lower = gap.lower().strip()
            if gap_lower:
                gap_counts[gap_lower] = gap_counts.get(gap_lower, 0) + 1
    
    sorted_gaps = sorted(gap_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_gaps[:n]


def get_top_keywords(n: int = 10) -> List[tuple]:
    """
    Get most frequent job keywords.
    
    Args:
        n: Number of top keywords to return
        
    Returns:
        List of tuples (keyword, count)
    """
    data = _load_analytics()
    analyses = data.get("analyses", [])
    
    keyword_counts = {}
    for analysis in analyses:
        for keyword in analysis.get("keywords", []):
            keyword_lower = keyword.lower().strip()
            if keyword_lower:
                keyword_counts[keyword_lower] = keyword_counts.get(keyword_lower, 0) + 1
    
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_keywords[:n]


def get_score_distribution() -> Dict[str, int]:
    """
    Get distribution of ATS scores across ranges.
    
    Returns:
        Dictionary with score ranges and counts
    """
    data = _load_analytics()
    analyses = data.get("analyses", [])
    
    distribution = {
        "0-40": 0,
        "41-60": 0,
        "61-80": 0,
        "81-100": 0
    }
    
    for analysis in analyses:
        score = analysis.get("ats_score", 0)
        if 0 <= score <= 40:
            distribution["0-40"] += 1
        elif 41 <= score <= 60:
            distribution["41-60"] += 1
        elif 61 <= score <= 80:
            distribution["61-80"] += 1
        elif 81 <= score <= 100:
            distribution["81-100"] += 1
    
    return distribution


def get_all_analyses() -> List[Dict[str, Any]]:
    """Get all analyses (for advanced features)."""
    data = _load_analytics()
    return data.get("analyses", [])


def clear_analytics() -> None:
    """Clear all analytics data (admin function)."""
    data = {
        "analyses": [],
        "created_at": datetime.now().isoformat(),
        "version": "1.0"
    }
    _save_analytics(data)
