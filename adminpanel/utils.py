import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfMerger
import pandas as pd
from PIL import Image


# Convert image to PDF
def image_to_pdf(image_path, output_path):
    image = Image.open(image_path)
    pdf_bytes = io.BytesIO()
    image.save(pdf_bytes, format='PDF')
    with open(output_path, 'wb') as f:
        f.write(pdf_bytes.getvalue())
    return output_path


# Convert text to PDF
def text_to_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    text_object = c.beginText(40, height - 40)
    for line in text.splitlines():
        text_object.textLine(line)
    c.drawText(text_object)
    c.save()
    return output_path


# Convert Excel to PDF (basic table)
def excel_to_pdf(excel_file_path, output_path):
    df = pd.read_excel(excel_file_path)
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    x, y = 50, height - 50
    row_height = 20

    for index, row in df.iterrows():
        line = ", ".join([str(item) for item in row])
        c.drawString(x, y - index * row_height, line)
        if y - index * row_height < 50:
            c.showPage()
            y = height - 50

    c.save()
    return output_path


# Combine multiple PDFs into one
def combine_pdfs(pdf_paths, output_path):
    merger = PdfMerger()
    for pdf in pdf_paths:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()
    return output_path
