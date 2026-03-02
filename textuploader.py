import streamlit as st
import pandas as pd  #read the csv and excel files
from docx import Document  #read Documents files
from PyPDF2 import PdfReader #read PDF files

st.set_page_config(layout="wide")#full screen covers not narrow layout

st.title("📂 Multi File Viewer")#title of the page

# Session storage
if "files" not in st.session_state: #reloads app every time user interacts
    st.session_state.files = {} #to store the files

# -------- FILE READ FUNCTIONS -------- #

def read_txt(file):
    return file.read().decode("utf-8")  #reading text files

def read_csv(file):  #reading csv file
    return pd.read_csv(file)  

def read_excel(file):  #reading excel files
    return pd.read_excel(file)

def read_docx(file):  #reading documents
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs]) 
    return text

def read_pdf(file): #reading pdf files
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# -------- FILE UPLOAD -------- #

uploaded_files = st.file_uploader(
    "Upload files",
    type=["txt", "pdf", "docx", "xlsx", "csv"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        name = file.name
        ext = name.split(".")[-1]

        try:
            if ext == "txt":
                data = read_txt(file)

            elif ext == "csv":
                data = read_csv(file)

            elif ext == "xlsx":
                data = read_excel(file)

            elif ext == "docx":
                data = read_docx(file)

            elif ext == "pdf":
                data = read_pdf(file)

            st.session_state.files[name] = data

        except Exception as e:
            st.error(f"Error reading {name}: {e}")

# -------- LAYOUT -------- #

left, right = st.columns([1, 3])

# Showing uploaded files
with left:
    st.subheader("📁 Uploaded Files")

    if st.session_state.files:
        selected_file = st.radio(
            "Select File",
            list(st.session_state.files.keys())
        )
    else:
        st.info("Upload files to view.")

# Preview of the uploaded files
with right:
    st.subheader("👀 File Preview")

    if st.session_state.files:

        content = st.session_state.files[selected_file]

        # DataFrame preview
        if isinstance(content, pd.DataFrame):
            st.dataframe(content, use_container_width=True)

        # Text preview
        else:
            st.text_area(
                "Content",
                content,
                height=500
            )