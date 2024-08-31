import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv() ##load all env variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Gemini Pro response
def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
As an experienced Applicant Tracking System (ATS) analyst,
with profound knowledge in technology, software engineering, data science, machine learning, data analyst, full stack web development, cloud engineer, 
cloud developers, devops engineer and big data engineering, your role involves evaluating resumes against job descriptions.
Recognizing the competitive job market, provide top-notch assistance for resume improvement.

After evaluation, i want the response to be generated as:
1. Percentage match between the uploaded resume and job description (display only percentage match)
2. List of missing keywords or skills in the resume according to the job description
3. A summary of what can be improved in the uploaded resume to make it more perfect according to the job description
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)