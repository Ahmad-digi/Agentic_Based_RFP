import json

def markdown_p(solutions: dict) -> str:
    return f"""
You are a proposal formatting agent. Your task is to take the following solutions and convert them into a clean, well-structured Markdown document.

Instructions:
- Use `##` for top-level headings (e.g., "1. Introduction", "2. Scope of Work")
- Use `###` for subheadings, if any
- Preserve all text formatting (bold, lists, line breaks)
- Return only valid Markdown output. Do not return JSON or extra text.

Here is the solutions dictionary (heading → content):

{json.dumps(solutions, indent=2, ensure_ascii=False)}

Return only the Markdown document.
"""
