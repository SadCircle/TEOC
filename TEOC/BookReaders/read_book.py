from base64 import decode, encode
from BookReaders.PdfReader.pdfreader import *
from BookReaders.EpubReader.epubreader import *
import os

# def take_name_file_and_extension(path: str):
#     try:
#         name_file = path[path.rindex('\\') + 1:path.rindex('.')]
#     except ValueError:
#         name_file = path[:path.index('.')]
#     extension_ = path[path.rindex('.') + 1:]
#     return name_file, extension_ 

#УБРАТЬ  SAVE_IMAGE и СДЕЛАТЬ ОТДЕЛЬНО!!!

def take_additional_features(path: str, extension_: str):
    if extension_ == '.pdf':
        pdf_file =  read_pdf(path)
        book_text = pdf_text(path)
        hash_key = str(abs(hash(book_text[:int(len(book_text)*0.1)])))
        save_image(pdf_file, os.path.join('media','images', hash_key + '.png'))
        # lang, _ = language_definition(pdf_file)
        lang = 'unk'
        author, title = pdf_parse(path)
    elif extension_ == '.epub':
        book_text = ''
        hash_key = str(abs(hash(book_text[:int(len(book_text)*0.1)])))
        title, lang, author = read_epub(path)
    output_file_path = os.path.join('images',hash_key + '.png')
    return hash_key, book_text, output_file_path, title, lang, author

# if __name__ == '__main__':
#     path = "Bruce_Johnson_Visual_Studio_Code_End_To_End_Editing_and_Debugging.pdf"
#     name_file, extension_ = take_name_file_and_extension(path)
#     if extension_ == 'pdf':
#         pdf_file =  read_pdf(path)
#         save_image(pdf_file,name_file)
#         lang, prob = language_definition(pdf_file)
#         print(f'lang: {lang},probability: {prob}')
#         author, title = pdf_parse(path)
#         print(f'author: {author}\ntitle: {title}')
#     elif extension_ == 'epub':
#         title,lang,author = read_epub(path)
#         print(f'title: {title}, lang: {lang}, author: {author}')