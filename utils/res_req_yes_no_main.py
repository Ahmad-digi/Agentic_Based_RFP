import json
import ast
from src.prompts.res_req_yes_no_prompt import res_req_yes_no_p
from src.agents.res_req_yes_no_agent import res_req_yes_no_a

def res_req_yes_no_fun(parsed_json):
    toc_prompt = res_req_yes_no_p(parsed_json)
    toc_response = res_req_yes_no_a(toc_prompt)
    toc_json = toc_response["response"]
    toc_list = ast.literal_eval(toc_json)
    toc_str = toc_list[0]["text"]["value"]
    try:
        toc_structured = json.loads(toc_str)
    except Exception:
        toc_structured = ast.literal_eval(toc_str)
    return toc_structured