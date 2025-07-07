from src.prompts.markdown_prompt import markdown_p
from src.agents.markdown_agent import markdown_a

def markdown_fun(solutions: dict) -> str:
    prompt = markdown_p(solutions)
    response = markdown_a(prompt)
    return response.get("response", "")
