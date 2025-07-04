# src/prompts/res_req_yes_no_prompt.py
def res_req_yes_no_p(extracted_data: dict) -> str:
    return f"""
    Scan the following document content and check if the phrase 'RESPONSE REQUIREMENTS' exists.

    Always return a JSON-formatted response with the following structure:
    {{
        "status": "yes" or "no",
        "message": "The phrase 'RESPONSE REQUIREMENTS' is present in the document." 
                   or "The phrase 'RESPONSE REQUIREMENTS' is not present in the document.",
        "document_content": [Full extracted document content]
    }}

    Document content:
    {extracted_data}
    """
