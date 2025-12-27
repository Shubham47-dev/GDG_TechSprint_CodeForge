import streamlit as st
import pdf_utils
import ai_logic
import visuals

st.title("JobFit AI - Resume Analyzer")
st.write("Team: GDG TechSprint Legends")


st.title("JobFit AI Resume Analyzer")

# 1. Member 1 creates the button
uploaded_file = st.file_uploader("Upload Resume")
job_desc = st.text_area("Paste Job Description")

if st.button("Analyze Resume"):
    
    # 2. Member 1 calls Member 2's function to handle the file
    # "Hey pdf_utils, run your 'get_text' function on this file!"
    resume_text = pdf_utils.get_text(uploaded_file) 

    # 3. Member 1 passes that text to Member 3's function
    # "Hey ai_logic, take this text and give me the score!"
    ai_result = ai_logic.analyze_with_gemini(resume_text, job_desc)

    # 4. Member 1 passes the score to Member 4's function
    # "Hey visuals, take this score and draw a chart!"
    st.subheader("Results")
    visuals.draw_gauge_chart(ai_result['score'])
    
    st.write(ai_result['feedback'])