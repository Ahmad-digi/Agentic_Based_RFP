import logging
import json
import os
import io
import ast
from datetime import datetime
import streamlit as st
from docx import Document
from markdown import markdown as md_to_html
from bs4 import BeautifulSoup

# Import your utility functions
from utils.document_intelligence_main import extract_data_from_rfp
from utils.res_req_from_rfp_main import res_req_from_rfp_fun
from utils.orchestrate_main import master_slave_solution_generation
from src.prompts.markdown_prompt import markdown_p
from src.agents.markdown_agent import markdown_a

LOG_DIR = "log"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_json_to_log(data, prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.json"
    filepath = os.path.join(LOG_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filepath

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
            code_text = element.text
            doc.add_paragraph(code_text, style='Intense Quote')
        elif element.text and element.text.strip():
            doc.add_paragraph(element.text)

    doc.save(buffer)
    buffer.seek(0)
    return buffer

def markdown_fun(solutions: dict) -> str:
    prompt = markdown_p(solutions)
    response = markdown_a(prompt)
    raw = response.get("response", "")

    # Robust extraction from agent output
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list) and parsed:
            return parsed[0]['text']['value']
        elif isinstance(parsed, dict) and 'text' in parsed:
            return parsed['text']['value']
        else:
            return str(parsed)
    except Exception:
        return raw

def process_rfp_file(file):
    try:
        # Step 0: Validate file upload
        if not file:
            st.error("No file uploaded.")
            return

        filename = file.name
        file_bytes = file.read()

        # Step 1: Extract text from file using Azure Document Intelligence
        logging.info("Starting Step 1: Document intelligence extraction.")
        extracted_data = extract_data_from_rfp(file_bytes, filename)
        parsed_data = json.loads(extracted_data)
        logging.info("Step 1 complete: Document intelligence extraction done.")
        save_json_to_log(parsed_data, "docintell")

        # Step 2: Extract RFP headings and response requirements
        logging.info("Starting Step 2: Extracting RFP headings and requirements.")
        extraction_result = res_req_from_rfp_fun(parsed_data)
        status = extraction_result.get("status", "no")
        rfp_headings = extraction_result.get("rfp_headings", {})
        requirements = extraction_result.get("requirements", {})
        logging.info("Step 2 complete: RFP headings and requirements extracted.")
        save_json_to_log(extraction_result, "extraction")

        # Step 3: Master-slave agent solution generation
        logging.info("Starting Step 3: Generating solutions.")
        solutions = master_slave_solution_generation(rfp_headings, requirements)
        logging.info("Step 3 complete: Solutions generated.")
        save_json_to_log(solutions, "solutions")

        # Step 4: Convert solutions to Markdown
        logging.info("Starting Step 4: Generating Markdown.")
        markdown_content = markdown_fun(solutions)
        logging.info("Step 4 complete: Markdown generated.")
        save_json_to_log({"markdown": markdown_content}, "markdown")

        # Step 5: Validate Markdown by converting to DOCX
        logging.info("Validating Markdown by converting to DOCX.")
        docx_buffer = append_markdown_to_docx(markdown_content)
        logging.info("Markdown validation complete.")

        # Step 6: Display Markdown output and download DOCX
        st.success("Markdown generation and validation successful!")
        st.markdown(markdown_content)
        st.download_button(
            label="Download DOCX",
            data=docx_buffer.getvalue(),
            file_name="proposal.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        logging.exception("RFP processing failed.")
        st.error(f"Internal Server Error: {str(e)}")

def main():
    st.title("RFP Markdown Generator")
    st.write("Upload a PDF file to generate Markdown output and download as DOCX.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        process_rfp_file(uploaded_file)

if __name__ == "__main__":
    main()
