from concurrent.futures import ThreadPoolExecutor, as_completed
from src.prompts.slave_prompt import slave_p
from src.agents.slave_1_agent import slave_1_a
from src.agents.slave_2_agent import slave_2_a
from src.agents.slave_3_agent import slave_3_a
import ast


def flatten_headings(rfp_headings):
    items = []
    for heading, heading_info in rfp_headings.items():
        if isinstance(heading_info, dict):
            items.append((heading, heading_info.get("content", "")))
            for subheading, sub_info in heading_info.items():
                if subheading == "content":
                    continue
                if isinstance(sub_info, dict):
                    items.append((subheading, sub_info.get("content", "")))
        else:
            # If heading_info is just text (fallback)
            items.append((heading, heading_info))
    return items


def split_list(lst, n):
    """Split a list into n nearly equal parts"""
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def parse_agent_response(response_string: str) -> str:
    """
    Parses the agent response and extracts all 'text.value' fields.
    Returns a joined string of all extracted values.
    """
    try:
        parsed = ast.literal_eval(response_string)
        if isinstance(parsed, list):
            return "\n".join(
                item.get("text", {}).get("value", "")
                for item in parsed
                if isinstance(item, dict) and "text" in item
            ).strip()
        elif isinstance(parsed, dict):
            return parsed.get("text", {}).get("value", "").strip()
        else:
            return str(parsed)
    except Exception as e:
        return f"[Unparsable response] {response_string}"


def process_chunk(chunk, requirements, agent_func):
    solutions = {}
    for heading, content in chunk:
        reqs = requirements.get(heading, {})
        prompt = slave_p(heading, content, reqs)
        try:
            response = agent_func(prompt)
            raw_resp = response.get("response", "")
            clean_resp = parse_agent_response(raw_resp)
            solutions[heading] = clean_resp
        except Exception as e:
            solutions[heading] = f"[ERROR] {str(e)}"
    return solutions


def master_slave_solution_generation(rfp_headings, requirements):
    all_items = flatten_headings(rfp_headings)
    agent_funcs = [slave_1_a, slave_2_a, slave_3_a]
    chunks = split_list(all_items, len(agent_funcs))

    solutions = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(process_chunk, chunk, requirements, agent_funcs[i])
            for i, chunk in enumerate(chunks)
        ]
        for future in as_completed(futures):
            result = future.result()
            solutions.update(result)
    return solutions
