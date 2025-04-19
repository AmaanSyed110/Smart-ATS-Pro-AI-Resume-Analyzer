import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from fpdf import FPDF
import base64
from datetime import datetime
import plotly.express as px
from streamlit_tags import st_tags
import time

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the best available Gemini model
def get_gemini_model():
    try:
        # Try to use Gemini 1.5 Pro if available
        return genai.GenerativeModel('gemini-1.5-pro-latest')
    except:
        # Fallback to Gemini Pro if 1.5 isn't available
        return genai.GenerativeModel('gemini-pro')

# Initialize session state
if 'previous_analyses' not in st.session_state:
    st.session_state.previous_analyses = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

# Core functions
def get_gemini_response(prompt):
    model = get_gemini_model()
    response = model.generate_content(prompt)
    return response.text

def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""  # Handle None returns
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def analyze_resume(job_title, jd, resume_text, key_skills):
    prompt = f"""
    ROLE: You are an expert ATS (Applicant Tracking System) analyst and professional resume reviewer with 
    15+ years experience in tech recruiting (software engineering, data science, cloud, etc.).

    TASK: Analyze this resume against the job description and provide detailed, actionable feedback.

    JOB TITLE: {job_title if job_title else 'Not specified'}
    
    JOB DESCRIPTION:
    {jd}
    
    RESUME CONTENT:
    {resume_text}

    {f"KEY SKILLS TO PRIORITIZE: {', '.join(key_skills)}" if key_skills else ""}

    ANALYSIS REQUIREMENTS:
    1. First determine if the resume is generally appropriate for this job (Y/N)
    2. Calculate an ATS match score (0-100%) considering:
       - Keyword matching (hard skills)
       - Experience relevance
       - Education alignment
       - Overall presentation quality
    3. Provide detailed feedback in this EXACT structure:

    ### 🎯 ATS Match Score: [X]%
    (Show percentage prominently)

    ### 🔍 Missing Keywords:
    (Bullet list of important missing keywords/skills)

    ### 📈 Top Improvement Recommendations:
    (Prioritized list of actionable improvements)

    ### ⚠️ Potential Red Flags:
    (Any concerning elements that might hurt chances)

    ### 💎 Strengths to Highlight:
    (What's working well in this resume)

    ### 📝 Suggested Resume Edits:
    (Specific text suggestions for improvement)

    FORMATTING:
    - Use clear markdown formatting
    - Include emojis for visual scanning
    - Be constructive but honest
    - Prioritize by impact on hiring chances
    """
    return get_gemini_response(prompt)

def generate_improved_resume(analysis, original_text):
    prompt = f"""
    ORIGINAL RESUME:
    {original_text}

    ANALYSIS AND IMPROVEMENT SUGGESTIONS:
    {analysis}

    TASK: Rewrite this resume incorporating all improvement suggestions while:
    - Maintaining the original's best qualities
    - Adding missing keywords naturally
    - Fixing all identified issues
    - Optimizing for ATS parsing
    - Keeping professional tone

    OUTPUT: The full improved resume text ready for PDF generation.
    """
    return get_gemini_response(prompt)

# UI Setup
st.set_page_config(page_title="Smart ATS Pro", page_icon="📄", layout="wide")

# Sidebar
with st.sidebar:
    st.title("Smart ATS Pro")
    st.markdown("""
    **Boost your resume's ATS performance**  
    Get AI-powered analysis and improvement suggestions  
    """)
    
    st.divider()
    st.markdown("### Previous Analyses")
    for i, analysis in enumerate(st.session_state.previous_analyses):
        with st.expander(f"{analysis.get('job_title', 'Analysis')} - {analysis.get('date', '')}"):
            if st.button(f"Load Analysis {i+1}", key=f"load_{i}"):
                st.session_state.current_analysis = analysis
            if st.button(f"❌", key=f"delete_{i}"):
                st.session_state.previous_analyses.pop(i)
                st.rerun()

# Main Content
st.title("📄 Smart ATS Pro Resume Analyzer")
st.markdown("### Get AI-powered feedback to optimize your resume for Applicant Tracking Systems")

with st.expander("ℹ️ How to use this tool", expanded=True):
    st.write("""
    1. 📋 Paste the job description
    2. 📤 Upload your resume (PDF)
    3. 🔍 Add important skills from the JD (optional)
    4. 🚀 Click "Analyze My Resume"
    5. 💡 Review your personalized feedback
    6. 🔄 Generate an improved version (optional)
    """)

# Input Form
with st.form(key='analysis_form'):
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.text_input("🔍 Job Title/Position", 
                                placeholder="e.g. 'Senior Data Scientist'")
        jd = st.text_area("📋 Job Description", 
                         height=300,
                         placeholder="Paste the full job description here...")
        
    with col2:
        uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", 
                                       type="pdf",
                                       help="We recommend PDF format for best ATS compatibility")
        key_skills = st_tags(
            label='🏷️ Important Skills from JD (optional)',
            text='Press enter to add more',
            value=[],
            suggestions=['Python', 'Machine Learning', 'AWS', 'SQL', 'React', 'Docker', 'Kubernetes']
        )
    
    submitted = st.form_submit_button("🚀 Analyze My Resume", type="primary")

# Results Display
if submitted and uploaded_file is not None and jd.strip() != "":
    with st.spinner("🔍 Analyzing your resume (this may take 20-30 seconds)..."):
        start_time = time.time()
        resume_text = input_pdf_text(uploaded_file)
        
        # Store analysis in session state
        analysis_entry = {
            'job_title': job_title,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'jd': jd,
            'resume_text': resume_text,
            'key_skills': key_skills
        }
        
        # Run analysis
        analysis_result = analyze_resume(job_title, jd, resume_text, key_skills)
        analysis_entry['result'] = analysis_result
        analysis_entry['time'] = time.time() - start_time
        
        st.session_state.current_analysis = analysis_entry
        st.session_state.previous_analyses.append(analysis_entry)
        
        st.success("Analysis complete!")
        st.balloons()

if st.session_state.current_analysis:
    analysis = st.session_state.current_analysis
    
    # Extract match score for visualization
    match_score = 0
    if "### 🎯 ATS Match Score:" in analysis['result']:
        try:
            match_score = int(analysis['result'].split("### 🎯 ATS Match Score:")[1].split("%")[0])
        except:
            pass
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📝 Full Analysis", "✨ Resume Builder"])
    
    with tab1:
        st.subheader("Quick Overview")
        
        # Score visualization
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ATS Match Score", f"{match_score}%")
        with col2:
            st.metric("Analysis Time", f"{analysis['time']:.1f} seconds")
        with col3:
            st.metric("Resume Length", f"{len(analysis['resume_text'].split())} words")
        
        # Score gauge
        fig = px.bar(x=[match_score], y=["Match"], 
                    text=[f"{match_score}%"], 
                    orientation='h',
                    color_discrete_sequence=["#4CAF50"] if match_score > 75 
                            else ["#FFC107"] if match_score > 50 
                            else ["#F44336"])
        fig.update_layout(showlegend=False, 
                         xaxis_range=[0,100],
                         height=100,
                         margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        # Quick summary
        if "### 💎 Strengths to Highlight:" in analysis['result']:
            st.subheader("✅ Strengths")
            strengths = analysis['result'].split("### 💎 Strengths to Highlight:")[1].split("###")[0]
            st.markdown(strengths)
        
        if "### 🔍 Missing Keywords:" in analysis['result']:
            st.subheader("⚠️ Missing Keywords")
            missing = analysis['result'].split("### 🔍 Missing Keywords:")[1].split("###")[0]
            st.markdown(missing)
    
    with tab2:
        st.subheader("Detailed Analysis Report")
        st.markdown(analysis['result'])
        
        # Skill matching visualization (if skills were provided)
        if analysis['key_skills']:
            st.subheader("🔧 Skill Match Analysis")
            skill_prompt = f"""
            Analyze how well these required skills appear in the resume:
            REQUIRED SKILLS: {", ".join(analysis['key_skills'])}
            
            RESUME TEXT: {analysis['resume_text']}
            
            For each skill, indicate:
            - Presence (Yes/Partial/No)
            - Where it appears (section/context)
            - Strength of evidence
            
            Format as a markdown table with columns: Skill | Presence | Evidence | Strength
            """
            
            with st.spinner("Analyzing skill matches..."):
                skill_analysis = get_gemini_response(skill_prompt)
                st.markdown(skill_analysis)
    
    with tab3:
        st.subheader("AI-Powered Resume Builder")
        
        if st.button("🔄 Generate Improved Resume", type="primary"):
            with st.spinner("✨ Creating enhanced resume (this may take 30-60 seconds)..."):
                improved_text = generate_improved_resume(analysis['result'], analysis['resume_text'])
                
                st.subheader("Improved Resume Preview")
                st.text_area("Edited Content", improved_text, height=400)
                
                # PDF Generation
                st.subheader("Download Options")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📥 Download as Text",
                        data=improved_text,
                        file_name="improved_resume.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    # Create PDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
                    pdf.set_font("DejaVu", size=11)
                    
                    # Add improved text to PDF
                    for line in improved_text.split('\n'):
                        pdf.cell(0, 10, txt=line, ln=1)
                    
                    # Generate download link
                    pdf_output = pdf.output(dest='S')
                    b64 = base64.b64encode(pdf_output).decode()
                    
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="improved_resume.pdf">📥 Download as PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)

elif submitted:
    if not uploaded_file:
        st.error("Please upload your resume")
    if not jd.strip():
        st.error("Please paste the job description")

# Footer
st.divider()
st.caption("""
ℹ️ Smart ATS Pro uses Google's Gemini 1.5 AI to analyze resumes.  
For best results, provide complete job descriptions and properly formatted resumes.
""")