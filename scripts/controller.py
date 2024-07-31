from knowledgeDB import KnowledgeDataBase
from typing import Any
from file_reader import FileLoader
class Controller:
    def __init__(self, user_id: str, vecDB: KnowledgeDataBase, relationDB: Any):
        self.user_id = user_id
        self.vec_db = vecDB
        self.relation_db = relationDB
    
    def add_file(self, filename, is_url):
        new_file = FileLoader(filename, self.user_id, is_url)
        new_file.split_file_to_docs()
        self.vec_db.update_index(new_file.docs)

    def add_content(self, content):
        empty_file = FileLoader("", self.user_id, False)
        empty_file.split_content_to_docs(content)
        self.vec_db.update_index(empty_file.docs)

    ### 临时方案，检查文件是否重复上传
    def is_file_stored(self, filename, file_map):
        ##mysql

        ## trick code
        if filename in file_map:
            return True
        return False

    def search(self, query):
        if self.vec_db == None:
            print("vecDB is None!PASS")
            return None
        return self.vec_db.search(query)

