from ebooklib import epub, ITEM_IMAGE

def read_epub(path: str):
    epub_file = epub.read_epub(path)
    title = epub_file.get_metadata('DC','title')[0][0].replace(' ','_')
    lang = epub_file.get_metadata('DC','language')[0][0]
    author = epub_file.get_metadata('DC','creator')[0][0].replace(' ','_')
    # cover_image = epub_file.get_item_with_id('cover-image')
    # try:
    #     cover_image = cover_image.get_content()
    #     with open(output_file_path, 'wb') as handler:
    #         handler.write(cover_image)
    # except:
    #     pass #ничего не делать
    return title, lang, author