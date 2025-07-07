import time
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
load_dotenv()

AGENT_ENDPOINT = os.getenv('AZURE_PROJECT_ENDPOINT')
AGENT_ID = os.getenv('AZURE_AGENT_ID_3')

def slave_1_a(prompt: str) -> dict:
    if not AGENT_ENDPOINT or not AGENT_ID:
        raise RuntimeError("Agent endpoint or ID not configured.")

    client = AIProjectClient(
        endpoint=AGENT_ENDPOINT,
        credential=DefaultAzureCredential()
    )

    thread = client.agents.threads.create()
    client.agents.messages.create(thread_id=thread.id, role="user", content=prompt)
    run = client.agents.runs.create_and_process(thread_id=thread.id, agent_id=AGENT_ID)

    while run.status in ("queued", "in_progress"):
        time.sleep(1)
        run = client.agents.runs.get(thread_id=thread.id, run_id=run.id)

    messages = list(client.agents.messages.list(thread_id=thread.id))
    assistant_msgs = [m for m in messages if m.role == "assistant"]
    if not assistant_msgs:
        raise RuntimeError("No assistant message found.")

    last = assistant_msgs[-1]
    content_obj = last.content
    return {"response": content_obj.text if hasattr(content_obj, "text") else str(content_obj)}
