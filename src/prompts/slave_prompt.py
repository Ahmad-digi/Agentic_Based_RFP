import json
def slave_p(heading: str, content: str, requirements: dict) -> str:
    return f"""
You are a proposal solution generation agent.

Your task is to write a detailed, client-focused solution narrative for the section: **{heading}**

Context:
{content}

Requirements for this section:
{json.dumps(requirements, indent=2) if requirements else "None"}

Instructions:
- Write a compelling and tailored solution based on the above context.
- Address all requirements (if provided).
- Avoid generic language—make it specific to the section and content.
- Output only the solution text.

Begin.
"""
