import PyPDF2 
import streamlit as st 

def get_text(uploaded_file):
    try:
        uploaded_file.seek(0)
        
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
        return text 
        
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None 

def resume_len(uploaded_file):
    try:
        uploaded_file.seek(0)
        
        reader = PyPDF2.PdfReader(uploaded_file)
        num_pages = len(reader.pages)
        return num_pages
        
    except Exception as e:
        return 0