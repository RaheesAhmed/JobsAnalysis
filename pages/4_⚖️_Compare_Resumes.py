import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.helper import extract_text_from_pdf, ask_openai

# Page configuration
st.set_page_config(
    page_title="Resume Comparison - AI Job Analyzer",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #CCCCFF;
    }
    
    .header-container {
        background: linear-gradient(135deg, #6b7fd7 0%, #8b5fbf 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 12px rgba(107, 127, 215, 0.3);
    }
    
    .resume-box {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        height: 100%;
    }
    
    .winner-badge {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #2c3e50;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
    }
    
    .comparison-table {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 style="margin: 0; font-size: 2.5rem;">⚖️ Resume Comparison</h1>
    <p style="margin-top: 0.5rem; font-size: 1.1rem; opacity: 0.95;">
        Compare Two Resumes Side-by-Side
    </p>
</div>
""", unsafe_allow_html=True)

# Instructions
st.markdown("""
### 📋 How to Use

Upload two resumes to compare their strengths and weaknesses side-by-side.  
The system will analyze both resumes and show you which one performs better in key areas.
""")

st.divider()

# Two-column layout for uploads
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 Resume A")
    uploaded_file_a = st.file_uploader("Upload Resume A (PDF)", type=["pdf"], key="upload_a")
    
    if uploaded_file_a:
        with st.spinner("📝 Extracting text from Resume A..."):
            resume_text_a = extract_text_from_pdf(uploaded_file_a)
            st.session_state.resume_a = resume_text_a
            st.success("✅ Resume A loaded!")
        
        with st.expander("View Resume A Text"):
            st.text_area("", resume_text_a, height=150, disabled=True, key="text_a")

with col2:
    st.markdown("### 📄 Resume B")
    uploaded_file_b = st.file_uploader("Upload Resume B (PDF)", type=["pdf"], key="upload_b")
    
    if uploaded_file_b:
        with st.spinner("📝 Extracting text from Resume B..."):
            resume_text_b = extract_text_from_pdf(uploaded_file_b)
            st.session_state.resume_b = resume_text_b
            st.success("✅ Resume B loaded!")
        
        with st.expander("View Resume B Text"):
            st.text_area("", resume_text_b, height=150, disabled=True, key="text_b")

st.divider()

# Compare button
if 'resume_a' in st.session_state and 'resume_b' in st.session_state:
    if st.button("🔍 Compare Resumes", type="primary", use_container_width=True):
        
        # Analyze Resume A
        with st.spinner("🤖 Analyzing Resume A..."):
            summary_a = ask_openai(
                f"Summarize this resume highlighting the skills, education, and experience: \n\n{st.session_state.resume_a}", 
                max_tokens=500
            )
            
            gaps_a = ask_openai(
                f"List the top 5 missing skills or certifications in this resume (brief bullet points): \n\n{st.session_state.resume_a}", 
                max_tokens=300
            )
            
            ats_analysis_a = ask_openai(
                f"""Analyze this resume for ATS compatibility. Provide ONLY:
                ATS Score: [0-100]
                
                Resume: {st.session_state.resume_a}""", 
                max_tokens=200
            )
            
            try:
                score_line_a = ats_analysis_a.split('\n')[0]
                ats_score_a = int(''.join(filter(str.isdigit, score_line_a)))
            except:
                ats_score_a = 0
            
            skill_count_a = len([line for line in gaps_a.split('\n') if line.strip().startswith('-') or line.strip().startswith('•')])
        
        # Analyze Resume B
        with st.spinner("🤖 Analyzing Resume B..."):
            summary_b = ask_openai(
                f"Summarize this resume highlighting the skills, education, and experience: \n\n{st.session_state.resume_b}", 
                max_tokens=500
            )
            
            gaps_b = ask_openai(
                f"List the top 5 missing skills or certifications in this resume (brief bullet points): \n\n{st.session_state.resume_b}", 
                max_tokens=300
            )
            
            ats_analysis_b = ask_openai(
                f"""Analyze this resume for ATS compatibility. Provide ONLY:
                ATS Score: [0-100]
                
                Resume: {st.session_state.resume_b}""", 
                max_tokens=200
            )
            
            try:
                score_line_b = ats_analysis_b.split('\n')[0]
                ats_score_b = int(''.join(filter(str.isdigit, score_line_b)))
            except:
                ats_score_b = 0
            
            skill_count_b = len([line for line in gaps_b.split('\n') if line.strip().startswith('-') or line.strip().startswith('•')])
        
        # Store results
        st.session_state.comparison = {
            'a': {
                'summary': summary_a,
                'gaps': gaps_a,
                'ats_score': ats_score_a,
                'skill_count': skill_count_a
            },
            'b': {
                'summary': summary_b,
                'gaps': gaps_b,
                'ats_score': ats_score_b,
                'skill_count': skill_count_b
            }
        }
        
        st.success("✅ Comparison completed!")

# Display Comparison
if 'comparison' in st.session_state:
    comp = st.session_state.comparison
    
    st.divider()
    st.markdown("### 🏆 Comparison Results")
    
    # Quick Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 ATS Score")
        ats_winner = "A" if comp['a']['ats_score'] > comp['b']['ats_score'] else "B" if comp['b']['ats_score'] > comp['a']['ats_score'] else "Tie"
        st.metric("Resume A", f"{comp['a']['ats_score']}/100", delta=None)
        st.metric("Resume B", f"{comp['b']['ats_score']}/100", delta=None)
        if ats_winner != "Tie":
            st.markdown(f'<div class="winner-badge">🏆 Winner: Resume {ats_winner}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🛠️ Skill Gaps")
        gap_winner = "A" if comp['a']['skill_count'] < comp['b']['skill_count'] else "B" if comp['b']['skill_count'] < comp['a']['skill_count'] else "Tie"
        st.metric("Resume A", f"{comp['a']['skill_count']} gaps")
        st.metric("Resume B", f"{comp['b']['skill_count']} gaps")
        if gap_winner != "Tie":
            st.markdown(f'<div class="winner-badge">🏆 Better: Resume {gap_winner}</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("#### 🎯 Overall")
        # Calculate overall winner
        a_wins = 0
        b_wins = 0
        
        if comp['a']['ats_score'] > comp['b']['ats_score']:
            a_wins += 1
        elif comp['b']['ats_score'] > comp['a']['ats_score']:
            b_wins += 1
        
        if comp['a']['skill_count'] < comp['b']['skill_count']:
            a_wins += 1
        elif comp['b']['skill_count'] < comp['a']['skill_count']:
            b_wins += 1
        
        overall_winner = "A" if a_wins > b_wins else "B" if b_wins > a_wins else "Tie"
        
        st.metric("Resume A Wins", a_wins)
        st.metric("Resume B Wins", b_wins)
        if overall_winner != "Tie":
            st.markdown(f'<div class="winner-badge">🏆 Overall Winner: Resume {overall_winner}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="winner-badge">🤝 It\'s a Tie!</div>', unsafe_allow_html=True)
    
    # Detailed Comparison
    st.divider()
    st.markdown("### 📝 Detailed Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Resume A")
        st.markdown(f"""
        <div class="resume-box">
            <h4 style="color: #6b7fd7;">Summary</h4>
            <p style="line-height: 1.6;">{comp['a']['summary']}</p>
            
            <h4 style="color: #ff9f43;">Skill Gaps</h4>
            <p style="line-height: 1.6;">{comp['a']['gaps']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Resume B")
        st.markdown(f"""
        <div class="resume-box">
            <h4 style="color: #6b7fd7;">Summary</h4>
            <p style="line-height: 1.6;">{comp['b']['summary']}</p>
            
            <h4 style="color: #ff9f43;">Skill Gaps</h4>
            <p style="line-height: 1.6;">{comp['b']['gaps']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendations
    st.divider()
    st.markdown("### 💡 Recommendations")
    
    if overall_winner == "A":
        st.info("""
        **Resume A is stronger overall.** However, consider:
        - Resume B might have unique strengths in specific areas
        - Both resumes can be improved based on the skill gaps identified
        - Use the improvement suggestions on the Home page for both resumes
        """)
    elif overall_winner == "B":
        st.info("""
        **Resume B is stronger overall.** However, consider:
        - Resume A might have unique strengths in specific areas  
        - Both resumes can be improved based on the skill gaps identified
        - Use the improvement suggestions on the Home page for both resumes
        """)
    else:
        st.info("""
        **Both resumes are equally matched!** 
        - Consider the specific job requirements to choose
        - Both can be improved based on the skill gaps identified
        - Use the improvement suggestions on the Home page for both resumes
        """)

else:
    # Show placeholder
    if 'resume_a' not in st.session_state or 'resume_b' not in st.session_state:
        st.info("👆 Upload both resumes above to start the comparison!")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
    <p><strong>Tip:</strong> For the most accurate comparison, ensure both resumes are for similar job roles.</p>
</div>
""", unsafe_allow_html=True)
