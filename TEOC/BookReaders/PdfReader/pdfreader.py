import fitz
from langdetect import detect_langs
from langdetect import detector_factory
from PyPDF2 import PdfFileReader
import re

def pdf_text(path: str) -> str:
    pdf = fitz.open(path)
    text=''
    for page in range(pdf.pageCount):
        pageObj = pdf.load_page(page)
        text += re.sub(r'\n{1,}', '\n',re.sub('\d', '',pageObj.get_text("text"))).lower()
    return text

def read_pdf(path: str) -> tuple: 
    pdf_file = fitz.open(path)
    return pdf_file

def pdf_parse(path: str) -> list:
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
    author = ''
    if info.author is not None:
        author = info.author
    if info.creator is not None and not author:
        author = info.creator
    title = ''
    if info.title is not None:
        title = info.title
    return author, title
    

def language_definition(pdf_file: tuple) -> list:
    detector_factory.seed = 0
    for page_no in range(len(pdf_file)//2,len(pdf_file)):
        curr_page = pdf_file[page_no]
        text = curr_page.get_text()
        if not text:
            continue
        list_of_languages = detect_langs(text)
        language = sorted(list_of_languages,key = lambda x: x.prob)[0]
        return language.lang, language.prob

def save_image(pdf_file: tuple, output_file_path: str, zoom_x: int = 2, zoom_y: int = 2):
    curr_page = pdf_file[0]
    mat = fitz.Matrix(zoom_x, zoom_y)
    pix = curr_page.get_pixmap(matrix=mat, alpha=False)
    pix.save(output_file_path)