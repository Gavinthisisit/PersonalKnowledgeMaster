from llama_index.core.schema import (
    BaseNode
)

import json
from llm import Conversation
from knowledgeDB import KnowledgeDataBase
from sql import SqliteDB
from typing import Any
from file_reader import FileLoader

class Controller:
    def __init__(self, user_id: str, vecDB: KnowledgeDataBase, relationDB: SqliteDB, agent: Conversation):
        self.user_id = user_id
        self.vec_db = vecDB
        self.agent = agent
        self.relation_db = relationDB
    
    def add_file(self, filename, is_url):
        new_file = FileLoader(filename, self.user_id, is_url)
        new_file.split_file_to_docs()
        self.vec_db.update_index(new_file.docs)
        ### 请求大模型
        self.generate_info = self.call_llm(new_file.content)

        ### 写入数据库
        if new_file.title != "":
            self.generate_info["title"] = new_file.title
        else:
            self.generate_info["title"] = new_file.title
        self.generate_info["file_path"] = filename
        self.generate_info["fileid"] = new_file.file_id
        self.generate_info["modality"] = "file" if not is_url else "link"
        self.generate_info["content"] = new_file.content   
        self.writeSqlite(self.generate_info)

    def add_content(self, content):
        empty_file = FileLoader("", self.user_id, False)
        empty_file.split_content_to_docs(content)
        self.vec_db.update_index(empty_file.docs)
        ### 请求大模型
        self.generate_info = self.call_llm(content)

        ### 写入数据库
        self.generate_info["title"] = ""
        self.generate_info["file_path"] = ""
        self.generate_info["modality"] = "text"
        self.generate_info["fileid"] = empty_file.file_id
        self.generate_info["content"] = content
        self.writeSqlite(self.generate_info)

    ### 临时方案，检查文件是否重复上传
    def is_file_stored(self, filename):
        ##mysql
        search_map = {"userid":self.user_id, "file_path":filename}
        records = self.relation_db.read(search_map)
        if len(records) == 0:
            return True
        return False

    def gen_node_info(self, node: BaseNode):
        retval = {}
        metadata = node.metadata
        retval["title"] = metadata["title"]
        retval["file_path"] = metadata["file_path"]
        fileid = metadata["file_id"]
        ### 从关系数据库查询abstract、快速阅读、label、modal
        retval["abstract"] = "这是摘要内容..."
        retval["quick_read"] = "这是快速阅读的内容..."
        retval["label"] = "label1, label2, label3"
        retval["modality"] = "模态"
        return retval

    def readSqlite(self, fileid=None, labels=None, modality=None):
        search_map = {"userid":self.user_id, "fileid":fileid, "label":labels, "modality":modality}
        records = self.relation_db.read(search_map)
        return records
    
    def writeSqlite(self, info_map):
        info_map["userid"] = self.user_id
        self.relation_db.insert(info_map)

    def search(self, query):
        if self.vec_db == None:
            print("vecDB is None!PASS")
            return None
        datas = []
        nodes = self.vec_db.search(query)
        for node in nodes:
            info = self.get_node_info(node)
            datas.append(info)     
        return datas

    def call_llm(self, content):
        retval = {"abstract": "none", "quick_read": "none", "label":"none"}
        try:
            llm_resp = self.agent.generate(content)
            resp_obj = json.loads(llm_resp)
            retval["abstract"] = resp_obj["abstract"]
            retval["label"] = resp_obj["label"]
            retval["quick_read"] = resp_obj["short_version"]
        except Exception as e:
            return retval
        return retval
