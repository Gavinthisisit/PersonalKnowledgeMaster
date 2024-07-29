from knowledgeDb import KnowledgeDataBase
from typing import any
from file_loader import FileLoader
class Controller:
    def __init__(self, user_id: str, vecDB: KnowledgeDataBase, relationDB:any):
        self.user_id = user_id
        self.vec_db = vecDB
        self.relation_db = relationDB
    
    def add_file(self, filename):
        ##check mysql
        if self.is_file_stored(filename):
            print("file has been stored!PASS")
            return 
        new_file = FileLoader(filename, self.user_id, False)
        new_docs = new_file.split_file_to_docs()
        self.vecDB.update(new_docs)

    def is_file_stored(self, filename):
        ##mysql
        return False

    def search(self, query, args):
        if self.vec_db == None:
            print("vecDB is None!PASS")
            return None
        return self.vec_db.search(query)

