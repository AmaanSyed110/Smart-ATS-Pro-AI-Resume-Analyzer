# Smart ATS Pro - AI Resume Analyzer

## Overview 

Smart ATS Pro is an AI-powered resume optimization tool that helps job seekers:
- Analyze resume compatibility with Applicant Tracking Systems (ATS)
- Match resumes against specific job descriptions
- Generate actionable improvement suggestions
- Create ATS-optimized resume versions

Built with Google's Gemini AI, it provides recruiter-level analysis in seconds.


## Tech Stack 

**Frontend:**
- Streamlit (Python web framework)
- Plotly (Data visualization)
- Streamlit-Tags (Tag input component)

**Backend:**
- Google Gemini 1.5 Pro (AI analysis)
- PyPDF2 (PDF text extraction)
- FPDF (PDF generation)

**Supporting:**
- python-dotenv (Environment management)
- base64 (File encoding)

## Features

| Feature | Description |
|---------|-------------|
| **ATS Score** | 0-100% compatibility score with visual dashboard |
| **Keyword Gap Analysis** | Identifies missing hard skills from job descriptions |
| **AI-Powered Rewrites** | Generates improved resume versions with one click |
| **Skill Matching** | Visual comparison of resume skills vs job requirements |
| **Historical Tracking** | Saves previous analyses for comparison |
| **Multi-Format Export** | Download improved resumes as PDF or text |

## How it works
1. **Input Phase**:
   - Upload resume PDF
   - Paste job description
   - Add priority skills (optional)

2. **Analysis Phase**
   - PDF text extraction
   - Gemini AI processes JD vs resume
   - Generates match score and feedback
  
3. **Output Phase**
   - Visual dashboard with score
   - Detailed improvement suggestions
   - Option to generate improved resume

## How to run the project locally in your system
### Prerequisites
- Python 3.9+
  
- Gemini Pro model api key (Note: Ensure you have the necessary credentials and permissions to access the Gemini Pro API)
  
### Step-by-Step Setup
- ### Clone repository
  Open a terminal and run the following command to clone the repository:

```
git clone https://github.com/AmaanSyed110/Youtube-Video-Summarizer.git
```
- ### Set Up a Virtual Environment
It is recommended to use a virtual environment for managing dependencies:

```
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```
- ### Install Dependencies
Install the required packages listed in the ```requirements.txt``` file
```
pip install -r requirements.txt
```

- ### Add Your Gemini API Key
Create a ```.env``` file in the project directory and add your Gemini API key:
```
GOOGLE_API_KEY=your_api_key_here
```
- ### Run the Application
Launch the Streamlit app by running the following command:
```
streamlit run app.py
```
