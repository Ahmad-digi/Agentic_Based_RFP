def toc_generated_p(extracted_data: dict) -> str:
    """
    Generate a prompt for the TOC generation agent based on extracted RFP data.
    """
    return f"""
You are a highly intelligent assistant skilled in analyzing RFP (Request for Proposal) documents and generating professional, structured outputs.
Your task is to create a comprehensive Table of Contents (TOC) based on the provided extracted RFP content.

### Instructions:
- Read and interpret the structure and content of the RFP.
- Identify major sections (e.g., Project Overview, Scope of Work, Deliverables, Timeline, Evaluation Criteria, etc.).
- Under each major section, extract all relevant subsections and sub-subsections, maintaining proper hierarchical order.
- Format the Table of Contents using full numbering:
  - Main sections: "1. Section Title"
  - Subsections: "1.1. Subsection Title", and so on.
- Use clean, professional, title-cased headings (e.g., "Project Objectives", "Technology Stack").
- Represent nested structure using nested Python-style lists (for JSON serialization).

### Output Format (JSON):
Return only a "value" object in the exact structure below:
{{
  "table_of_contents": [
    "1. Section Title",
    [
      "1.1. Subsection Title",
      "1.2. Another Subsection",
      [
        "1.2.1. Sub-subsection Title"
      ]
    ],
    "2. Next Section"
  ]
}}

### Extracted Data:
{str(extracted_data)}
"""