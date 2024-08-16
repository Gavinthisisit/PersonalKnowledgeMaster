# from qanything_kernel.utils.general_utils import *
from typing import List, Union, Callable
from model_config import UPLOAD_ROOT_PATH, SENTENCE_SIZE, ZH_TITLE_ENHANCE
# from langchain_core.documents import Document
# from qanything_kernel.utils.loader.my_recursive_url_loader import MyRecursiveUrlLoader
# from langchain.document_loaders import UnstructuredFileLoader, TextLoader
# from langchain_community.document_loaders import UnstructuredFileLoader, TextLoader
# from langchain_community.document_loaders import UnstructuredWordDocumentLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# # from langchain.document_loaders import UnstructuredExcelLoader
# from langchain_community.document_loaders import UnstructuredEmailLoader
# from langchain_community.document_loaders import UnstructuredPowerPointLoader
from csv_loader import CSVLoader
from pdf_loader import load_pdf
from xls_loader import load_xls
from pptx_loader import load_pptx
from url_loader import Crawler
# from qanything_kernel.utils.custom_log import debug_logger, qa_logger
from chinese_text_splitter import ChineseTextSplitter,TextSplitter
from image_loader import UnstructuredPaddleImageLoader
# from pdf_loader import UnstructuredPaddlePDFLoader
from ZhTitleEnhance import zh_title_enhance
# from sanic.request import File
from llama_index.core import Document
import pandas as pd
import os
from general_utils import gen_file_id
from file_utils import *

# text_splitter = RecursiveCharacterTextSplitter(
#     separators=["\n", ".", "。", "!", "！", "?", "？", "；", ";", "……", "…", "、", "，", ",", " "],
#     chunk_size=400,
#     length_function=num_tokens,
# )


class FileLoader:
    def __init__(self, file_name, user_id, is_url=False):
        self.user_id = user_id
        # self.kb_id = kb_id
        self.file_id = gen_file_id(user_id, file_name)
        self.docs: List[Document] = []
        self.content = ""
        self.title = ""
        self.file_path = file_name
        self.url = ""
        if is_url:
            self.url = file_name


    def split_file_to_docs(self, sentence_size=SENTENCE_SIZE,
                           using_zh_title_enhance=ZH_TITLE_ENHANCE):
        if self.url != "":
            crawler = Crawler(self.url)
            texts, title = crawler.crawl()
            self.title = title
        elif self.file_path.lower().endswith(".md"):
            pass
        elif self.file_path.lower().endswith(".txt"):
            text_content = load_txt(self.file_path)
            texts_splitter = TextSplitter(pdf=False, sentence_size=sentence_size)
            texts = texts_splitter.split_text(text_content)
        elif self.file_path.lower().endswith(".pdf"):
            text_content = load_pdf(self.file_path)
            texts_splitter = TextSplitter(pdf=False, sentence_size=sentence_size)
            texts = texts_splitter.split_text(text_content)
        elif self.file_path.lower().endswith(".jpg") or self.file_path.lower().endswith(
                ".png") or self.file_path.lower().endswith(".jpeg"):
            pass
        elif self.file_path.lower().endswith(".docx"):
            text_content = load_docx(self.file_path)
            texts_splitter = TextSplitter(pdf=False, sentence_size=sentence_size)
            texts = texts_splitter.split_text(text_content)
        elif self.file_path.lower().endswith(".xlsx"):
            texts = []
            xlsx = pd.read_excel(self.file_path, engine='openpyxl', sheet_name=None)
            for sheet in xlsx.keys():
                df = xlsx[sheet]
                df.dropna(how='all', inplace=True)
                csv_file_path = self.file_path[:-5] + '_' + sheet + '.csv'
                df.to_csv(csv_file_path, index=False)
                loader = CSVLoader(csv_file_path, csv_args={"delimiter": ",", "quotechar": '"'}, autodetect_encoding=True)
                text_content = loader.load()
                texts_splitter = TextSplitter(pdf=False, sentence_size=sentence_size)
                texts += texts_splitter.split_text(text_content)
        elif self.file_path.lower().endswith(".pptx"):
            text_content = load_pptx(self.file_path)
            texts_splitter = TextSplitter(pdf=False, sentence_size=sentence_size)
            texts = texts_splitter.split_text(text_content)
        elif self.file_path.lower().endswith(".eml"):
            pass
        elif self.file_path.lower().endswith(".csv"):
            loader = CSVLoader(self.file_path, csv_args={"delimiter": ",", "quotechar": '"'}, encoding='utf8')
            text_content = loader.load()
            texts_splitter = TextSplitter(pdf=False, sentence_size=sentence_size)
            texts = texts_splitter.split_text(text_content)
        elif self.file_path.lower().endswith(".xls"):
            text_content = load_xls(self.file_path)
            texts_splitter = TextSplitter(pdf=False, sentence_size=sentence_size)
            texts = texts_splitter.split_text(text_content)
        else:
            raise TypeError("文件类型不支持，目前仅支持：[md,txt,pdf,jpg,png,jpeg,docx,xls,xlsx,pptx,eml,csv]")
        if using_zh_title_enhance:
            print("using_zh_title_enhance %s", using_zh_title_enhance)
            docs = zh_title_enhance(docs)
        print(f'success init localfile {self.file_path}')
        # print(texts)
        self.content = "\n".join(texts)
        if self.title == "" and self.url == "":
            self.title = self.get_file_name(self.file_path)
        # 这里开始构造chunk对象
        metadata={'source': self.file_path, 'file_id': self.file_id, 'user_id': self.user_id, 'file_name': self.url if self.url else os.path.split(self.file_path)[-1]}
        for t in texts:
            doc = Document(
                text = t, 
                metadata = metadata
            )
            self.docs.append(doc)

        if self.docs:
            print('langchain analysis content head: %s', self.docs[0])
        else:
            print('langchain analysis docs is empty!')

    def split_content_to_docs(self, content, sentence_size=SENTENCE_SIZE):
        texts_splitter = TextSplitter(pdf=False, sentence_size=sentence_size)
        texts = texts_splitter.split_text(content)
        # 这里开始构造chunk对象
        metadata={'source': "raw_content", 'user_id': self.user_id}
        for t in texts:
            doc = Document(
                text = t, 
                metadata = metadata
            )
            self.docs.append(doc)
        return

    def get_file_name(self, filename):
        index = filename.rfind("/")
        clean_filename = filename[index + 1:]
        return clean_filename

if __name__ == '__main__':
    user_id = "test_userid"
    filename = "../data/清算部资金清算处2023年度工作总结 - 汇报版（更新数据）.docx"
    file_id = gen_file_id(filename, user_id)
    file_loader = FileLoader("../data/清算部资金清算处2023年度工作总结 - 汇报版（更新数据）.docx", file_id, user_id, False)
    file_loader.split_file_to_docs()
    print(len(file_loader.docs))