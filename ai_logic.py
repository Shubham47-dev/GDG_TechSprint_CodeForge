import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# 1. Load the API Key safely
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Configure the Model
# We use 'gemini-1.5-flash' because it's fast and free
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

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
        # B. Make the API Call
        response = model.generate_content(prompt_template)
        
        # C. Cleaning the Output (The "Safety Net")
        # Sometimes AI adds ```json ... ``` wrapper even if we tell it not to.
        # We must strip it to prevent crashes.
        raw_text = response.text.strip()
        
        # Remove markdown fences if present
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "").replace("```", "")
        
        # D. Parse JSON
        result = json.loads(raw_text)
        
        # Ensure match_percentage is an integer (sometimes AI gives "85%")
        if isinstance(result.get("match_percentage"), str):
            result["match_percentage"] = int(result["match_percentage"].replace("%", ""))
            
        return result

    except json.JSONDecodeError:
        # If AI returns bad text that isn't JSON
        return {
            "match_percentage": 0,
            "missing_keywords": ["Error parsing AI response"],
            "summary": "The AI analysis failed to generate a valid report. Please try again."
        }
        
    except Exception as e:
        # General API errors (no internet, bad key, etc.)
        return {
            "match_percentage": 0,
            "missing_keywords": ["Connection Error"],
            "summary": f"System Error: {str(e)}"
        }