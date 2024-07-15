# from qanything_kernel.utils.general_utils import *
from typing import List, Union, Callable
from model_config import UPLOAD_ROOT_PATH, SENTENCE_SIZE, ZH_TITLE_ENHANCE
from langchain.docstore.document import Document
# from qanything_kernel.utils.loader.my_recursive_url_loader import MyRecursiveUrlLoader
# from langchain.document_loaders import UnstructuredFileLoader, TextLoader
from langchain_community.document_loaders import UnstructuredFileLoader, TextLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
# from langchain.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import UnstructuredEmailLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from qanything_kernel.utils.custom_log import debug_logger, qa_logger
from chinese_text_splitter import ChineseTextSplitter
from image_loader import UnstructuredPaddleImageLoader
# from pdf_loader import UnstructuredPaddlePDFLoader
from ZhTitleEnhance import zh_title_enhance
from sanic.request import File
import pandas as pd
import os
from general_utils import *

text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n", ".", "。", "!", "！", "?", "？", "；", ";", "……", "…", "、", "，", ",", " "],
    chunk_size=400,
    length_function=num_tokens,
)


class LocalFile:
    # def __init__(self, user_id, kb_id, file: Union[File, str], file_id, file_name, embedding, is_url=False, in_milvus=False):
    def __init__(self, file_name, file_id, is_url=False):
        # self.user_id = user_id
        # self.kb_id = kb_id
        self.file_id = file_id
        self.docs: List[Document] = []
        # self.embs = []
        # self.emb_infer = embedding
        # self.url = None
        # self.in_milvus = in_milvus
        self.file_path = file_name
        self.url = ""
        if is_url:
            self.url = file_name
        # else:
        #     if isinstance(file, str):
        #         self.file_path = file
        #         with open(file, 'rb') as f:
        #             self.file_content = f.read()
        #     else:
        #         upload_path = os.path.join(UPLOAD_ROOT_PATH, user_id)
        #         file_dir = os.path.join(upload_path, self.file_id)
        #         os.makedirs(file_dir, exist_ok=True)
        #         self.file_path = os.path.join(file_dir, self.file_name)
        #         self.file_content = file.body
        #     with open(self.file_path, "wb+") as f:
        #         f.write(self.file_content)
        print(f'success init localfile {self.file_path}')

    def split_file_to_docs(self, sentence_size=SENTENCE_SIZE,
                           using_zh_title_enhance=ZH_TITLE_ENHANCE):
        if self.url != "":
            # print("load url: {}".format(self.url))
            # loader = MyRecursiveUrlLoader(url=self.url)
            # textsplitter = ChineseTextSplitter(pdf=False, sentence_size=sentence_size)
            # docs = loader.load_and_split(text_splitter=textsplitter)
            pass
        elif self.file_path.lower().endswith(".md"):
            loader = UnstructuredFileLoader(self.file_path, mode="elements")
            docs = loader.load()
        elif self.file_path.lower().endswith(".txt"):
            loader = TextLoader(self.file_path, autodetect_encoding=True)
            texts_splitter = ChineseTextSplitter(pdf=False, sentence_size=sentence_size)
            docs = loader.load_and_split(texts_splitter)
        elif self.file_path.lower().endswith(".pdf"):
            # loader = UnstructuredPaddlePDFLoader(self.file_path, ocr_engine)
            # texts_splitter = ChineseTextSplitter(pdf=True, sentence_size=sentence_size)
            # docs = loader.load_and_split(texts_splitter)
            pass
        elif self.file_path.lower().endswith(".jpg") or self.file_path.lower().endswith(
                ".png") or self.file_path.lower().endswith(".jpeg"):
            loader = UnstructuredPaddleImageLoader(self.file_path, mode="elements")
            texts_splitter = ChineseTextSplitter(pdf=False, sentence_size=sentence_size)
            docs = loader.load_and_split(text_splitter=texts_splitter)
        elif self.file_path.lower().endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(self.file_path, mode="elements")
            texts_splitter = ChineseTextSplitter(pdf=False, sentence_size=sentence_size)
            docs = loader.load_and_split(texts_splitter)
        elif self.file_path.lower().endswith(".xlsx"):
            # loader = UnstructuredExcelLoader(self.file_path, mode="elements")
            docs = []
            xlsx = pd.read_excel(self.file_path, engine='openpyxl', sheet_name=None)
            for sheet in xlsx.keys():
                df = xlsx[sheet]
                df.dropna(how='all', inplace=True)
                csv_file_path = self.file_path[:-5] + '_' + sheet + '.csv'
                df.to_csv(csv_file_path, index=False)
                loader = CSVLoader(csv_file_path, csv_args={"delimiter": ",", "quotechar": '"'})
                docs += loader.load()
        elif self.file_path.lower().endswith(".pptx"):
            loader = UnstructuredPowerPointLoader(self.file_path, mode="elements")
            docs = loader.load()
        elif self.file_path.lower().endswith(".eml"):
            loader = UnstructuredEmailLoader(self.file_path, mode="elements")
            docs = loader.load()
        elif self.file_path.lower().endswith(".csv"):
            loader = CSVLoader(self.file_path, csv_args={"delimiter": ",", "quotechar": '"'}, encoding='utf8')
            docs = loader.load()
        else:
            raise TypeError("文件类型不支持，目前仅支持：[md,txt,pdf,jpg,png,jpeg,docx,xlsx,pptx,eml,csv]")
        if using_zh_title_enhance:
            print("using_zh_title_enhance %s", using_zh_title_enhance)
            docs = zh_title_enhance(docs)

        # 重构docs，如果doc的文本长度大于800tokens，则利用text_splitter将其拆分成多个doc
        # text_splitter: RecursiveCharacterTextSplitter
        # print(f"before 2nd split doc lens: {len(docs)}")
        # docs = text_splitter.split_documents(docs)
        # print(f"after 2nd split doc lens: {len(docs)}")

        # 这里给每个docs片段的metadata里注入file_id
        for doc in docs:
            doc.metadata["file_id"] = self.file_id
            doc.metadata["file_name"] = self.url if self.url else os.path.split(self.file_path)[-1]
        write_check_file(self.file_path, docs)
        if docs:
            print('langchain analysis content head: %s', docs[0].page_content[:100])
        else:
            print('langchain analysis docs is empty!')
        self.docs = docs

    def create_embedding(self):
        self.embs = self.emb_infer._get_len_safe_embeddings([doc.page_content for doc in self.docs])

if __name__ == '__main__':
    file = LocalFile('./test.csv', "123", False)
    file.split_file_to_docs()
    print(len(file.docs))
    print(file.docs[1])
