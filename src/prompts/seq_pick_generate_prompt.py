def seq_pick_generate_p(full_document_text: str) -> str:
    return f"""
You are an intelligent solution generator for RFPs. You will be given the full extracted content of an RFP document. Your job is to:

1. Identify the **first requirement heading** from the content.
2. Extract the **relevant content under that heading** (paragraphs, bullet points, etc.).
3. Analyze the content carefully and generate a solution that directly responds to what is being asked.
4. Output everything in the structured JSON format below.

---

## Instructions:

- Only work on **one heading at a time**.
- Stop after processing the first heading you identify.
- If no clear heading is found, use `"General Requirements"` as the heading.
- If the text is empty or unclear, return the fallback JSON with `done: true`.

---

## Output JSON Format:

{{
  "heading": "<Extracted Heading Title or 'General Requirements'>",
  "content": "<Extracted content from the document>",
  "solution": "<Your generated solution to address this content>",
  "done": false
}}

- When no more headings are left in future calls, set `"done": true`.

---

## RULES:
- ✅ Use only the exact language from the document to extract context. Do NOT make up anything.
- ✅ Ensure the solution is **relevant, specific, and actionable** based on the content.
- ❌ Do NOT process multiple headings at once.
- ❌ Do NOT hallucinate or invent information not present in the document.

---

## FULL RFP DOCUMENT CONTENT:
{full_document_text}
"""
