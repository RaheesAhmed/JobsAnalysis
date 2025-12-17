import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mcp_client import (
    call_mcp_analyze_resume, 
    format_json_for_display, 
    get_sample_resume_names, 
    get_sample_resume
)
from src.helper import extract_text_from_pdf

# Page configuration
st.set_page_config(
    page_title="MCP Demo - AI Job Analyzer",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #CCCCFF;
    }
    
    .json-box {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 1.5rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        overflow-x: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .request-box {
        border-left: 5px solid #4a90e2;
    }
    
    .response-box {
        border-left: 5px solid #26de81;
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
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .success-badge {
        background: #26de81;
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .error-badge {
        background: #e74c3c;
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6b7fd7 0%, #8b5fbf 100%);
        color: white;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        border: none;
        box-shadow: 0 4px 12px rgba(107, 127, 215, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(107, 127, 215, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 style="margin: 0; font-size: 2.5rem;">🔍 MCP Communication Demo</h1>
    <p style="margin-top: 0.5rem; font-size: 1.1rem; opacity: 0.95;">
        See Model Context Protocol (MCP) in Action - Request & Response Viewer
    </p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
### 📖 What is MCP?

**Model Context Protocol (MCP)** is a standardized protocol for AI applications to communicate with external tools and services. 
This page demonstrates how our resume analyzer uses MCP to process requests and return responses.

**How it works:**
1. **Client** sends a request to the **MCP Server** with tool name and parameters
2. **MCP Server** processes the request using the appropriate tool
3. **Server** returns a structured JSON response with the results
4. You can see the **exact JSON communication** below!
""")

st.divider()

# Input Section
st.markdown("### 📝 Step 1: Provide Resume Text")

input_method = st.radio(
    "Choose input method:",
    ["Use Sample Resume", "Upload PDF", "Paste Text"],
    horizontal=True
)

resume_text = ""

if input_method == "Use Sample Resume":
    sample_names = get_sample_resume_names()
    selected_sample = st.selectbox("Select a sample resume:", sample_names)
    if st.button("Load Sample Resume"):
        resume_text = get_sample_resume(selected_sample)
        st.session_state.resume_text = resume_text
        st.success(f"✅ Loaded sample resume: {selected_sample}")

elif input_method == "Upload PDF":
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    if uploaded_file:
        with st.spinner("Extracting text from PDF..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            st.session_state.resume_text = resume_text
            st.success("✅ PDF text extracted successfully!")

else:  # Paste Text
    resume_text = st.text_area(
        "Paste your resume text here:",
        height=200,
        placeholder="Enter resume text here..."
    )
    if resume_text:
        st.session_state.resume_text = resume_text

# Display current resume text
if 'resume_text' in st.session_state and st.session_state.resume_text:
    with st.expander("📄 View Current Resume Text"):
        st.text_area("Resume:", st.session_state.resume_text, height=150, disabled=True)

st.divider()

# MCP Call Section
st.markdown("### 🚀 Step 2: Call MCP Server")

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    Click the button below to send an **MCP request** to analyze the resume.  
    The request and response will be displayed in JSON format.
    """)

with col2:
    test_button = st.button("🔬 Test MCP Server", type="primary", use_container_width=True)

if test_button:
    if 'resume_text' not in st.session_state or not st.session_state.resume_text:
        st.error("❌ Please provide resume text first!")
    else:
        with st.spinner("⏳ Calling MCP Server..."):
            # Call MCP server
            mcp_result = call_mcp_analyze_resume(st.session_state.resume_text)
            st.session_state.mcp_result = mcp_result
        
        st.success("✅ MCP Server responded!")

# Display MCP Communication
if 'mcp_result' in st.session_state:
    st.divider()
    st.markdown("### 📡 Step 3: View MCP Communication")
    
    mcp_result = st.session_state.mcp_result
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Tool Called", "analyze_resume")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Response Time", f"{mcp_result['duration_ms']}ms")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        status = "Success ✅" if mcp_result['success'] else "Error ❌"
        st.metric("Status", status)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        timestamp = mcp_result['timestamp'].split('T')[1].split('.')[0]
        st.metric("Time", timestamp)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Request & Response
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📤 MCP REQUEST (Client → Server)")
        request_json = format_json_for_display(mcp_result['request'])
        st.markdown(f'<div class="json-box request-box">{request_json}</div>', unsafe_allow_html=True)
        
        # Copy button
        st.download_button(
            label="📋 Copy Request JSON",
            data=request_json,
            file_name="mcp_request.json",
            mime="application/json",
            key="request_download"
        )
    
    with col2:
        st.markdown("#### 📥 MCP RESPONSE (Server → Client)")
        response_json = format_json_for_display(mcp_result['response'])
        st.markdown(f'<div class="json-box response-box">{response_json}</div>', unsafe_allow_html=True)
        
        # Copy button
        st.download_button(
            label="📋 Copy Response JSON",
            data=response_json,
            file_name="mcp_response.json",
            mime="application/json",
            key="response_download"
        )
    
    st.divider()
    
    # Explanation
    st.markdown("### 💡 Understanding the Communication")
    
    st.markdown("""
    **Request Structure:**
    - `jsonrpc`: Protocol version (2.0)
    - `id`: Unique request identifier
    - `method`: The MCP method being called (`tools/call`)
    - `params`:
      - `name`: Tool name (`analyze_resume`)
      - `arguments`: Input parameters for the tool
    
    **Response Structure:**
    - `result`: The tool's output (resume analysis)
      - `summary`: AI-generated resume summary
      - `skill_gaps`: Identified missing skills
      - `career_roadmap`: Career growth suggestions
      - `ats_score`: ATS compatibility score (0-100)
      - `job_keywords`: Suggested search keywords
    
    **This demonstrates:**
    - ✅ Client-Server communication using MCP
    - ✅ Structured JSON request/response format
    - ✅ Tool invocation through the MCP protocol
    - ✅ Real-time processing and response
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
    <p><strong>For Teacher Review:</strong> This page demonstrates our understanding and implementation of the Model Context Protocol (MCP).</p>
    <p>The exact JSON communication can be copied and included in documentation.</p>
</div>
""", unsafe_allow_html=True)
