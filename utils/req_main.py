import json
import ast
from src.agents.requirements_gather_agent import requirements_gather_a
from src.prompts.requirements_gather_prompt import requirements_gather_p

def process_requirements_extraction(full_text):
    extract_response = requirements_gather_a(requirements_gather_p(full_text))
    response_json = extract_response["response"]
    response_list = ast.literal_eval(response_json)
    extracted_value = response_list[0]["text"]["value"]
    parsed_json = json.loads(extracted_value)
    return parsed_json