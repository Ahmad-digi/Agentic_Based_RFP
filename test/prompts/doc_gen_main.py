import ast
from test.prompts.doc_generated_agent import doc_generated_a
from test.prompts.doc_generated_prompt import doc_generated_p
def process_doc_generation(requirements_json, toc_json, solutions_json):
    prompt = doc_generated_p(requirements_json, toc_json, solutions_json)
    response = doc_generated_a(prompt)
    response_1 = ast.literal_eval(response["response"])
    proposal_value_1 = response_1[0]["text"]["value"]
    return proposal_value_1
