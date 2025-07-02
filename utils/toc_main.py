import json
import ast
from src.agents.toc_generated_agent import toc_generated_a
from src.prompts.toc_generated_prompt import toc_generated_p

def process_toc_generation(parsed_json):
    toc_prompt = toc_generated_p(parsed_json)
    toc_response = toc_generated_a(toc_prompt)
    toc_json = toc_response["response"]
    toc_list = ast.literal_eval(toc_json)
    toc_str = toc_list[0]["text"]["value"]
    try:
        toc_structured = json.loads(toc_str)
    except Exception:
        toc_structured = ast.literal_eval(toc_str)
    return toc_structured