import os
import fitz
    
def get_page_text(path):
    with fitz.open(path) as doc:
        page_relation = {}
        page_num = 1
        text = ''
        for page in doc:
            lines = page.getText().replace('\n', '')
            page_relation[page_num] = lines
            text += lines + '\n\n'
            page_num += 1
    return text, page_relation