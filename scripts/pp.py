from llama_index.core import Document
import pandas as pd
import os
#from general_utils import gen_file_id
#from file_utils import *
#from embedding_model import get_embeddings

tmp_map = {}
doc = Document(
    text = "123"
)
print(doc)

# if __name__ == '__main__':
#     user_id = "test_userid"
#     filename = "../data/清算部资金清算处2023年度工作总结 - 汇报版（更新数据）.docx"
#     file_id = gen_file_id(filename, user_id)
#     file_loader = FileLoader("../data/清算部资金清算处2023年度工作总结 - 汇报版（更新数据）.docx", file_id, user_id, False)
#     file_loader.split_file_to_docs()
#     print(len(file_loader.docs))
