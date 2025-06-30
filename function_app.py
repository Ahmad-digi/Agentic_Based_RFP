import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="invoice-ai", methods=["POST"])
def invoice_ai(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files.get("file")
        if not file:
            return func.HttpResponse("No file uploaded", status_code=400)
        
        file_bytes = file.read()

        full_text = ""
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

        if not full_text.strip():
            return func.HttpResponse("No text extracted from file", status_code=400)

        extract_prompt = call_extract_prompt(full_text)
        extract_response = call_extract_agent(extract_prompt)
        logging.info(f"Extract response: {extract_response}")

        try:
            response_json = ast.literal_eval(extract_response["response"])
            extracted_data = response_json[0]["text"]["value"]
        except Exception as e:
            logging.error(f"Error parsing extraction agent response: {str(e)}")
            return func.HttpResponse(
                "Invalid extraction agent response format",
                status_code=400
            )
        
        try:
            result_json = json.loads(extracted_data)
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing error: {str(e)}")
            return func.HttpResponse(
                "Invalid JSON format in extracted data",
                status_code=400
            )

        return func.HttpResponse(
            json.dumps(result_json),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.exception("Error processing invoice")
        return func.HttpResponse(
            f"Internal Server Error: {str(e)}",
            status_code=500
        )
