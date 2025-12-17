import streamlit as st
from datetime import datetime
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_rapidapi_jobs
from src.pdf_generator import generate_analysis_pdf
from src.improvement_suggestions import get_improvement_suggestions, get_formatted_issues_html, get_formatted_improvements_html
from src.analytics_manager import save_analysis  



# Page configuration
st.set_page_config(
    page_title="AI Job Analyzer", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS matching the screenshot design
st.markdown("""
<style>
       
            
    /* Main background - Periwinkle */
    .main {
        background-color: #CCCCFF;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling with gradient background */
    .header-container {
        background: linear-gradient(135deg, #6b7fd7 0%, #8b5fbf 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 12px rgba(107, 127, 215, 0.3);
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        color: white;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        font-size: 1.3rem;
        margin-top: 0.8rem;
        opacity: 0.95;
        color: white;
        font-weight: 400;
    }

    
    /* Section labels */
    .section-label {
        color: #333;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        text-align: center;
        display: block;
    }
    
    /* Content boxes - light colored backgrounds */
    .content-box {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        margin-bottom: 2rem;
        border: 1px solid #e8e8e8;
    }
    
    .content-box-summary {
        background: linear-gradient(135deg, #e8f4fd 0%, #d4e9fc 100%);
        border-left: 5px solid #4a90e2;
    }
    
    .content-box-gaps {
        background: linear-gradient(135deg, #fff5e6 0%, #ffe4b3 100%);
        border-left: 5px solid #ff9f43;
    }
    
    .content-box-roadmap {
        background: linear-gradient(135deg, #e8f8f0 0%, #d0f0e0 100%);
        border-left: 5px solid #26de81;
    }
    
    .content-text {
        color: #2c3e50;
        font-size: 1.05rem;
        line-height: 1.8;
        margin: 0;
    }
            
    /* NEW: ATS Score Box */
    .ats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        color: white;
    }
    
    .ats-score-circle {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: white;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .ats-score-number {
        font-size: 3rem;
        font-weight: 700;
        color: #667eea;
        line-height: 1;
    }
    
    .ats-score-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 600;
        margin-top: 0.3rem;
    }
    
    .ats-content {
        background: rgba(255, 255, 255, 0.15);
        padding: 1.5rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        color: white;
        line-height: 1.8;
    }
    
    .ats-title {
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
        color: white;
    }
    
    /* Section headers */
    .section-header {
        color: #2c3e50;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Job cards */
    .job-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #e8e8e8;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .job-card:hover {
        border-color: #6b7fd7;
        box-shadow: 0 8px 24px rgba(107, 127, 215, 0.2);
        transform: translateY(-4px);
    }
    
    .job-title {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .job-company {
        color: #6b7fd7;
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .job-location {
        color: #7f8c8d;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    
    /* Button styling - matching the purple gradient */
    .linkedin-button {
        display: inline-block;
        background: linear-gradient(135deg, #6b7fd7 0%, #8b5fbf 100%);
        color: white !important;
        padding: 0.9rem 2.5rem;
        border-radius: 12px;
        text-decoration: none !important;
        font-weight: 600;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(107, 127, 215, 0.3);
        text-align: center;
    }
    
    .linkedin-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(107, 127, 215, 0.4);
        color: white !important;
    }
    
    /* Success banner */
    .success-banner {
        background: linear-gradient(135deg, #26de81 0%, #20bf6b 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 2rem 0;
        box-shadow: 0 4px 12px rgba(38, 222, 129, 0.3);
    }
    
    /* Keywords box */
    .keywords-box {
        background: linear-gradient(135deg, #e8f4fd 0%, #d4e9fc 100%);
        padding: 1.3rem;
        border-radius: 12px;
        border-left: 5px solid #6b7fd7;
        margin: 2rem 0;
        font-weight: 600;
        font-size: 1.1rem;
        color: #2c3e50;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #d0d0d0, transparent);
        margin: 3rem 0;
        border: none;
    }
    
    /* Streamlit button styling - matching the gradient */
    .stButton > button {
        background: linear-gradient(135deg, #6b7fd7 0%, #8b5fbf 100%);
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
        padding: 1rem 2rem;
        border-radius: 12px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(107, 127, 215, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(107, 127, 215, 0.4);
    }
    

    
    /* Input fields styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e8e8e8;
        padding: 0.8rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6b7fd7;
        box-shadow: 0 0 0 2px rgba(107, 127, 215, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Spinner color */
    .stSpinner > div {
        border-top-color: #6b7fd7 !important;
    }
            
    /* ✅ Make all text inside boxes black */
    .content-box,
    .content-box-summary,
    .content-box-gaps,
    .content-box-roadmap {
    color: black !important;
            }
    .content-box *,
    .content-box-summary *,
    .content-box-gaps *,
    .content-box-roadmap * {
    color: black !important;
            }

</style>
""", unsafe_allow_html=True)

# Header matching the screenshot
st.markdown("""
<div class="header-container">
    <h1 class="header-title"><span style="font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji';">🤖</span> AI Job Analyzer</h1>
    <p class="header-subtitle">Find jobs that match your skills using AI-powered analysis</p>
</div>
""", unsafe_allow_html=True)

# Upload section in white container
#st.markdown('<div class="white-container">', unsafe_allow_html=True)
#st.markdown('<span class="section-label">Upload Your Resume</span>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
#st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    # Extract and analyze resume
    with st.spinner("🔍 Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("📝 Summarizing your resume..."):
        summary = ask_openai(
            f"Summarize this resume highlighting the skills, education, and experience: \n\n{resume_text}", 
            max_tokens=500
        )

    with st.spinner("🛠️ Finding skills gaps..."):
        gaps = ask_openai(
            f"Analyze this resume and highlight missing skills, certifications, and experiences needed for better job opportunities: \n\n{resume_text}", 
            max_tokens=400
        )

    with st.spinner("🚀 Career Growth Plan..."):
        roadmap = ask_openai(
            f"Based on this resume, suggest a career growth plan to improve this person's career prospects (Skills to learn, certifications needed, industry exposure): \n\n{resume_text}", 
            max_tokens=400
        )
     # NEW: ATS Score Analysis
    with st.spinner("📈 Calculating ATS Score..."):
        ats_analysis = ask_openai(
            f"""Analyze this resume for ATS (Applicant Tracking System) compatibility and provide:
            1. An ATS score from 0-100
            2. Detailed explanation of the score
            3. Specific recommendations to improve ATS compatibility
            Consider these factors:
            - Keyword optimization
            - Formatting and structure
            - Section headers- Contact information
            - Contact information
            - File format compatibility
            - Use of standard fonts
            - Bullet points usage
            - Quantifiable achievements
            - Relevant skills placement
            Resume:
            {resume_text}
            Provide the response in this format:
            ATS Score: [0-100]
            Explanation:
            [Detailed explanation of why this score was given]
            Recommendations:
            [Specific actionable recommendations to improve the score]""", 
            max_tokens=600
        )
    
    # Display results
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ATS Score - Display FIRST
    st.markdown('<h2 class="section-header">📈 ATS Compatibility Score</h2>', unsafe_allow_html=True)
    
    # Extract the score from the response
    try:
        score_line = ats_analysis.split('\n')[0]
        ats_score = ''.join(filter(str.isdigit, score_line))
        if not ats_score:
            ats_score = "N/A"
    except:
        ats_score = "N/A"
    
    st.markdown(f"""
    <div class="ats-container">
        <div class="ats-score-circle">
            <div class="ats-score-number">{ats_score}</div>
            <div class="ats-score-label">ATS Score</div>
        </div>
        <div class="ats-content">
            {ats_analysis.replace('ATS Score: ' + ats_score, '').strip()}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    # Resume Summary
    st.markdown('<h2 class="section-header">📑 Resume Summary</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-box content-box-summary"><p class="content-text">{summary}</p></div>', unsafe_allow_html=True)
    
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    # Skill Gaps
    st.markdown('<h2 class="section-header">🛠️ Skills Gaps & Missing Areas</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-box content-box-gaps"><p class="content-text">{gaps}</p></div>', unsafe_allow_html=True)
    
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    # Career Growth Plan
    st.markdown('<h2 class="section-header">🚀 Career Growth Plan</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-box content-box-roadmap"><p class="content-text">{roadmap}</p></div>', unsafe_allow_html=True)
    
    # Success message
    st.markdown('<div class="success-banner">✅ Analysis Completed Successfully!</div>', unsafe_allow_html=True)
    
    # Before/After Improvement Suggestions
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">💡 Resume Improvement Suggestions</h2>', unsafe_allow_html=True)
    
    if st.button("🔍 Get Improvement Suggestions"):
        with st.spinner("🤖 Analyzing improvement areas..."):
            improvements = get_improvement_suggestions(resume_text)
            st.session_state.improvements = improvements
    
    if 'improvements' in st.session_state:
        st.markdown(get_formatted_issues_html(st.session_state.improvements['current_issues']), unsafe_allow_html=True)
        st.markdown(get_formatted_improvements_html(st.session_state.improvements['suggested_improvements']), unsafe_allow_html=True)
    
    # PDF Export
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📥 Export Analysis</h2>', unsafe_allow_html=True)
    
    # Generate PDF
    pdf_buffer = generate_analysis_pdf(
        summary=summary,
        ats_score=ats_score,
        ats_analysis=ats_analysis,
        gaps=gaps,
        roadmap=roadmap,
        keywords=st.session_state.get('keywords_extracted', ''),
        jobs=st.session_state.get('jobs_list', []),
        improvements=st.session_state.get('improvements', None)
    )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="📥 Download Analysis as PDF",
        data=pdf_buffer,
        file_name=f"resume_analysis_{timestamp}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    # Job recommendations button
    if st.button("🔎 Get Job Recommendations"):
        with st.spinner("🤖 Extracting job keywords..."):
            keywords = ask_openai(
                f"Based on this resume summary, suggest the best job titles and keywords for searching jobs. Give a comma-separated list only, no explanation.\n\nSummary: {summary}",
                max_tokens=100
            )
            search_keywords_clean = keywords.replace("\n", "").strip()
            st.session_state.keywords_extracted = search_keywords_clean
        
        # Display extracted keywords
        st.markdown(f'<div class="keywords-box">🎯 Extracted Job Keywords: {search_keywords_clean}</div>', unsafe_allow_html=True)
        
        # Fetch from BOTH sources
        # with st.spinner("🔍 Fetching jobs from LinkedIn and other websites..."):
        with st.spinner("🔍 Fetching jobs from Jobs websites..."):
            # In your app.py, when calling the functions:
            #linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean, location="Saudi Arabia", rows=10)
            rapidapi_jobs = fetch_rapidapi_jobs(search_keywords_clean, location="Saudi Arabia", rows=10)
            st.session_state.jobs_list = rapidapi_jobs
            
            # Save to analytics
            # Extract skill gaps from the gaps text
            gap_lines = [line.strip('- •').strip() for line in gaps.split('\n') if line.strip().startswith(('-', '•'))]
            keyword_list = search_keywords_clean.split(',')[:10]
            
            try:
                save_analysis(
                    ats_score=int(ats_score) if ats_score and str(ats_score).isdigit() else 0,
                    skill_gaps=gap_lines[:10],
                    keywords=keyword_list,
                    job_count=len(rapidapi_jobs)
                )
            except Exception as e:
                print(f"Error saving analytics: {e}")

        
        # Display LinkedIn Jobs
        # st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        # st.markdown('<h2 class="section-header">💼 LinkedIn Jobs</h2>', unsafe_allow_html=True)
        
        # if linkedin_jobs:
        #     for job in linkedin_jobs:
        #         print("LinkedIn Job Link:", job.get("link"))
        #         job_title = job.get('title', 'No Title')
        #         job_company = job.get('companyName', 'Unknown Company')
        #         job_location = job.get('location', 'Location not specified')
        #         job_link = job.get('link', '#')

        #                 # ✅ Fix: ensure full LinkedIn URL
        #         job_link = job.get('link', '').strip()
        #         if job_link.startswith("/"):
        #              job_link = f"https://www.linkedin.com{job_link}"
        #         elif not job_link.startswith("http"):
        #             job_link = f"https://{job_link}


        #         st.markdown(f"""
        #         <div class="job-card">
        #             <div class="job-title">{job_title}</div>
        #             <div class="job-company">{job_company}</div>
        #             <div class="job-location">📍 {job_location}</div>
        #             <a href="{job_link}" target="_blank" class="linkedin-button">View Job on LinkedIn →</a>
        #         </div>
        #         """, unsafe_allow_html=True)
        # else:
        #     st.info("ℹ️ No LinkedIn jobs found.")
        
        
        # Display RapidAPI Jobs
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">🌐 Jobs Recommendation </h2>', unsafe_allow_html=True)
  
        
        if rapidapi_jobs:
            for job in rapidapi_jobs:
                job_title = job.get('job_title', 'No Title')
                job_company = job.get('employer_name', 'Unknown Company')
                job_location = f"{job.get('job_city') or ''}, {job.get('job_country') or ''}".strip(', ') or "Location not specified"
                job_link = job.get('job_apply_link', '#')
                
                st.markdown(f"""
                <div class="job-card">
                    <div class="job-title">{job_title}</div>
                    <div class="job-company">{job_company}</div>
                    <div class="job-location">📍 {job_location}</div>
                    <a href="{job_link}" target="_blank" class="linkedin-button">View Job →</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ No RapidAPI jobs found.")

else:
    # Show placeholder message when no file uploaded
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #95a5a6;">
        <p style="font-size: 1.2rem;">Upload your resume above to get started with AI-powered job matching</p>
    </div>
    """, unsafe_allow_html=True)


