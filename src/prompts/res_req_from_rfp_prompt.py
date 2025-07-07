def res_req_from_rfp_p(extracted_data: str) -> str:
    return f"""
You are an expert RFP document parser. You will receive the full text of an RFP document.

Your task:
- Carefully analyze the document and extract three things, returning them in a single structured JSON object.

---

### 📋 OUTPUT JSON FORMAT:

{{
  "status": "yes" or "no",                // "yes" if a section titled RESPONSE REQUIREMENTS is found, otherwise "no"
  
  "rfp_headings": {{                      // A nested JSON of all major headings and subheadings with their actual content
    "1. Introduction": {{
      "content": "[Insert actual content under '1. Introduction']"
    }},
    "2. Scope of Work": {{
      "content": "[Insert actual content under '2. Scope of Work']"
    }},
    "3. Project Phases": {{
      "content": "[Insert content if exists under '3. Project Phases']",
      "3.1 Initiation": {{
        "content": "[Insert actual content under '3.1 Initiation']"
      }},
      "3.2 Architecture": {{
        "content": "[Insert actual content under '3.2 Architecture']"
      }}
    }},
    ...
  }},
  
  "requirements": {{
    // If RESPONSE REQUIREMENTS is found, extract its full content into a nested structured format, like:
    "Company Profile": {{
      "description": "[Insert the full relevant RFP content for Company Profile here]",
      "subsections": {{
        "Subsection Title": "[Insert the full relevant RFP content for this subsection here]"
      }}
    }},
    
    // If not found, use this default structure:
    "Executive Summary": {{
      "description": "[Insert the full relevant RFP content for Executive Summary here]"
    }},
    "Understanding Scope of Work": {{
      "description": "[Insert the full relevant RFP content for Understanding Scope of Work here]"
    }},
    "Proposed Solution": {{
      "description": "[Insert the full relevant RFP content for Proposed Solution here]"
    }},
    "Our Implementation Approach": {{
      "description": "[Insert the full relevant RFP content for Our Implementation Approach here]"
    }},
    "Management Approach": {{
      "description": "[Insert the full relevant RFP content for Management Approach here]"
    }},
    "Training and Knowledge Transfer Approach": {{
      "description": "[Insert the full relevant RFP content for Training and Knowledge Transfer Approach here]"
    }},
    "Support Approach": {{
      "description": "[Insert the full relevant RFP content for Support Approach here]"
    }},
    "Company Profile": {{
      "description": "[Insert the full relevant RFP content for Company Profile here]"
    }},
    "References": {{
      "description": "[Insert the full relevant RFP content for References here]"
    }}
  }}
}}

---

### 🧠 RULES:

- ✅ Use only **actual text** from the document. Do **not** hallucinate, summarize, or paraphrase.
- ✅ For every `"description"` and `"content"` field, **copy the full, literal content from the RFP** that is relevant to that heading or requirement.
- ✅ For `rfp_headings`, include all headings even if there are no requirements, and **store content in a "content" field inside each heading**.
- ✅ Maintain heading hierarchy and order.
- ✅ If you find RESPONSE REQUIREMENTS, extract it **exactly as structured**, with its titles and bullet points as sections/subsections.
- ❌ Do not rename, reword, or assume any headings that are not explicitly present.
- ❌ Do not summarize or paraphrase any RFP content.

---

### 📄 INPUT RFP DOCUMENT:
{extracted_data}
"""
