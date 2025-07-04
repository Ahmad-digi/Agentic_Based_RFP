def requirements_gather_p(full_text: str) -> str:
    return f"""
You are a highly intelligent RFP (Request for Proposal) reader and analyzer.

You will receive raw extracted text from an RFP document. This text may be noisy or unstructured due to OCR processing, but your task is to interpret the content and extract all relevant information required to build a complete and professional proposal.

**Instructions:**
- Analyze the document end-to-end.
- Identify key pieces of information that are useful for responding to the RFP.
- Dynamically determine what should be included — no predefined fields are provided.
- Structure your output as a valid JSON object with keys and values representing the important data extracted from the RFP.
- Only include fields that exist or are reasonably inferred.
- Do **not** add explanations, code fences, or markdown formatting.

**Input:**
{full_text}

Output:
Only return the extracted information as a valid JSON object.
"""
