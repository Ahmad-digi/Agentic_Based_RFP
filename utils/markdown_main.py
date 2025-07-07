import json
import ast
from src.prompts.markdown_prompt import markdown_p
from src.agents.markdown_agent import markdown_a

def markdown_fun(solutions: dict) -> str:
    prompt = markdown_p(solutions)
    response = markdown_a(prompt)
    raw = response.get("response", "")

    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list) and parsed:
            return parsed[0]['text']['value']
        elif isinstance(parsed, dict) and 'text' in parsed:
            return parsed['text']['value']
        else:
            return str(parsed)
    except Exception:
        return raw
