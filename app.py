import streamlit as st
import pdf_utils
import ai_logic
import visuals
import time
import altair as alt
import pandas as pd

st.set_page_config(
    page_title="JobFit AI | Smart Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)


def mock_ai_analysis(resume_text, job_desc):
    """Simulates Member 3's AI Analysis"""
    time.sleep(2) # Fake AI thinking
    return {
        "match_percentage": 48,
        "missing_keywords": ["Python", "Docker", "AWS", "Communication"],
        "found_count" : 2,
        "summary": "The candidate has strong technical skills but lacks cloud experience mentioned in the job description.",
        "ATS_Readability" : "Low",
        "soft_skill" : "string, explain briefly the required soft skills and what soft skill resume already has",
        "advice" : "string, briefly advice on how user can improve the score",
        "critical_gaps" : "string, explain the critical gap between what skill user has and what user is missing using the missing keyword you listed and how important it is for job"

    }

with st.container():
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.title("JobFit AI 📝")
        st.caption("AI-Powered Resume Optimization System")
    with col_b:
        st.metric(label="System Status", value="Online", delta="Ready")

with st.sidebar:
    st.caption("Powered by Google Gemini 1.5 Flash.")
    st.caption("We do not store your data.")
    st.caption("Built by CodeForge for GDG TechSprint.")
    with st.expander("ℹ️ How to use this app"):
        st.caption("""
        1. Paste the **Job Description** below.
        2. Upload your **Resume (PDF)** in the main area.
        3. Click **Analyze** to see your score.
        """)

with st.container(border=True):
    st.subheader("Data Inputs:")
    col_a,col_b = st.columns([1.25,1])
    with col_a:
        job_desc = st.text_area("Job Description: ",height = 150, placeholder = "Paste your Job Description here.")
        st.info("💡 Tip: Be specific! The AI matches your resume against this text.")

    with col_b:
        uploaded_file = st.file_uploader("Upload your Resume(PDF Only):", type = ["pdf"])
        if uploaded_file:
            st.write("✅ Resume uploaded successfully!📄")


if st.button("Analyze Resume Now", type="primary", use_container_width=True):

    if job_desc and uploaded_file:
        # Showing Spinner "
        with st.spinner("🔍 Reading PDF and consulting AI..."):
            
            resume_text = pdf_utils.get_text(uploaded_file)
            pg = pdf_utils.resume_len(uploaded_file)
            
            # (Later: ai_logic.analyze_resume(resume_text, job_desc))
            analysis = mock_ai_analysis(resume_text, job_desc)
            
        st.success("Analysis Complete!")

        with st.container(border = True):

            st.subheader("Result:")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
               
                st.metric(label = "Match Score", value=f"{analysis['match_percentage']}%", delta="Target: 80%")
            
            with col_b:
                if len(analysis['missing_keywords'])!=0:
                    st.metric(label = "Missing Keywords", value = len(analysis['missing_keywords']), delta = "Crucial", delta_color="inverse")
                elif len(analysis['missing_keywords'])==0:
                    st.metric(label = "Missing Keywords", value = len(analysis['missing_keywords']), delta = "Well Done")

            with col_c:
                st.markdown("### Verdict:")
                if analysis['match_percentage']>=75:
                    st.write("##### :green-background[✅ Great Match]")
                elif analysis['match_percentage']>=50:
                    st.write("##### :yellow-background[⚠️ Potential Match]")
                else:
                    st.write("##### :red-background[❌ Low Match]")
                if analysis['ATS_Readability'] == 'High':
                    st.markdown(f"###### ATS Readability: :green-background[{analysis['ATS_Readability']}]")
                elif analysis['ATS_Readability'] == 'Medium':
                    st.markdown(f"###### ATS Readability: :yellow-background[{analysis['ATS_Readability']}]")
                elif analysis['ATS_Readability'] == 'Low':
                    st.markdown(f"###### ATS Readability: :red-background[{analysis['ATS_Readability']}]")
            st.divider()
        
            col1, col2 = st.columns([1, 1.6])
            
            with col1:
                st.subheader("Resume Match Score")
                visuals.plot_gauge(analysis["match_percentage"])
                st.write("")
                st.divider()
                st.write("")

                visuals.plot_keyword_bar(analysis['found_count'],len(analysis['missing_keywords']))

                
            with col2:
                st.subheader("Analysis Report 📊")
                st.markdown("**🚨 Critical Gaps**")
                st.info(analysis['critical_gaps']) 
                st.divider()

                st.markdown("**🗣️ Soft Skills**")
                st.write(analysis['soft_skill'])
                st.divider()
    
                st.markdown("**💡 Key Advice**")
                st.success(analysis['advice']) 
                st.divider()
    
                st.markdown("**📝 Summary**")
                st.markdown(f">{analysis['summary']}")
                
        
            
        with st.expander("🔍 What AI extracted from your Resume"):
            st.write("Your Resume has", pg, "number of pages.")
            st.write(resume_text)
        with st.expander("🔍 What AI concluded"):
            st.write(analysis)

    elif uploaded_file and not job_desc:
        st.error("⚠️ Please paste the Job Description to start!")

    elif not uploaded_file and job_desc:
        st.error("⚠️ Please upload your Resume to start!")

    elif not uploaded_file and not job_desc:
        st.error("⚠️ Please paste the Job Description and Upload your Resume to start!")
