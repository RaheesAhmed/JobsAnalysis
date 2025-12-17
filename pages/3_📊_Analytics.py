import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analytics_manager import (
    get_total_count,
    get_average_ats,
    get_top_skill_gaps,
    get_top_keywords,
    get_score_distribution,
    clear_analytics
)

# Page configuration
st.set_page_config(
    page_title="Analytics Dashboard - AI Job Analyzer",
    page_icon="📊",
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
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-left: 5px solid #6b7fd7;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #6b7fd7;
        margin: 0;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #7f8c8d;
        margin-top: 0.5rem;
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 style="margin: 0; font-size: 2.5rem;">📊 Analytics Dashboard</h1>
    <p style="margin-top: 0.5rem; font-size: 1.1rem; opacity: 0.95;">
        Insights from All Resume Analyses
    </p>
</div>
""", unsafe_allow_html=True)

# Get analytics data
total_resumes = get_total_count()
avg_ats = get_average_ats()
top_gaps = get_top_skill_gaps(5)
top_keywords = get_top_keywords(10)
score_dist = get_score_distribution()

# Check if there's data
if total_resumes == 0:
    st.info("""
    📭 **No Data Available Yet**
    
    The analytics dashboard will populate once you analyze resumes using the main page.
    
    **To get started:**
    1. Go to the Home page (🏠)
    2. Upload and analyze resumes
    3. Come back here to see the insights!
    """)
    st.stop()

# Key Metrics
st.markdown("### 📈 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="stat-number">{total_resumes}</div>
        <div class="stat-label">Total Resumes Analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="stat-number">{avg_ats}</div>
        <div class="stat-label">Average ATS Score</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    most_common_gap = top_gaps[0][0].title() if top_gaps else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="stat-number" style="font-size: 1.5rem;">{most_common_gap}</div>
        <div class="stat-label">Most Common Gap</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    top_keyword = top_keywords[0][0].title() if top_keywords else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="stat-number" style="font-size: 1.5rem;">{top_keyword}</div>
        <div class="stat-label">Top Job Keyword</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Charts Section
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 ATS Score Distribution")
    
    if any(score_dist.values()):
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Prepare data for bar chart
        score_ranges = list(score_dist.keys())
        counts = list(score_dist.values())
        
        st.bar_chart({
            "Score Range": score_ranges,
            "Count": counts
        }, x="Score Range", y="Count", color="#6b7fd7")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No ATS score data available yet.")

with col2:
    st.markdown("### 🛠️ Top Skill Gaps")
    
    if top_gaps:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Create horizontal bar chart data
        gap_names = [gap[0].title() for gap in top_gaps]
        gap_counts = [gap[1] for gap in top_gaps]
        
        # Display as table for better readability
        for i, (name, count) in enumerate(zip(gap_names, gap_counts), 1):
            progress = count / max(gap_counts) if gap_counts else 0
            st.markdown(f"""
            <div style="margin: 0.8rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                    <span style="font-weight: 600;">{i}. {name}</span>
                    <span style="color: #6b7fd7; font-weight: bold;">{count}</span>
                </div>
                <div style="background: #e0e0e0; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: linear-gradient(135deg, #6b7fd7 0%, #8b5fbf 100%); 
                                height: 100%; width: {progress*100}%; transition: width 0.3s;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No skill gap data available yet.")

st.divider()

# Top Job Keywords
st.markdown("### 🎯 Top Job Keywords")

if top_keywords:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Display keywords in a grid
    cols = st.columns(5)
    for i, (keyword, count) in enumerate(top_keywords):
        col_idx = i % 5
        with cols[col_idx]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e8f4fd 0%, #d4e9fc 100%);
                        padding: 1rem; border-radius: 10px; text-align: center;
                        margin-bottom: 0.5rem; border-left: 3px solid #6b7fd7;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #6b7fd7;">{count}</div>
                <div style="font-size: 0.9rem; color: #2c3e50;">{keyword.title()}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No keyword data available yet.")

st.divider()

# Admin Section
with st.expander("⚙️ Admin Actions"):
    st.warning("**Caution:** These actions cannot be undone!")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        **Clear All Analytics Data**  
        This will permanently delete all stored analysis data and reset the dashboard.
        """)
    
    with col2:
        if st.button("🗑️ Clear Data", type="secondary"):
            clear_analytics()
            st.success("✅ Analytics data cleared!")
            st.rerun()

# Footer
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem; margin-top: 2rem;">
    <p>Analytics are updated in real-time as new resumes are analyzed.</p>
    <p>Data is stored locally in <code>data/analytics.json</code></p>
</div>
""", unsafe_allow_html=True)
