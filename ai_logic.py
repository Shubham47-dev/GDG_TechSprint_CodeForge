import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load the secret environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Configure the AI Model
genai.configure(api_key=api_key)

def get_gemini_response(resume_text, job_description):
    """
    This function takes the resume text and JD, sends it to AI,
    and returns the AI's analysis.
    """
    
    # This is the "Model" - flash is faster and cheaper/free
    model = genai.GenerativeModel('gemini-2.5-flash')

    # This is the "Prompt" - The instructions you give the AI
    # You can change this text to make the AI smarter!
    prompt = f"""
    Act as a skilled ATS (Applicant Tracking System) scanner with a deep understanding of tech jobs. 
    Evaluate the resume based on the job description.
    
    Resume Text: {resume_text}
    Job Description: {job_description}
    
    I want the response in a single string having the structure:
    {{"JD Match":"%", "MissingKeywords":[], "Profile Summary":""}}
    """

    # Send data to AI
    response = model.generate_content(prompt)
    
    return response.text

# --- TESTING SECTION ---
# This part only runs when you run THIS file directly. 
# It helps you test without needing the other members.
if __name__ == "__main__":
    fake_resume = "I am a python developer with 3 years experience in AI."
    fake_jd = "Looking for a python developer who knows AI and Streamlit."
    
    print("Sending to AI... please wait...")
    result = get_gemini_response(fake_resume, fake_jd)
    print("AI Response:\n", result)
