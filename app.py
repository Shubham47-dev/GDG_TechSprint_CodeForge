import streamlit as st
import pdf_utils
import ai_logic
import visuals

st.set_page_config(
    page_title="JobFit AI | Smart Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None

with st.container():
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.write("## **JobFit AI** | Smart ATS Resume Analyzer 📝")
        st.caption("AI-Powered Resume Optimization System")
    with col_b:
        st.metric(label="System Status", value="Online", delta="Ready")
    st.write("")

with st.sidebar:
    st.caption("Powered by Google Gemini 2.5 Flash.")
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

        with st.spinner("Reading PDF..."):
            resume_text = pdf_utils.get_text(uploaded_file)
            pg = pdf_utils.resume_len(uploaded_file)
        
        with st.spinner("Consulting Gemini AI..."):
            st.session_state.analysis_data = ai_logic.analyze_resume(resume_text, job_desc)
        st.success("Analysis Complete!")

    elif uploaded_file and not job_desc:
        st.error("⚠️ Please paste the Job Description to start!")

    elif not uploaded_file and job_desc:
        st.error("⚠️ Please upload your Resume to start!")

    elif not uploaded_file and not job_desc:
        st.error("⚠️ Please paste the Job Description and Upload your Resume to start!")
    
if st.session_state.analysis_data:
        
        analysis = st.session_state.analysis_data
        resume_text = pdf_utils.get_text(uploaded_file)

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
                    st.write("##### :green[✅ Great Match]")
                elif analysis['match_percentage']>=50:
                    st.write("##### :yellow[⚠️ Potential Match]")
                else:
                    st.write("##### :red[❌ Low Match]")
                if analysis['ATS_Readability'] == 'High':
                    st.markdown(f"###### ATS Readability: :green[{analysis['ATS_Readability']}]")
                elif analysis['ATS_Readability'] == 'Medium':
                    st.markdown(f"###### ATS Readability: :yellow[{analysis['ATS_Readability']}]")
                elif analysis['ATS_Readability'] == 'Low':
                    st.markdown(f"###### ATS Readability: :red[{analysis['ATS_Readability']}]")
            st.divider()

            col1, col2 = st.columns([1, 1.6])
            
            with col1:
                st.subheader("Resume Match Score")
                visuals.plot_gauge(analysis["match_percentage"])
                st.write("")
                st.divider()
                st.write("")

                visuals.plot_keyword_bar(analysis['found_count'],len(analysis['missing_keywords']))

                st.write("")
                st.divider()
                st.caption("Why this Score: ")

                st.markdown(f">_{analysis['wts']}_")

                
            with col2:
                st.subheader("Analysis Report 📊")
                st.write("")
                if(len(analysis['missing_keywords'])): 
                    st.markdown("**🧩 Missing Critical Skills**")
                    chip_style = """
                        <style>
                        .chip-container {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 8px;
                        margin-top: 5px;
                        margin-bottom: 20px;
                        }
                        .chip {
                            background-color: rgba(255, 75, 75, 0.15); /* Light red background */
                            color: #ff4b4b;                             /* Dark red text */
                            border: 1px solid #ff4b4b;
                            padding: 6px 14px;
                            border-radius: 20px;
                            font-size: 14px;
                            font-weight: 600;
                            font-family: sans-serif;
                            }
                        </style>
                        """
        
                    chips_html = '<div class="chip-container">'
                    for keyword in analysis['missing_keywords']:
                        chips_html += f'<div class="chip">{keyword}</div>'
                    chips_html += '</div>'
        
                        # Render it
                    st.markdown(chip_style + chips_html, unsafe_allow_html=True)

                else:
                    st.success("✅ No critical keywords missing!")
                
                st.divider()

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
                
        st.divider()
        
        with st.container():
            st.subheader("Raw Data Extracted: ")
        
            col1, col2 = st.columns(2)
        
            with col1:
                with st.expander("View Raw ATS Text (What ATS would sees)"):
                    st.info("This is how an ATS reads your resume. If your text looks scrambled here, the algorithms can't read your skills!")
                    st.code(resume_text, language='text')
        
            with col2:
                with st.expander("View Raw AI JSON"):
                    st.json(analysis)
        job_title_snippet = job_desc[:50] + "..." if len(job_desc) > 50 else job_desc
                
        report_content = f"""
        JOBFIT AI REPORT
        ----------------
        Match Score: {analysis['match_percentage']}%
        Job Role: {job_title_snippet}

        MISSING SKILLS:
        {', '.join(analysis['missing_keywords'])}

        ADVICE:
        {analysis['advice']}

        Generated by CodeForge
        """
        st.markdown("""
            <style>
            div[data-testid="stDownloadButton"] > button {
                color: #e8f7f7ff;
                background: #8b5cf6;
                font-weight: bold;
            }
            </style>
        """, unsafe_allow_html=True)

        st.download_button(
            label="Download Full Report ",
            data=report_content,
            file_name="JobFit_Analysis.txt",
            mime="text/plain",
            use_container_width=True
        )
