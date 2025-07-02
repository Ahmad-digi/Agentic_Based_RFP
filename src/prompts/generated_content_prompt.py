import json
import logging

def generated_content_p(agent_1_json: dict) -> str:
    try:
        # Validate that agent_1_json is a dictionary
        if not isinstance(agent_1_json, dict):
            logging.error(f"Invalid input to generated_content_p: {type(agent_1_json)}")
            raise ValueError("Input to generated_content_p must be a dictionary")

        # Serialize JSON with proper escaping to avoid f-string issues
        json_str = json.dumps(agent_1_json, indent=2, ensure_ascii=False)

        # Construct the prompt using a triple-quoted f-string
        prompt = f"""
You are a senior business proposal writer for a top-tier technology consulting firm.

You will receive a JSON object containing structured information extracted from an RFP or client requirements document. Your task is to generate a comprehensive, professionally persuasive set of solutions for each requirement in the JSON. Each solution should be actionable, tailored to the requirement, and aligned with industry best practices.

Instructions:
- For each top-level key in the JSON, create a solution entry that addresses the corresponding requirement.
- Each solution entry must include:
  - The original key name (as provided in the JSON).
  - The original value (the requirement description from the JSON).
  - A detailed, actionable solution that expands on the requirement with professional context, methodologies, and client-focused benefits.
- When a value is:
  - A string: Provide a solution in one or two paragraphs, incorporating industry best practices and persuasive language to demonstrate how the requirement will be met.
  - A list of strings: Address each item in the list with a specific solution, presented as bullet points or a summary paragraph with clear explanations.
  - A list of objects or a dictionary: Create detailed solutions for each nested element, using subsections, bullet points, or tables to organize the information clearly.
  - Nested or complex: Ensure all relevant details are addressed with tailored solutions, using multi-level sectioning or bullet points for clarity.
- For requirements related to "Company Profile", "Expertise", "Previous Experiences", "Technical Proposal", "Project Plan", "Training and Support Plan", or "Warranty Coverage", provide extensive detail, emphasizing strengths, methodologies, and value to the client.
- Incorporate any value propositions, certifications, methodologies, or unique selling points found in the JSON into the solutions, highlighting their relevance to the client's needs.
- If the JSON includes roles, resources, partners, or certifications, create dedicated solution subsections or tables to showcase these credentials and their benefits.
- Maintain a formal, client-centered, and persuasive tone suitable for executive stakeholders and decision-makers.
- Output the solutions in the following JSON format, ensuring all solutions are comprehensive and suitable for direct client submission:
{{
  "solutions": [
    {{
      "key": "<key>",
      "value": "<original value>",
      "solution": "<detailed, actionable solution>"
    }}
  ]
}}
- Do NOT include any instructions, explanations, or additional headings in the output—just the JSON object with the solutions.
- Ensure the solutions are as detailed and comprehensive as the information in the JSON allows.

Here is the JSON:
{json_str}

Now, generate the solutions in the specified JSON format:
"""
        return prompt

    except Exception as e:
        logging.error(f"Error in generated_content_p: {str(e)}")
        raise ValueError(f"Failed to generate prompt: {str(e)}")