import os
import tempfile
from PyPDF2 import PdfMerger
from reportlab.pdfgen import canvas
from PIL import Image
from docx2pdf import convert as convert_docx
import pdfkit
import pandas as pd

# Convert text to PDF
def create_text_pdf(text):
    file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    c = canvas.Canvas(file_path)
    y = 800
    for line in text.split('\n'):
        c.drawString(40, y, line.strip())
        y -= 15
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    return file_path

# Convert other file types to PDF
def convert_to_pdf(input_file_path):
    ext = os.path.splitext(input_file_path)[1].lower()
    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name

    if ext in ['.jpg', '.jpeg', '.png']:
        image = Image.open(input_file_path).convert('RGB')
        image.save(output_file)
    elif ext == '.docx':
        convert_docx(input_file_path, output_file)
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(input_file_path)
        html = df.to_html(index=False)
        html_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        with open(html_file.name, 'w') as f:
            f.write(html)
        pdfkit.from_file(html_file.name, output_file)
        os.unlink(html_file.name)
    elif ext == '.pdf':
        return input_file_path
    else:
        return None
    return output_file

# Merge list of PDF files into one
def merge_files_to_pdf(file_list, output_path):
    merger = PdfMerger()
    for file_path in file_list:
        if file_path:
            merger.append(file_path)
    merger.write(output_path)
    merger.close()
