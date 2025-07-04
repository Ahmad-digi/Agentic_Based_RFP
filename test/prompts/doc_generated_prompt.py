import json
def doc_generated_p(requirements_json, toc_json, solutions_json):
    return f"""
You are an expert business proposal writer. You will receive three JSON objects:
1. Extracted client requirements.
2. A structured table of contents (TOC) for the proposal.
3. Detailed solutions for each requirement.

Your task:
- Write a professional, comprehensive business proposal document for an executive audience.
- Use the TOC to structure the document.
- For each section/subsection in the TOC, use the most relevant requirements and solutions (match by section names/keys if possible).
- Integrate requirements and solutions smoothly into the narrative, not as raw JSON.
- Ensure the proposal is clear, persuasive, and client-focused.
- Output only the full proposal text (no explanations, no JSON).

Here are the three JSONs:
Requirements:
{json.dumps(requirements_json, indent=2, ensure_ascii=False)}

Table of Contents:
{json.dumps(toc_json, indent=2, ensure_ascii=False)}

Solutions:
{json.dumps(solutions_json, indent=2, ensure_ascii=False)}

Now write the full proposal, organized according to the TOC, integrating requirements and solutions as described.
"""
