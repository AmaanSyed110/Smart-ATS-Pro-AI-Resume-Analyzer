# Applicant-Tracking-System-using-Gemini-Pro-LLM

## Overview
The Resume Applicant Tracking System using Gemini Pro LLM is designed to help students tailor their resumes according to specific job descriptions. By implementing advanced natural language processing capabilities, this system provides detailed feedback on how well a student's resume matches the requirements of a job, identifies any missing keywords or skills, and offers personalized recommendations for improvement.



## Tech Stack
- **Python**: The core programming language used for developing the backend logic and integrating with AI models.
  
- **Streamlit**: Framework for creating the interactive web interface where users can upload resumes, input job descriptions, and view the results.
  
- **Gemini Pro LLM**: The language model employed for analyzing resumes and job descriptions, providing insights such as percentage matching, missing keywords, and resume improvement recommendations.
  
- **Langchain**: A framework that facilitates the interaction with Gemini Pro LLM, optimizing language model performance and integrating additional tools as needed.

## Features
- **Percentage Matching:** Automatically calculate the percentage match between a student's resume and the job description. This feature helps students understand how closely their resume aligns with the job requirements and identify areas for improvement.

- **Missing Keywords or Skills:** Analyze the resume to identify any missing keywords or skills that are critical for the desired job. This feature highlights gaps in the resume, guiding students on what to add or emphasize to better meet the job criteria.

- **Resume Improvement Recommendations:** Provide personalized suggestions to enhance the resume based on the job description. These recommendations help students optimize their resumes by adding relevant skills, experiences, and keywords that increase their chances of getting noticed by recruiters.

## Requirements
- Python 3.10
  
- Gemini Pro model api key (Note: Ensure you have the necessary credentials and permissions to access the Gemini Pro API)
  
- Obtain API credentials from the makersuit platform.

- Create a file named .env in the project root directory.

- Add the following lines to .env:
  ```bash
   GOOGLE_API_KEY= "your_api_key"
   ```
