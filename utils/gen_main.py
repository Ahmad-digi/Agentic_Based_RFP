import json
import ast
import re
from src.agents.generated_content_agent import generated_content_a
from src.prompts.generated_content_prompt import generated_content_p

def process_proposal_generation(parsed_json):
    proposal_prompt = generated_content_p(parsed_json)
    proposal_response = generated_content_a(proposal_prompt)
    proposal_json = proposal_response["response"]
    proposal_list = ast.literal_eval(proposal_json)
    proposal_value = proposal_list[0]["text"]["value"]

    formatted_solutions = []
    
    solutions_json = json.loads(proposal_value)
    solutions = solutions_json.get("solutions", [])
    if not isinstance(solutions, list):
        return []
    for sol in solutions:
        value = sol.get("value")
        if isinstance(value, str):
            tuple_pattern = r"^$'([^']+)',\s*($.*?$|\S+)$$"
            match = re.match(tuple_pattern, value.strip())
            if match:
                try:
                    list_value = ast.literal_eval(match.group(2))
                    value = list_value if isinstance(list_value, list) else value
                except Exception:
                    pass
        formatted_solutions.append({
            "key": sol.get("key"),
            "value": value,
            "solution": sol.get("solution")
        })
    return formatted_solutions