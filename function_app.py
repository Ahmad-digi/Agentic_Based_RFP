import logging
import json
import azure.functions as func
from utils.doc_intell_main import extract_data_from_rfp
from utils.req_main import process_requirements_extraction
from utils.toc_main import process_toc_generation
from utils.gen_main import process_proposal_generation

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
@app.route(route="proposal", methods=["POST"])
def proposal_agent(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files.get("file")
        if not file:
            return func.HttpResponse("No file uploaded", status_code=400)
        filename = file.filename
        file_bytes = file.read()

        doc_intell_response = extract_data_from_rfp(file_bytes, filename)
        parsed = json.loads(doc_intell_response)
        full_text = parsed.get("content", "")

        parsed_json = process_requirements_extraction(full_text)
        toc_structured = process_toc_generation(parsed_json)
        formatted_solutions = process_proposal_generation(parsed_json)

        return func.HttpResponse(
            json.dumps({
                "agent_response": parsed_json,
                "table_of_contents": toc_structured["table_of_contents"],
                "generated_solutions": formatted_solutions
            }, indent=2, ensure_ascii=False),
            status_code=200,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        logging.exception(f"Agent processing failed: {str(e)}")
        return func.HttpResponse(
            f"Internal Server Error: {str(e)}",
            status_code=500
        )