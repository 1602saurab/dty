from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
import fitz  # PyMuPDF
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Open the PDF with PyMuPDF
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        # Extract the first page
        first_page = pdf_document.load_page(0)

        # Convert the page to an image (optional, if you still need an image)
        pix = first_page.get_pixmap()
        img_byte_arr = pix.tobytes()

        # Encode to base64 (if needed for your specific task)
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")

### Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)..", type=['pdf'])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully....")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR with Tech Experience in the field of any one job role from Data Science, Full Stack, Web Development, Big Data Engineering, DEVOPS, Data Analyst. Your task is to review the provided resume against the job description for these profiles. 
Please share your professional evaluation on whether the candidate's profile align with Highlight the strengths and weaknesses of the applicant in relation to the specified job role.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full Stack, Web Development, Big Data Engineering, DEVOPS, Data Analyst, and deep ATS functionality. Your task is to evaluate the resume against the provided job description. 
Give me the percentage of match if the resume matches the job description. 
First the output should come as percentage, then keywords missing, and last final.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

