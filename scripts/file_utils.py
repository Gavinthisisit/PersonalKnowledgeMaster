from docx import Document as Doc
import chardet

 
def load_docx(filename):
    # 加载一个已经存在的文档
    doc = Doc(filename)
     
    # 遍历文档中的所有段落并打印它们的内容
    content = ""
    for para in doc.paragraphs:
        print(para.text)
        content += para.text
        print("-----------")
    return content

def load_txt(filename):
    content = ""
    encoding = detect_file_encoding(filename)
    print(encoding)
    for line in open(filename, encoding=encoding).readlines():
        content += line
    return content

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    return chardet.detect(raw_data)['encoding']