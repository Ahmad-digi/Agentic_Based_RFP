import json
import ast
from src.prompts.seq_pick_generate_prompt import seq_pick_generate_p
from src.agents.seq_pick_generate_agent import seq_pick_generate_a

def seq_pick_generate_fun(parsed_json):
    toc_prompt = seq_pick_generate_p(parsed_json)
    toc_response = seq_pick_generate_a(toc_prompt)
    toc_json = toc_response["response"]
    toc_list = ast.literal_eval(toc_json)
    toc_str = toc_list[0]["text"]["value"]
    try:
        toc_structured = json.loads(toc_str)
    except Exception:
        toc_structured = ast.literal_eval(toc_str)
    return toc_structured