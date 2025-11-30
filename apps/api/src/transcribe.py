from PyPDF2 import PdfReader
from PIL import Image
import fitz
from pdf2image import convert_from_bytes
import io
import numpy as np
import easyocr
import cv2
from google.cloud import documentai_v1
from google.api_core.client_options import ClientOptions
from google.oauth2 import service_account
import fitz

from fastapi import UploadFile


def transcribe_pdf(raw_bytes, filename):
    # TODO: Move these all to .env
    project_id = 'document-ai-479801'
    processor_id = 'f70206c200d81703'
    location = 'us'

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    credentials = service_account.Credentials.from_service_account_file(
      "document-ai-479801-eeca2f70d17b.json"
    )

    # Initialize Document AI client.
    client = documentai_v1.DocumentProcessorServiceClient(client_options=opts, credentials=credentials)

    # Get the Fully-qualified Processor path.
    full_processor_name = client.processor_path(project_id, location, processor_id)

    # Get a Processor reference.
    request = documentai_v1.GetProcessorRequest(name=full_processor_name)
    processor = client.get_processor(request=request)

    # `processor.name` is the full resource name of the processor.
    # For example: `projects/{project_id}/locations/{location}/processors/{processor_id}`
    print(f"Processor Name: {processor.name}")

    # Load binary data.
    # For supported MIME types, refer to https://cloud.google.com/document-ai/docs/file-types
    raw_document = documentai_v1.RawDocument(
      content=raw_bytes,
      mime_type="application/pdf",
    )

    # Send a request and get the processed document.
    request = documentai_v1.ProcessRequest(name=processor.name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    # Read the text recognition output from the processor.
    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    print("The document contains the following text:")
    print(document.text)
    # TODO: Save the text and somehow give users access to it.

