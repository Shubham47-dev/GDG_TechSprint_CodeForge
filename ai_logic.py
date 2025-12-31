import streamlit as st 
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ ERROR: API Key is None! Check your .env file path.")
else:
    print(f"✅ API Key found! It starts with: {API_KEY[:5]}...")

genai.configure(api_key = API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash')

@st.cache_data

def analyze_resume(resume_text, job_desc):
    prompt_template = f"""
    Act as an expert ATS (Applicant Tracking System) and HR Manager.
    
    JOB DESCRIPTION:
    {job_desc}
    
    RESUME TEXT:
    {resume_text}
    
    TASK:
    Evaluate the resume against the job description.
    
    OUTPUT FORMAT (Strict JSON Only):
    Provide a valid JSON object with exactly these keys:
    {{
        "match_percentage": (integer between 0-100),
        "missing_keywords": (list of strings, strictly tech skills),
        "found_count": (integer, number of matching keywords found),
        "summary": (string, brief executive summary),
        "ATS_Readability": (string, strictly one of: "High", "Medium", "Low"),
        "soft_skill": (string, 1-2 sentences analyzing soft skills),
        "advice": (string, 1-2 actionable tip to improve the score),
        "critical_gaps": (string, 2-3 sentence explaining the biggest missing technical skill)
    }}
    """

    try:
        response = model.generate_content(prompt_template)
        
        raw_text = response.text.strip()
        
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "") 
            raw_text = raw_text.replace("```", "")

        result = json.loads(raw_text)
        
        if (type(result.get("match_percentage"))==str):
            result["match_percentage"] = result["match_percentage"].replace("%", "")
            result["match_percentage"] = int(result["match_percentage"])

            
        return result

        # If AI returns bad text that isn't JSON
    except json.JSONDecodeError:
        return {
            "match_percentage": 0,
            "missing_keywords": [],
            "found_count": 0,
            "summary": "Error parsing AI response. Please try again.",
            "ATS_Readability": "Low",
            "soft_skill": "None",
            "advice": "Please retry the analysis.",
            "critical_gaps": "System error evaluating resume."
        }
        
    except Exception as e:
        return {
            "match_percentage": 0,
            "missing_keywords": [],
            "found_count": 0,
            "summary": f"System Error: {str(e)}",
            "ATS_Readability": "Low",
            "soft_skill": "None",
            "advice": "Check your connection or API key.",
            "critical_gaps": "System error."
        }