# CODE SUMMARY - AI Job Analyzer 🤖


---

## 📖 What Does This Project Do?

This is an **AI-powered resume analyzer** that helps job seekers:
1. Upload their resume (PDF)
2. Get AI analysis (summary, ATS score, skill gaps, career advice)
3. Get improvement suggestions
4. Find matching jobs
5. Export results as PDF
6. Compare two resumes
7. View analytics from all analyses

**Plus**: It has a special **MCP Demo page** to show the teacher how client-server communication works!

---

## 📁 Project Structure (Simple Breakdown)

```
JobsAnalysis/
├── app.py                    # Main page - Resume analysis
├── mcp_server.py             # MCP server (runs in background)
├── pages/                    # Additional pages (sidebar navigation)
│   ├── 2_🔍_MCP_Demo.py     # Shows MCP communication (IMPORTANT!)
│   ├── 3_📊_Analytics.py    # Charts and statistics
│   └── 4_⚖️_Compare.py      # Compare 2 resumes
├── src/                      # Helper functions
│   ├── helper.py            # PDF reading & OpenAI calls
│   ├── job_api.py           # Fetch jobs from internet
│   ├── analytics_manager.py # Save/load analytics data
│   ├── pdf_generator.py     # Create PDF reports
│   ├── mcp_client.py        # Talk to MCP server
│   └── improvement_suggestions.py # Before/after tips
├── data/
│   └── analytics.json       # Stores all analysis data
├── prompts/
│   └── system_instructions.md # How AI should behave
├── .env                     # Secret API keys (don't share!)
├── requirements.txt         # List of libraries needed
└── README.md               # How to use the project
```

---

## 🎯 Main Features (What You Built)

### 1️⃣ Resume Analysis (Home Page)
**File**: `app.py`

**What it does**:
- User uploads a PDF resume
- AI reads it and gives:
  - Summary (what's good about the resume)
  - ATS Score (0-100, how well it works with job systems)
  - Skill Gaps (what's missing)
  - Career Roadmap (what to learn next)

**How it works**:
1. Extract text from PDF using PyMuPDF
2. Send text to OpenAI (GPT-4o) with specific questions
3. Display results in colored boxes

---

### 2️⃣ MCP Request/Response Logger (MOST IMPORTANT!)
**File**: `pages/2_🔍_MCP_Demo.py`

**What it does**:
- Shows the teacher **exactly** how MCP works
- Displays JSON requests (what client sends)
- Displays JSON responses (what server sends back)

**Why it's important**:
- This is what the teacher wants to see!
- Proves you understand client-server communication
- You can screenshot this for documentation

**How it works**:
1. User loads a sample resume or uploads one
2. Clicks "Test MCP Server"
3. Client sends HTTP request to server (blue box)
4. Server processes and sends response (green box)
5. Shows time taken and status

---

### 3️⃣ Before/After Improvement Suggestions
**Files**: `app.py`, `src/improvement_suggestions.py`

**What it does**:
- Analyzes resume for problems
- Shows current issues (red box)
- Shows how to fix them (green box)

**Example**:
- Current Issue: "Missing quantifiable achievements"
- Suggestion: "Add numbers like 'Increased sales by 30%'"

---

### 4️⃣ PDF Export
**File**: `src/pdf_generator.py`

**What it does**:
- Creates a professional PDF report
- Includes all analysis results
- User can download and save it

**Uses**: ReportLab library to create PDFs

---

### 5️⃣ Analytics Dashboard
**Files**: `pages/3_📊_Analytics.py`, `src/analytics_manager.py`, `data/analytics.json`

**What it does**:
- Saves data every time someone analyzes a resume
- Shows:
  - Total resumes analyzed
  - Average ATS score
  - Most common skill gaps
  - Popular job keywords
- Charts and graphs

**Storage**: All data saved in `data/analytics.json` file

---

### 6️⃣ Resume Comparison
**File**: `pages/4_⚖️_Compare_Resumes.py`

**What it does**:
- Upload 2 resumes
- Compares them side-by-side
- Shows which one is better
- Highlights winner for each metric

---

## 🔧 How the Code Works (Simple Explanations)

### Main Files Explained:

#### `app.py` - Home Page
```python
# 1. User uploads PDF
uploaded_file = st.file_uploader("Upload Resume")

# 2. Extract text from PDF
resume_text = extract_text_from_pdf(uploaded_file)

# 3. Ask AI questions
summary = ask_openai("Summarize this resume: ..." + resume_text)
ats_analysis = ask_openai("Give ATS score: ..." + resume_text)
gaps = ask_openai("What's missing: ..." + resume_text)

# 4. Display results
st.markdown(f"Summary: {summary}")
st.markdown(f"ATS Score: {ats_score}")
```

#### `mcp_server.py` - Background Server
```python
# Define what the server can do
@mcp.tool()
def analyze_resume(resume_text: str):
    # Do analysis
    return {
        "summary": "...",
        "ats_score": 75,
        "gaps": "...",
        ...
    }

# Start server
mcp.run(transport="sse")  # SSE = Server-Sent Events over HTTP
```

#### `src/mcp_client.py` - Talk to Server
```python
# Send request to server
response = requests.post(
    "http://127.0.0.1:8000/mcp/v1/messages",
    json={
        "method": "tools/call",
        "params": {"name": "analyze_resume", "arguments": {...}}
    }
)

# Get response
result = response.json()
```

#### `src/helper.py` - Helper Functions
```python
# Extract text from PDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Ask OpenAI
def ask_openai(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

---

## 🔑 Important Concepts (Simple Explanations)

### What is MCP?
**MCP = Model Context Protocol**
- A way for AI apps to talk to tools/services
- Like a language that client and server both understand
- Uses JSON format (easy to read)

**Example**:
- Client says: "Hey server, analyze this resume"
- Server says: "OK, here's the analysis"

### What is JSON?
**JSON = JavaScript Object Notation**
- A way to organize data
- Looks like: `{"name": "John", "age": 25}`
- Easy for computers to read

### What is API?
**API = Application Programming Interface**
- A way for programs to talk to each other
- Like a restaurant menu - you order (request), chef makes it (processes), waiter brings it (response)

### What is SSE?
**SSE = Server-Sent Events**
- A way for server to send updates over HTTP
- Like a live stream of data

---

## 🌐 Libraries Used (What They Do)

| Library | What It Does |
|---------|-------------|
| **streamlit** | Makes the web pages/UI |
| **openai** | Talks to ChatGPT (GPT-4o) |
| **pymupdf** | Reads PDF files |
| **reportlab** | Creates PDF files |
| **requests** | Sends HTTP requests |
| **fastmcp** | MCP framework (makes server easy) |
| **python-dotenv** | Reads .env file (secret keys) |

---

## 🚀 How to Run (Step by Step)

### 1. Install Everything
```bash
uv sync
# OR
pip install -r requirements.txt
```

### 2. Add API Keys
Create `.env` file:
```
OPENAI_API_KEY=sk-your-key-here
RAPIDAPI_KEY=your-key-here
APIFY_API_TOKEN=your-token-here
```

### 3. Activate Virtual Environment
```bash
.venv\Scripts\activate
```

### 4. Start MCP Server (Terminal 1)
```bash
python mcp_server.py
```
You'll see: "🚀 Starting MCP Server"

### 5. Start Web App (Terminal 2)
```bash
streamlit run app.py
```
Browser opens at: http://localhost:8501

**Keep both terminals running!**

---


---

## 📊 Code Statistics

- **Total Files**: 15+
- **Total Lines**: ~2,500 lines
- **Languages**: Python, Markdown
- **Pages**: 4 (Home + 3 additional)
- **Helper Modules**: 6
- **External APIs**: 3 (OpenAI, RapidAPI, Apify)

---

## ❓ Common Questions

**Q: What if MCP server won't start?**
A: Make sure port 8000 isn't being used by another program

**Q: What if Streamlit won't start?**
A: Make sure virtual environment is activated (`.venv\Scripts\activate`)

**Q: Where is data stored?**
A: In `data/analytics.json` file (you can open it with notepad)

**Q: Can I change the port?**
A: MCP server runs on port 8000 by default (FastMCP controls this)

**Q: What if I get "Module not found"?**
A: Run `uv sync` again or `pip install -r requirements.txt`

