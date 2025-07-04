import json
import logging
def generated_content_p(agent_1_json: dict) -> str:
    try:
        if not isinstance(agent_1_json, dict):
            logging.error(f"Invalid input to generated_content_p: {type(agent_1_json)}")
            raise ValueError("Input to generated_content_p must be a dictionary")

        json_str = json.dumps(agent_1_json, indent=2, ensure_ascii=False)

        prompt = f"""
You are a senior business proposal writer for a top-tier technology consulting firm.

You will receive a JSON object containing structured information extracted from an RFP or client requirements document. Your task is to generate a comprehensive, professionally persuasive set of solutions for each requirement in the JSON. Each solution should be actionable, tailored to the requirement, and aligned with industry best practices.

Instructions:
- For every key in the JSON, create a corresponding solution entry.
- If the value is a string, number, or boolean, provide a solution in one or two paragraphs, and include a "solution" field at this level.
- If the value is a list of strings, output a list of objects, each with "value" (the item) and "solution" (the solution for that item).
- If the value is a list of objects, output a list of objects, each with all original fields, and for each field, include a "solution" for that field (only for leaf fields).
- If the value is a dictionary, output an object with the same keys, and for each key, include a "solution" for that key (only for leaf fields).
- **Do NOT include a "solution" field at any level where the value is a list or a dictionary. Only include a "solution" field for items where the value is a string, number, or boolean (leaf values).**
- Apply this logic recursively for all nested lists and dictionaries, so that every value at any level is paired with its own solution, but only at the leaf level.
- Do NOT skip any keys or items, and do NOT flatten or merge solutions for multiple items—each item must have its own solution.
- Do NOT include any instructions, explanations, or additional headings in the output—just the JSON object with the solutions.
- Maintain a formal, client-centered, and persuasive tone suitable for executive stakeholders and decision-makers.

### Output Format Example (for various input types):

If the input is:
{{
  "key1": "A string requirement",
  "key2": ["List item 1", "List item 2"],
  "key3": [
    {{"subkey": "Subitem 1"}},
    {{"subkey": "Subitem 2"}}
  ],
  "key4": {{
    "nested1": "Nested string",
    "nested2": ["Nested list item 1", "Nested list item 2"]
  }}
}}

Then the output should be:
{{
  "solutions": [
    {{
      "key": "key1",
      "value": "A string requirement",
      "solution": "A detailed solution for key1."
    }},
    {{
      "key": "key2",
      "value": [
        {{"value": "List item 1", "solution": "A solution for List item 1."}},
        {{"value": "List item 2", "solution": "A solution for List item 2."}}
      ]
    }},
    {{
      "key": "key3",
      "value": [
        {{"subkey": "Subitem 1", "solution": "A solution for Subitem 1."}},
        {{"subkey": "Subitem 2", "solution": "A solution for Subitem 2."}}
      ]
    }},
    {{
      "key": "key4",
      "value": {{
        "nested1": {{"value": "Nested string", "solution": "A solution for Nested string."}},
        "nested2": [
          {{"value": "Nested list item 1", "solution": "A solution for Nested list item 1."}},
          {{"value": "Nested list item 2", "solution": "A solution for Nested list item 2."}}
        ]
      }}
    }}
  ]
}}

**IMPORTANT:**  
- Do NOT include a "solution" field at any level where the value is a list or a dictionary. Only include "solution" for direct (leaf) values such as strings, numbers, or booleans.
- Do NOT include any instructions, explanations, or additional headings in the output—just the JSON object with the solutions.

Here is the JSON:
{json_str}

Now, generate the solutions in the specified JSON format:
"""
        return prompt

    except Exception as e:
        logging.error(f"Error in generated_content_p: {str(e)}")
        raise ValueError(f"Failed to generate prompt: {str(e)}")
