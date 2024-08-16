import sqlite3


# 创建或连接到数据库
class SqliteDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # 创建用户表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS collect_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT NOT NULL,
            fileid TEXT NOT NULL,
            title TEXT NOT NULL,
            abstract TEXT NOT NULL,
            quick_read TEXT,
            label TEXT NOT NULL,
            modality TEXT NOT NULL,
            file_path TEXT,
            content TEXT NOT NULL
        )
        ''')
        self.conn.commit()
        # return cursor, conn
        
    def close_connection(self):
        self.cursor.close()
        self.conn.close()


    # 增加数据
    def insert(self, meta_info):
        userid = meta_info["userid"]
        fileid = meta_info["fileid"]
        title = meta_info["title"]
        abstract = meta_info["abstract"]
        quick_read = meta_info["quick_read"]
        label = meta_info["label"]
        modality = meta_info["modality"]
        content = meta_info["content"]
        file_path = meta_info["file_path"]
        self.cursor.execute('INSERT INTO collect_table (userid, fileid, title, abstract, quick_read, label, modality, content, file_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (userid, fileid, title, abstract, quick_read, label, modality, content, file_path))
        self.conn.commit()


    # 查询数据
    def read(self, search_info_map):
        condition = ""
        for key in search_info_map:
            if search_info_map[key] != "":
                if condition != "":
                    if key == "label":
                        condition = condition + " and " + key  + " like '%" + search_info_map[key] + "%'"
                    else:
                        condition = condition + " and " + key + "='" + search_info_map[key] + "'"
                else:
                    if key == "label":
                        condition = key  + " like '%" + search_info_map[key] + "%'"
                    else:
                        condition = key + "='" + search_info_map[key] + "'"
        self.cursor.execute('SELECT * FROM collect_table where ' + condition)
        retval = []
        for row in self.cursor.fetchall():
            print(row)
            tmp_map = {}
            tmp_map["userid"] = row[1]
            tmp_map["fileid"] = row[2]
            tmp_map["title"] = row[3]
            tmp_map["abstract"] = row[4]
            tmp_map["quick_read"] = row[5]
            tmp_map["label"] = row[6]
            tmp_map["modality"] = row[7]
            tmp_map["file_path"] = row[8]
            tmp_map["content"] = row[9]
            retval.append(tmp_map)
        return retval

    # 更新数据
    def update_user(self):
        # cursor.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', (name, age, user_id))
        # conn.commit()
        pass


    # 删除数据
    def delete_user(self):
        # cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        # conn.commit()
        pass


if __name__ == '__main__':
    db_name = 'new.db'
    db_con = SqliteDB(db_name)

    retval = {}
    retval["userid"] = "userid123"
    retval["title"] = "title_test"
    retval["file_path"] = "这是文件路径"
    retval["content"] = "这是文本content..."
    retval["fileid"] = "file_id12346"
    retval["abstract"] = "这是摘要内容..."
    retval["quick_read"] = ""
    retval["label"] = "label1, label2, label3"
    retval["modality"] = "file"
    db_con.insert(retval)
    retval["userid"] = "userid456"
    retval["title"] = "title_test2"
    retval["file_path"] = "file_path2"
    retval["content"] = "这是文本content..."
    retval["fileid"] = "file_id456"
    retval["abstract"] = "这是摘要内容..."
    retval["quick_read"] = "这是快速阅读的内容..."
    retval["label"] = "label4, label5, label6"
    retval["modality"] = "url"
    # db_con.insert(retval)
    retval["label"] = "label5, label6"
    retval["modality"] = "file"
    # db_con.insert(retval)
    print('Before update and delete:')
    search_map = {"userid": "userid123", "label":""}
    for user in db_con.read(search_map):
        print(user)

    db_con.close_connection()

