def res_req_from_rfp_p(extracted_data: dict) -> str:
    return f"""
You are a document parser. Your task is to extract structured response requirements from the given RFP document.

Check if the section or heading **'RESPONSE REQUIREMENTS'** exists in the document.

Respond ONLY in this JSON format:

{{
  "status": "yes" or "no",
  "message": "The phrase 'RESPONSE REQUIREMENTS' is present in the document." OR "The phrase 'RESPONSE REQUIREMENTS' is not present in the document.",
  "document_content": "<INSERT FULL ORIGINAL TEXT BELOW>",
  "requirements": {{
    "<Section Title>": {{
      "description": "<Exact bullet, line or paragraph taken from the document>",
      "subsections": {{
        "<Subsection Title>": "<Exact content from the document>",
        ...
      }}
    }},
    ...
  }}
}}

---

### RULES:

- ✅ If the section **'RESPONSE REQUIREMENTS' is present**:
  - Extract the section **title** and all associated content directly under or near it.
  - Maintain a nested structure for any bullets or grouped sub-items.
  - Do NOT make anything up. Only use what’s exactly written in the RFP.
  - If a section has no subsections, omit the `"subsections"` key or leave it as an empty dictionary.

- ❌ If the section **'RESPONSE REQUIREMENTS' is not found**:
  - Set `"status": "no"`.
  - Use this fallback `requirements` structure (keep descriptions as-is):

    {{
      "Executive Summary": {{
        "description": "Summarize the key points of the proposal."
      }},
      "Understanding Scope of Work": {{
        "description": "Explain your understanding of the scope of the work requested."
      }},
      "Proposed Solution": {{
        "description": "Provide a detailed description of the proposed solution."
      }},
      "Our Implementation Approach": {{
        "description": "Describe how you plan to implement the solution."
      }},
      "Management Approach": {{
        "description": "Describe how the project will be managed."
      }},
      "Training and Knowledge Transfer Approach": {{
        "description": "Explain how training and knowledge transfer will be conducted."
      }},
      "Support Approach": {{
        "description": "Describe your support model post-implementation."
      }},
      "Company Profile": {{
        "description": "Include information about your company's background and expertise."
      }},
      "References": {{
        "description": "List relevant references or case studies."
      }}
    }}

---

### RFP Document:
{extracted_data}
"""
