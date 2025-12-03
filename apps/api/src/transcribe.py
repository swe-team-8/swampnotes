"""
unused imports
from PyPDF2 import PdfReader
from PIL import Image
# import fitz
# the above import breaks the backennd build for some reason
from pdf2image import convert_from_bytes
import io
import numpy as np
import easyocr
import cv2
from fastapi import UploadFile
"""

from google.cloud import documentai_v1
from google.api_core.client_options import ClientOptions
from google.oauth2 import service_account
from pdf_annotate import PdfAnnotator, Location, Appearance
import fitz


def transcribe_pdf(raw_bytes, autocorrect):
    # Source for accessing the API: https://docs.cloud.google.com/document-ai/docs/send-request#documentai_process_document-python
    # TODO: Move these all to .env
    project_id = "document-ai-479801"
    processor_id = "f70206c200d81703"
    location = "us"

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    credentials = service_account.Credentials.from_service_account_file(
        "document-ai-479801-eeca2f70d17b.json"
    )

    client = documentai_v1.DocumentProcessorServiceClient(
        client_options=opts, credentials=credentials
    )

    full_processor_name = client.processor_path(project_id, location, processor_id)

    request = documentai_v1.GetProcessorRequest(name=full_processor_name)
    processor = client.get_processor(request=request)

    raw_document = documentai_v1.RawDocument(
        content=raw_bytes,
        mime_type="application/pdf",
    )

    request = documentai_v1.ProcessRequest(
        name=processor.name, raw_document=raw_document
    )
    result = client.process_document(request=request)
    document = result.document

    for c in range(len(document.text)):
        if ord(document.text[c]) > 256:
            document.text = document.text[:c] + " " + document.text[c+1:]


    with open("BUFFER.pdf", "wb") as pdf_file:
        pdf_file.write(raw_bytes)

    new_doc = PdfAnnotator("BUFFER.pdf")
    for i, page in enumerate(document.pages):
        pc1 = page.layout.bounding_poly.vertices[0]
        pc2 = page.layout.bounding_poly.vertices[2]
        height = abs(pc1.y-pc2.y)
        new_doc.set_page_dimensions((abs(pc1.x-pc2.x), abs(pc1.y-pc2.y)), i)
        for paragraph in page.paragraphs:
            c1 = paragraph.layout.bounding_poly.vertices[0]
            c2 = paragraph.layout.bounding_poly.vertices[2]
            new_doc.add_annotation(
                'square',
                Location(x1=c1.x, y1=height-c1.y, x2=c2.x, y2=height-c2.y, page=i),
                Appearance(fill=(1, 1, 1), stroke_width=0),
            )
            text_anchor = paragraph.layout.text_anchor
            start_index = int(text_anchor.text_segments[0].start_index)
            end_index = int(text_anchor.text_segments[0].end_index)
            text = document.text[start_index:end_index].strip()
            new_doc.add_annotation(
                'text',
                Location(x1=c1.x, y1=height-c1.y, x2=c2.x, y2=height-c2.y, page=i),
                Appearance(content=text, fill=(0, 0, 0), font_size=abs(c1.y-c2.y)/2),
            )
    new_doc.write("BUFFER.pdf")
    with open("BUFFER.pdf", "rb") as f:
        return f.read()
    # TODO: Save the text and somehow give users access to it.

