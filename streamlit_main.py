import streamlit as st
import logging
import json
from utils.res_req_yes_no_main import req_req_fun
from utils.doc_intell_main import extract_data_from_rfp

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Set Streamlit page configuration
st.set_page_config(page_title="Proposal Agent", layout="wide")

def main():
    st.title("Proposal Agent: RFP Analysis")
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Upload RFP PDF")
        uploaded_file = st.file_uploader("", type=["pdf"], key="file_uploader")
        logging.debug(f"Uploaded file: {uploaded_file}")

        if st.button("Submit"):
            if uploaded_file is not None:
                try:
                    with st.spinner("Processing RFP and checking response requirements..."):
                        # Read file bytes and filename
                        file_bytes = uploaded_file.read()
                        filename = uploaded_file.name
                        logging.debug(f"Processing file: {filename}")

                        # Extract data from RFP
                        doc_intell_response = extract_data_from_rfp(file_bytes, filename)
                        parsed = json.loads(doc_intell_response)
                        full_text = parsed.get("content", "")
                        logging.debug(f"Extracted content length: {len(full_text)}")

                        # Prepare data for req_req_fun
                        parsed_data = {"content": full_text}

                        # Call req_req_fun to process with agent
                        agent_response = req_req_fun(parsed_data)
                        response_text = agent_response.get("response", "No valid response from agent.")
                        logging.debug(f"Agent response: {response_text}")

                    with col2:
                        # Display agent response
                        st.subheader("Agent Response")
                        st.markdown(response_text)

                        # Display extracted document intelligence data in an expander
                        st.subheader("Document Intelligence Output")
                        with st.expander("Extracted Document Data"):
                            st.json(parsed)

                except Exception as e:
                    logging.exception(f"Processing failed: {str(e)}")
                    st.error(f"Error processing file: {str(e)}. Check the terminal for detailed logs.")
            else:
                st.error("Please upload a PDF file before submitting.")

    with col2:
        if 'proposal_content' not in st.session_state or st.session_state.proposal_content is None:
            st.write("Agent response and document data will appear here after submission.")

if __name__ == "__main__":
    main()