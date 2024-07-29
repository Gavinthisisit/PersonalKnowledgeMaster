from llama_index.core import ServiceContext, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core import Document
from typing import Dict, List, Optional, Sequence

class KnowledgeDataBase:
    def __init__(self, persist_dir, similarity_top_k=5):
        self.persist_dir = persist_dir
        self.similarity_top_k = similarity_top_k
        if not os.path.exists(index_save_dir):
            self.db_index = load_index_from_storge(
                StorageContext.from_defaults(persist_dir=index_save_dir),
                service_context=sentence_context
            )
            self.retriever = self.db_index.as_retriever(self.similarity_top_k)
        self.db_index = None
        self.retriever = None
    
    def update_index(self, docs: Sequence[Document]):
        if self.db_index == None:
            return "db_index not found"
        for doc in docs:
            self.db_index.insert(doc)
        self.retriever = self.db_index.as_retriever(self.similarity_top_k)

    def search(self, query: str):
        if self.retriever == None:
            return None
        nodes = self.retriever.retrieve(query)
        if len(nodes) > 0:
            return nodes[0]
