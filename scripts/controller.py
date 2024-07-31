from knowledgeDB import KnowledgeDataBase
from typing import any
from file_reader import FileLoader
class Controller:
    def __init__(self, user_id: str, vecDB: KnowledgeDataBase, relationDB:any):
        self.user_id = user_id
        self.vec_db = vecDB
        self.relation_db = relationDB
    
    def add_file(self, filename):
        new_file = FileLoader(filename, self.user_id, False)
        new_docs = new_file.split_file_to_docs()
        self.vecDB.update(new_docs)

    def add_content(self, content):
        empty_file = FileLoader("", self.user_id, False)
        new_docs = empty_file.split_content_to_docs(content)
        self.vecDB.update(new_docs)

    ### 临时方案，检查文件是否重复上传
    def is_file_stored(self, filename, file_map):
        ##mysql

        ## trick code
        if filename in file_map:
            return True
        return False

    def search(self, query, args):
        if self.vec_db == None:
            print("vecDB is None!PASS")
            return None
        return self.vec_db.search(query)

