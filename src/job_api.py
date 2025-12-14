import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_linkedin_jobs(search_query, location="Saudi Arabia", rows=10):
    """Fetches jobs from LinkedIn using Apify"""
    apify_token = os.getenv("APIFY_API_TOKEN")
    
    if not apify_token:
        print(" APIFY_API_TOKEN not found")
        return []
    
    try:
        from apify_client import ApifyClient
        client = ApifyClient(apify_token)
        
        # Use only first keyword
        main_keyword = search_query.split(',')[0].strip()
        
        print(f" LinkedIn: '{main_keyword}' in '{location}'")
        
        run_input = {
            "title": main_keyword,
            "location": location,
            "rows": rows,
            "proxy": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"]
            }
        }
        
        run = client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
        jobs = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        
        print(f" LinkedIn: {len(jobs)} jobs found")
        return jobs
    
    except Exception as e:
        print(f" LinkedIn error: {str(e)}")
        return []

def fetch_rapidapi_jobs(search_query, location="Saudi Arabia", rows=10):
    """Fetches jobs from RapidAPI JSearch"""
    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    
    if not rapidapi_key:
        print(" RAPIDAPI_KEY not found")
        return []
    
    # Use only first keyword
    main_keyword = search_query.split(',')[0].strip()
    
    url = "https://jsearch.p.rapidapi.com/search"
    
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    
    querystring = {
        "query": f"{main_keyword} in {location}",
        "page": "1",
        "num_pages": "1"
    }
    
    try:
        print(f" RapidAPI: '{main_keyword}' in '{location}'" )
        
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        jobs = data.get("data", [])
        
        print(f" RapidAPI: {len(jobs)} jobs found")
        return jobs
    
    except Exception as e:
        print(f" RapidAPI error: {str(e)}")
        return []



