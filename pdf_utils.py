import PyPDF2

def get_text(uploaded_file):
    """
    This function takes a PDF file and returns its text as a string.
    """
    try:
        # Reset file pointer to the beginning (important if you read the file twice)
        uploaded_file.seek(0)
        
        # 1. Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        
        # 2. Create an empty string to hold the text
        text = ""
        
        # 3. Loop through every page in the PDF
        for page in pdf_reader.pages:
            # Extract text from the page and add it to our string
            # We use 'or ""' to prevent errors if a page has no text
            text += page.extract_text() or ""
            
        return text

    except Exception as e:
        # If something goes wrong, return the error message
        return str(e)

def resume_len(uploaded_file):
    """
    This function returns the total number of pages in the PDF.
    """
    try:
        # Reset file pointer to the beginning
        uploaded_file.seek(0)
        
        # Create the reader object
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        
        # Return the length of the pages list
        return len(pdf_reader.pages)
        
    except Exception as e:
        return 0
        
