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
from embedding_model import get_embeddings

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
            # loader = UnstructuredFileLoader(self.file_path, mode="elements")
            # docs = loader.load()
            pass
        elif self.file_path.lower().endswith(".txt"):
            text_content = load_txt(self.file_path)
            texts_splitter = TextSplitter(pdf=False, sentence_size=sentence_size)
            texts = texts_splitter.split_text(text_content)
        elif self.file_path.lower().endswith(".pdf"):
            # loader = UnstructuredPaddlePDFLoader(self.file_path, ocr_engine)
            # texts_splitter = ChineseTextSplitter(pdf=True, sentence_size=sentence_size)
            # docs = loader.load_and_split(texts_splitter)
            text_content = load_pdf(self.file_path)
            texts_splitter = TextSplitter(pdf=False, sentence_size=sentence_size)
            texts = texts_splitter.split_text(text_content)
        elif self.file_path.lower().endswith(".jpg") or self.file_path.lower().endswith(
                ".png") or self.file_path.lower().endswith(".jpeg"):
            # loader = UnstructuredPaddleImageLoader(self.file_path, mode="elements")
            # texts_splitter = ChineseTextSplitter(pdf=False, sentence_size=sentence_size)
            # docs = loader.load_and_split(text_splitter=texts_splitter)
            pass
        elif self.file_path.lower().endswith(".docx"):
            # loader = UnstructuredWordDocumentLoader(self.file_path, mode="elements")
            # print(loader)
            # docs = loader.load_and_split(texts_splitter)
            text_content = load_docx(self.file_path)
            texts_splitter = TextSplitter(pdf=False, sentence_size=sentence_size)
            texts = texts_splitter.split_text(text_content)
        elif self.file_path.lower().endswith(".xlsx"):
            # loader = UnstructuredExcelLoader(self.file_path, mode="elements")
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
            # loader = UnstructuredPowerPointLoader(self.file_path, mode="elements")
            # docs = loader.load()
            text_content = load_pptx(self.file_path)
            texts_splitter = TextSplitter(pdf=False, sentence_size=sentence_size)
            texts = texts_splitter.split_text(text_content)
        elif self.file_path.lower().endswith(".eml"):
            # loader = UnstructuredEmailLoader(self.file_path, mode="elements")
            # docs = loader.load()
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

        # 重构docs，如果doc的文本长度大于800tokens，则利用text_splitter将其拆分成多个doc
        # text_splitter: RecursiveCharacterTextSplitter
        # print(f"before 2nd split doc lens: {len(docs)}")
        # docs = text_splitter.split_documents(docs)
        # print(f"after 2nd split doc lens: {len(docs)}")

        # 这里开始构造chunk对象
        metadata={'source': self.file_path, 'file_id': self.file_id, 'user_id': self.user_id, 'file_name': self.url if self.url else os.path.split(self.file_path)[-1]}
        for t in texts:
            # tmp_obj = {"content": t, "metadata": metadata}
            # docs.append(tmp_obj)
            doc = Document(
                text = t, 
                metadata = metadata
            )
            self.docs.append(doc)
            
        # 这里给每个docs片段的metadata里注入file_id
        # for doc in docs:
        #     doc.metadata["file_id"] = self.file_id
        #     doc.metadata["file_name"] = self.url if self.url else os.path.split(self.file_path)[-1]
        
        # write_check_file(self.file_path, docs)
        if self.docs:
            print('langchain analysis content head: %s', self.docs[0])
        else:
            print('langchain analysis docs is empty!')
        # self.docs = docs

    # def create_embedding(self):
    #     self.embs = self.emb_infer._get_len_safe_embeddings([doc.page_content for doc in self.docs])

if __name__ == '__main__':
    user_id = "test_userid"
    filename = "../data/清算部资金清算处2023年度工作总结 - 汇报版（更新数据）.docx"
    file_id = gen_file_id(filename, user_id)
    file_loader = FileLoader("../data/清算部资金清算处2023年度工作总结 - 汇报版（更新数据）.docx", file_id, user_id, False)
    file_loader.split_file_to_docs()
    print(len(file_loader.docs))