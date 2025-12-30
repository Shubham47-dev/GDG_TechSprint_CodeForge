# pdf_utils.py
import PyPDF2


def extract_text_from_pdf(uploaded_file):
    """
    This function takes a PDF file and returns its text as a string.
    """
    try:
        # 1. Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        # 2. Create an empty string to hold the text
        text = ""

        # 3. Loop through every page in the PDF
        for page in pdf_reader.pages:
            # Extract text from the page and add it to our string
            text += page.extract_text()

        return text

    except Exception as e:
        # If something goes wrong, print the error
        return str(e)  #
