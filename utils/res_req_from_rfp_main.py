import json
import ast
from src.prompts.res_req_from_rfp_prompt import res_req_from_rfp_p
from src.agents.get_res_req_from_rfp_agent import get_res_req_from_rfp_a

def res_req_from_rfp_fun(parsed_json):
    toc_prompt = res_req_from_rfp_p(parsed_json)
    toc_response = get_res_req_from_rfp_a(toc_prompt)
    toc_json = toc_response["response"]
    toc_list = ast.literal_eval(toc_json)
    toc_str = toc_list[0]["text"]["value"]
    try:
        toc_structured = json.loads(toc_str)
    except Exception:
        toc_structured = ast.literal_eval(toc_str)
    return toc_structured