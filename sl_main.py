import streamlit as st
import requests
import io
import logging
from docx import Document
from markdown import markdown as md_to_html
from bs4 import BeautifulSoup

# Replace with your actual Azure Function URL
AZURE_FUNCTION_URL = "https://agentic-based-proposal-f0ejajfde9ghbnhn.eastus-01.azurewebsites.net/api/proposal"

# Utility: Convert Markdown to DOCX
def append_markdown_to_docx(markdown_text):
    buffer = io.BytesIO()
    doc = Document()
    html = md_to_html(markdown_text)
    soup = BeautifulSoup(html, "html.parser")

    for element in soup.contents:
        if element.name == "h1":
            doc.add_heading(element.text, level=1)
        elif element.name == "h2":
            doc.add_heading(element.text, level=2)
        elif element.name == "h3":
            doc.add_heading(element.text, level=3)
        elif element.name == "ul":
            for li in element.find_all("li"):
                doc.add_paragraph(li.text, style='ListBullet')
        elif element.name == "ol":
            for li in element.find_all("li"):
                doc.add_paragraph(li.text, style='ListNumber')
        elif element.name == "p":
            doc.add_paragraph(element.text)
        elif element.name == "pre":
            doc.add_paragraph(element.text, style='Intense Quote')
        elif element.text and element.text.strip():
            doc.add_paragraph(element.text)

    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Main logic to handle uploaded file
def process_rfp_file_via_functionapp(file):
    try:
        files = {"file": (file.name, file.getvalue(), "application/pdf")}
        with st.spinner("Sending file to Azure Function..."):
            response = requests.post(AZURE_FUNCTION_URL, files=files)

        if response.status_code != 200:
            st.error("FunctionApp error: " + response.text)
            return

        result = response.json()
        st.success("✅ File processed successfully!")

        # Display only Markdown
        markdown_content = result.get("markdown", "")
        st.subheader("📝 Generated Markdown")
        st.markdown(markdown_content)

        # Convert Markdown to DOCX
        docx_buffer = append_markdown_to_docx(markdown_content)

        # Offer download
        st.download_button(
            label="📥 Download Proposal DOCX",
            data=docx_buffer.getvalue(),
            file_name="generated_proposal.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        logging.exception("Processing failed.")
        st.error(f"❌ Error: {str(e)}")

# Streamlit UI
def main():
    st.title("📄 AI Proposal Generator (Agentic System)")
    st.write("Upload an RFP PDF. The Azure Function will analyze it and return a DOCX proposal.")

    uploaded_file = st.file_uploader("📤 Upload RFP (PDF only)", type=["pdf"])
    if uploaded_file:
        process_rfp_file_via_functionapp(uploaded_file)

if __name__ == "__main__":
    main()