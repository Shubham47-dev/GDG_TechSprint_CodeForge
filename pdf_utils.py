import PyPDF2

# This function is what Member 1 is "calling"
def get_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text  # It sends the text back to Member 1