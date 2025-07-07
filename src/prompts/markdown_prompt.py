import json

def markdown_agent_prompt(solutions: dict, requirements: dict) -> str:
    return f"""
You are a proposal formatting agent. Your task is to take the following solutions and requirements, and format them into a well-structured Markdown document. Use clear headings and bullet points for requirements.

Solutions:
{json.dumps(solutions, indent=2)}

Requirements:
{json.dumps(requirements, indent=2)}

Output only the Markdown document.
"""
