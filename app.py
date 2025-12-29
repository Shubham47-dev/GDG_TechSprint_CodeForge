import streamlit as st
import time

# ==========================================
# 1. PAGE CONFIGURATION
#    This makes the tab title look professional
# ==========================================
st.set_page_config(
    page_title="JobFit AI | Smart Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# 2. MOCK FUNCTIONS (The "Fake" Backend)
#    Delete these later when your teammates finish their work!
# ==========================================

def mock_pdf_extraction(file):
    """Simulates Member 2's PDF extraction"""
    time.sleep(1) # Fake processing time
    return "This is dummy text extracted from the PDF..."

def mock_ai_analysis(resume_text, job_desc):
    """Simulates Member 3's AI Analysis"""
    time.sleep(2) # Fake AI thinking
    return {
        "match_percentage": 72,
        "missing_keywords": ["Python", "Docker", "AWS", "Communication"],
        "summary": "The candidate has strong technical skills but lacks cloud experience mentioned in the job description."
    }

def mock_plot_gauge(score):
    """Simulates Member 4's Chart"""
    # A simple placeholder progress bar for now
    st.progress(score / 100)
    st.caption(f"Visuals Module will draw a Gauge Chart here. Score: {score}/100")

# ==========================================
# 3. THE UI LAYOUT (Your Work)
# ==========================================

with st.container():
    # We can put columns INSIDE a container!
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.title("JobFit AI 📝")
        st.caption("AI-Powered Resume Optimization System")
    with col_b:
        # A static metric just for looks
        st.metric(label="System Status", value="Online", delta="Ready")

# --- The Sidebar (Input 1: Job Description) ---
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

# --- Main Area (Input 2: Resume PDF) ---
with st.container(border=True):
    st.subheader("Data Inputs")
    col_a,col_b = st.columns([1,1])
    with col_a:
        job_desc = st.text_area("Job Description:", height = 150)
        st.info("💡 Tip: Be specific! The AI matches your resume against this text.")

    with col_b:
        uploaded_file = st.file_uploader("Upload your Resume(PDF Only):", type = ["pdf"])
        if uploaded_file:
            st.write("✅ Resume uploaded successfully!📄")



# --- The "Action" Button ---
if st.button("Analyze Resume Now", type="primary"):

    if job_desc and uploaded_file:
        # A. Show a spinner while "processing"
        with st.spinner("🔍 Reading PDF and consulting AI..."):
            
            # --- CALLING THE MOCK FUNCTIONS ---
            # (Later, you will change these to: pdf_utils.extract_text(uploaded_file))
            resume_text = mock_pdf_extraction(uploaded_file)
            
            # (Later: ai_logic.analyze_resume(resume_text, job_desc))
            analysis = mock_ai_analysis(resume_text, job_desc)
            
        # B. Display Results (Using Columns for a Pro Look)
        st.success("Analysis Complete!")
        
        col1, col2 = st.columns([1, 2]) # Left is smaller (1/3), Right is bigger (2/3)
        
        with col1:
            st.subheader("Match Score")
            # This calls the mock chart
            mock_plot_gauge(analysis["match_percentage"])
            st.metric(label="ATS Score", value=f"{analysis['match_percentage']}%", delta="Target: 80%")
            
        with col2:
            st.subheader("Analysis Report")
            st.write(f"**Summary:** {analysis['summary']}")
            
            st.write("**⚠️ Missing Keywords:**")
            # Create colorful tags for keywords
            for keyword in analysis["missing_keywords"]:
                st.markdown(f"- ❌ {keyword}")

    elif uploaded_file and not job_desc:
        st.error("⚠️ Please paste the Job Description to start!")

    elif not uploaded_file and job_desc:
        st.error("⚠️ Please upload your Resume to start!")

    elif not uploaded_file and not job_desc:
        st.error("⚠️ Please paste the Job Description and Upload your Resume to start!")