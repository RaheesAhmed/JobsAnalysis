# AI Job Analyzer 🤖

An AI-powered resume analysis and job recommendation system with **Model Context Protocol (MCP)** integration.

## 🌟 Features

### 1. **Resume Analysis** 📄
- Upload PDF resumes and get instant AI-powered analysis
- Resume summary with skills, education, and experience highlights
- ATS (Applicant Tracking System) compatibility score (0-100)
- Skills gaps and missing areas identification
- Personalized career growth roadmap

### 2. **MCP Request/Response Logger** 🔍 (Priority Feature)
- Live demonstration of MCP client-server communication
- View exact JSON requests and responses
- Sample resumes for quick testing
- Copy functionality for documentation
- Response time metrics

### 3. **Before/After Improvement Suggestions** 💡
- AI-generated resume improvement recommendations
- Current issues highlighting
- Actionable suggestions for enhancement
- ATS optimization tips

### 4. **PDF Export** 📥
- Professional PDF reports of analysis results
- Includes all analysis sections
- Job recommendations (if available)
- Improvement suggestions (if generated)
- Timestamped for record-keeping

### 5. **Analytics Dashboard** 📊
- Total resumes analyzed counter
- Average ATS score tracking
- Top skill gaps visualization
- Most frequent job keywords
- ATS score distribution chart

### 6. **Resume Comparison** ⚖️
- Side-by-side comparison of two resumes
- Winner determination across metrics
- Detailed analysis breakdown
- Overall scoring comparison

### 7. **Job Recommendations** 💼
- AI-powered job keyword extraction
- Integration with RapidAPI JSearch
- LinkedIn job scraping via Apify
- Direct application links

---

## 🏗️ Architecture

### MCP (Model Context Protocol)
This project demonstrates the implementation of MCP for AI tool communication:

```
Client (Streamlit UI)
    ↓
MCP Client (src/mcp_client.py)
    ↓ [JSON-RPC 2.0 over stdio]
MCP Server (mcp_server.py)
    ↓
Tools:
  - analyze_resume
  - analyze_resume_from_file
  - fetch_jobs
    ↓
External Services:
  - OpenAI GPT-4o
  - RapidAPI JSearch
  - Apify LinkedIn Scraper
```

### Application Structure

```
JobsAnalysis/
├── app.py                          # Main Streamlit app (Resume Analysis)
├── mcp_server.py                   # MCP server implementation
├── pages/                          # Multipage Streamlit app
│   ├── 2_🔍_MCP_Demo.py           # MCP Request/Response Logger
│   ├── 3_📊_Analytics.py          # Analytics Dashboard
│   └── 4_⚖️_Compare_Resumes.py   # Resume Comparison
├── src/
│   ├── helper.py                   # PDF extraction & OpenAI helpers
│   ├── job_api.py                  # Job fetching APIs
│   ├── analytics_manager.py        # Analytics data management
│   ├── pdf_generator.py            # PDF report generation
│   ├── mcp_client.py               # MCP client for communication
│   └── improvement_suggestions.py  # Before/After suggestions
├── data/
│   └── analytics.json              # Analytics data storage
├── prompts/
│   └── system_instructions.md      # AI system prompt
├── requirements.txt                # Python dependencies
└── pyproject.toml                  # Project metadata
```

---

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- pip or uv package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/Rofidah44/JobsAnalysis.git
cd JobsAnalysis
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or with uv:
```bash
uv sync
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-openai-api-key
APIFY_API_TOKEN=apify_api_your-token
RAPIDAPI_KEY=your-rapidapi-key
```

**Required API Keys:**
- **OpenAI API Key**: [Get it here](https://platform.openai.com/api-keys)
- **Apify Token**: [Sign up here](https://apify.com/)
- **RapidAPI Key**: [Get it here](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)

---

## 💻 Usage

### Running the Streamlit App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Running the MCP Server
```bash
python mcp_server.py
```

The MCP server runs on stdio transport and can be integrated with MCP-compatible clients like Claude Desktop.

---

## 📱 Application Pages

### 🏠 Home (Main Analysis)
1. Upload your resume (PDF format)
2. Wait for AI analysis to complete
3. View ATS score, summary, gaps, and roadmap
4. Click "Get Improvement Suggestions" for before/after tips
5. Download analysis as PDF
6. Click "Get Job Recommendations" to find matching jobs

### 🔍 MCP Demo
1. Choose input method (Sample Resume / Upload PDF / Paste Text)
2. Click "Test MCP Server"
3. View JSON request and response in formatted boxes
4. Copy JSON for documentation
5. See response time and status metrics

### 📊 Analytics
- View aggregated statistics from all analyses
- Explore ATS score distribution chart
- See top skill gaps bar chart
- Check most frequent job keywords
- Admin option to clear analytics data

### ⚖️ Compare Resumes
1. Upload two resumes (Resume A and Resume B)
2. Click "Compare Resumes"
3. View winner for each metric
4. See detailed analysis side-by-side
5. Get recommendations based on comparison

---

## 🔧 Configuration

### Model Settings
Default configuration uses:
- **Model**: GPT-4o
- **Temperature**: 0.5
- **Max Tokens**: 100-600 (varies by task)

To modify, edit `src/helper.py`:
```python
response = client.chat.completions.create(
    model="gpt-4o",  # Change model here
    temperature=0.5,  # Adjust creativity
    max_tokens=max_tokens
)
```

### Job Search Settings
Default location is "Saudi Arabia". To change:

In `app.py` (lines 470-471):
```python
rapidapi_jobs = fetch_rapidapi_jobs(
    search_keywords_clean, 
    location="Your Location",  # Change here
    rows=10
)
```

---

## 🧪 Testing the MCP Integration

### For Teacher Demonstration

**Step 1: Start the MCP Demo Page**
- Navigate to the MCP Demo page (🔍 icon in sidebar)
- Select "Use Sample Resume" → Choose "Software Engineer"
- Click "Load Sample Resume"

**Step 2: Test MCP Communication**
- Click "🔬 Test MCP Server"
- Wait for the response (should take 5-15 seconds)

**Step 3: Review Results**
- **Request JSON**: Shows the MCP request sent to the server
- **Response JSON**: Shows the structured response from tools
- **Metrics**: Response time, status, timestamp

**Step 4: Document for Review**
- Click "📋 Copy Request JSON" to save the request
- Click "📋 Copy Response JSON" to save the response
- Take screenshots of the displayed JSON boxes

### Expected Output Format

**Request Example:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "analyze_resume",
    "arguments": {
      "resume_text": "John Doe Software Engineer..."
    }
  }
}
```

**Response Example:**
```json
{
  "result": {
    "summary": "Experienced software engineer...",
    "skill_gaps": "Missing: AWS, Docker, Kubernetes...",
    "career_roadmap": "Suggested certifications...",
    "ats_score": "75",
    "job_keywords": "Software Engineer, Python, Full-Stack..."
  }
}
```

---

## 📊 Analytics Data Storage

Analytics are stored in `data/analytics.json`:

```json
{
  "analyses": [
    {
      "timestamp": "2025-12-18T00:51:38",
      "ats_score": 75,
      "skill_gaps": ["Python", "AWS", "Docker"],
      "keywords": ["Data Scientist", "ML Engineer"],
      "job_count": 10
    }
  ],
  "created_at": "2025-12-18T00:51:38",
  "version": "1.0"
}
```

---

## 🎓 College Project Notes

**For Teacher Review:**

1. **MCP Implementation**: See `mcp_server.py` for server-side and `src/mcp_client.py` for client-side
2. **Communication Flow**: Demonstrated on the MCP Demo page with JSON viewers
3. **Tools Exposed**: 
   - `analyze_resume`: Core resume analysis
   - `analyze_resume_from_file`: File-based analysis
   - `fetch_jobs`: Job recommendations
4. **Protocol**: Uses JSON-RPC 2.0 over stdio transport

**Key Technical Skills Demonstrated:**
- ✅ API Integration (OpenAI, RapidAPI, Apify)
- ✅ MCP Protocol Implementation
- ✅ Multi-page Web Application (Streamlit)
- ✅ Data Visualization (Charts, Metrics)
- ✅ PDF Generation (reportlab)
- ✅ JSON Data Storage
- ✅ Subprocess Communication

---

## 🐛 Troubleshooting

### Issue: "No module named 'reportlab'"
**Solution:**
```bash
pip install reportlab
```

### Issue: "MCP Server Timeout"
**Solution:**
- Check if `mcp_server.py` is accessible
- Ensure all dependencies are installed
- Try with shorter resume text

### Issue: "No jobs found"
**Solution:**
- Verify API keys in `.env`
- Check internet connection
- Try different keywords

### Issue: "Analytics not updating"
**Solution:**
- Ensure `data/` directory exists
- Check write permissions
- Verify `analytics.json` is not corrupted

---

## 📝 License

This project is created for educational purposes as a college project.

---

## 👥 Contributors

- **Rofidah44** - Initial work and MCP implementation

---

## 🙏 Acknowledgments

- OpenAI for GPT-4o API
- Streamlit for the web framework
- RapidAPI for job search API
- Apify for LinkedIn scraping
- Model Context Protocol team for the MCP standard

---

## 📧 Contact

For questions or issues, please open an issue on GitHub or contact the project maintainer.

---

**Last Updated**: December 18, 2025  
**Version**: 2.0 (with MCP and Analytics)
