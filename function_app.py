import logging
import json
import azure.functions as func
from datetime import datetime
import os

from utils.document_intelligence_main import extract_data_from_rfp
from utils.res_req_from_rfp_main import res_req_from_rfp_fun
from utils.orchestrate_main import master_slave_solution_generation
from utils.markdown_main import markdown_fun

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

LOG_DIR = "log"
os.makedirs(LOG_DIR, exist_ok=True)

def save_json_to_log(data, prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.json"
    filepath = os.path.join(LOG_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filepath

@app.route(route="proposal", methods=["POST"])
def proposal_solutions_agent(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Step 0: Validate file upload
        file = req.files.get("file")
        if not file:
            return func.HttpResponse(
                json.dumps({"status": "error", "message": "No file uploaded."}),
                status_code=400,
                mimetype="application/json"
            )

        filename = file.filename
        file_bytes = file.read()

        # Step 1: Extract text from file using Azure Document Intelligence
        extracted_data = extract_data_from_rfp(file_bytes, filename)
        parsed_data = json.loads(extracted_data)
        logging.info("Step 1 complete: Document intelligence extraction done.")

        save_json_to_log(parsed_data, "docintell")

        # Step 2: Extract RFP headings and response requirements
        extraction_result = res_req_from_rfp_fun(parsed_data)
        status = extraction_result.get("status", "no")
        rfp_headings = extraction_result.get("rfp_headings", {})
        requirements = extraction_result.get("requirements", {})
        logging.info("Step 2 complete: RFP headings and requirements extracted.")

        save_json_to_log(extraction_result, "extraction")

        # Step 3: Master-slave agent solution generation
        solutions = master_slave_solution_generation(rfp_headings, requirements)
        logging.info("Step 3 complete: Solutions generated.")

        save_json_to_log(solutions, "solutions")

        # Step 4: Convert solutions to Markdown using another agent
        markdown = markdown_fun(solutions)
        logging.info("Step 4 complete: Markdown generated.")

        save_json_to_log({"markdown": markdown}, "markdown")

        # Step 5: Return JSON with all key pieces
        response_body = {
            "status": "success",
            "rfp_status": status,
            "rfp_headings": rfp_headings,
            "requirements": requirements,
            "solutions": solutions,
            "markdown": markdown
        }

        return func.HttpResponse(
            json.dumps(response_body, indent=2, ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.exception("Proposal solutions agent processing failed.")
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "message": f"Internal Server Error: {str(e)}"
            }),
            status_code=500,
            mimetype="application/json"
        )
