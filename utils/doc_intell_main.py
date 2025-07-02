import os
import json
import numpy as np
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    reshaped_bounding_box = np.array(bounding_box).reshape(-1, 2)
    return ", ".join(["[{}, {}]".format(x, y) for x, y in reshaped_bounding_box])

def extract_data_from_rfp(file_bytes: bytes, filename: str) -> str:
    try:
        endpoint = os.environ.get("Document_Intelligence_Endpoint")
        key = os.environ.get("Document_Intelligence_Key")

        if not endpoint or not key:
            raise ValueError("Azure Document Intelligence endpoint or key not configured.")

        document_intelligence_client = DocumentIntelligenceClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-read", AnalyzeDocumentRequest(bytes_source=file_bytes)
        )
        result = poller.result()

        output = {
            "filename": filename,
            "content": result.content
        }

        return json.dumps(output)

    except Exception as e:
        raise Exception(f"Failed to process PDF with Document Intelligence: {str(e)}")