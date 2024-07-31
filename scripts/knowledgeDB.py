from llama_index.core import ServiceContext, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser
from typing import Dict, List, Optional, Sequence
import os

class KnowledgeDataBase:
    def __init__(self, index_save_dir, chunk_size=1024, similarity_top_k=5):
        self.persist_dir = index_save_dir
        self.similarity_top_k = similarity_top_k
        self.chunk_size = chunk_size
        if os.path.exists(self.persist_dir):
            self.db_index = load_index_from_storage(
                StorageContext.from_defaults(persist_dir=self.persist_dir)
            )
            self.retriever = self.db_index.as_retriever(similarity_top_k=self.similarity_top_k)
        else:
            self.db_index = None
            self.retriever = None
    
    def update_index(self, docs: Sequence[Document]):
        print(len(docs))
        if self.db_index == None:
           # 初始化db_index
           # 定义你的服务上下文
            service_context = ServiceContext.from_defaults(
                llm=None, embed_model= "local://root/autodl-tmp/models/bge-large-zh-v1.5"
            )
            node_parser = SimpleNodeParser.from_defaults(self.chunk_size)
            base_nodes = node_parser.get_nodes_from_documents(docs)
            # 创建index
            self.db_index = VectorStoreIndex(base_nodes, service_context=service_context)
        else:
            for doc in docs:
                self.db_index.insert(doc)
        ##更新retriever
        self.retriever = self.db_index.as_retriever(similarity_top_k=self.similarity_top_k)

    def search(self, query: str):
        if self.retriever == None:
            return None
        nodes = self.retriever.retrieve(query)
        if len(nodes) > 0:
            return nodes[0]
        else:
            return None
    
    def save(self):
        self.db_index.storage_context.persist(persist_dir=self.persist_dir)
