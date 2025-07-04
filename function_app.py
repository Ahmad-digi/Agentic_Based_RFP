import logging
import json
import azure.functions as func

from utils.doc_intell_main import extract_data_from_rfp
from utils.res_req_yes_no_main import res_req_yes_no_fun
from utils.res_req_from_rfp_main import res_req_from_rfp_fun
from utils.seq_pick_generate_main import seq_pick_generate_fun

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="proposal", methods=["POST"])
def proposal_agent(req: func.HttpRequest) -> func.HttpResponse:
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

        extracted_data = extract_data_from_rfp(file_bytes, filename)
        parsed_data = json.loads(extracted_data)

        requirements_data = res_req_from_rfp_fun(parsed_data)
        requirements = requirements_data.get("requirements", {})

        solutions = {}
        for heading, req_data in requirements.items():
            # Main section content
            section_text = req_data.get("description", "")
            section_solution = seq_pick_generate_fun(section_text)

            solutions[heading] = {
                "content": section_solution.get("content", ""),
                "solution": section_solution.get("solution", "")
            }

            # Subsections
            subsections = req_data.get("subsections", {})
            if subsections:
                solutions[heading]["subsections"] = {}
                for sub_heading, sub_text in subsections.items():
                    sub_solution = seq_pick_generate_fun(sub_text)
                    solutions[heading]["subsections"][sub_heading] = {
                        "content": sub_solution.get("content", ""),
                        "solution": sub_solution.get("solution", "")
                    }

        # Step 4: Return final combined response
        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "requirements": requirements,
                "requirements_with_solutions": solutions
            }, indent=2),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.exception("Proposal agent processing failed.")
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "message": f"Internal Server Error: {str(e)}"
            }),
            status_code=500,
            mimetype="application/json"
        )
