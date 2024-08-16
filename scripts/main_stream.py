from sanic import Sanic, response
#from sanic.exceptions import abort
from sanic.log import logger
import os
import sys
import json
import pickle
import general_utils

from knowledgeDB import KnowledgeDataBase
from llm import Conversation
from sql import SqliteDB
from controller import Controller

# 创建Sanic应用
app = Sanic("FileUploadService")
####配置密钥
os.environ["APPBUILDER_TOKEN"] = 'bce-v3/ALTAK-z7WdbEWUR242VCYC1o1IP/8b5619d99e8a458f0da94c3c75895efdbbaa4bf6'
# 配置密钥与应用ID
intent_app_id = "6aee035e-2689-4040-a02b-8785a392b292"
# 初始化向量数据库与文件去重map

vecDB = KnowledgeDataBase("./DataBase", similarity_top_k=5)
sqlDB = SqliteDB("new.db")
conversation = Conversation(intent_app_id)


@app.post('/search')
async def search(request):
    # 获取用户ID和文件
    user_id = general_utils.safe_get(request, "userid")
    content = general_utils.safe_get(request, "content")
    file = request.files.get('file')
    # 确保用户ID和文件都被提供
    if not user_id:
        return response.json({'error': 'No user info'}, status=400)
    contro = Controller(user_id, vecDB, sqlDB, conversation)
    if file:
        # 确保/tmp目录存在
        os.makedirs('./tmp', exist_ok=True)
        logger.info("file_body: " + str(len(file.body)))

        # 文件路径
        file_path = f'./tmp/{user_id}_{file.name}'

        # 暂存文件
        logger.info("file_path: " + file_path)
        with open(file_path, 'wb') as f:
            f.write(file.body)
        if contro.is_file_stored(file_path):
            return response.json({'status': 'success', 'message': f'File {file.name} already dealed!'})
               
        ## 处理新增文件
        contro.add_file(file_path)
        return response.json({'status': 'success', 'message': f'File saved at {file_path}'})
    else:
        if len(content) > 15:               ####存储文本内容
            contro.add_content(content)
            return response.json({'status': 'success', 'message': f'File {content} saved!'})
        elif general_utils.isURL(content):  ####存储链接内容
            if contro.is_file_stored(content):
                return response.json({'status': 'success', 'message': f'url {content} already dealed!'})
            
            contro.add_file(content, is_url=True)
            return response.json({'status': 'success', 'message': f'{content} saved!'})
        else:                               ####搜索收藏内容
            datas = contro.search(content)
            if datas == None:
                return response.json({'status': 'success', 'message': f'Sorry, 没找到{content}相关的内容'})
            else:
                resp = json.dumps(datas, ensure_ascii=False)
                return response.json({'status': 'success', 'message': '为您找到以下相关的内容...', 'data':f'{resp}'})

@app.post('/collected')
async def user_collected(request):
    # 收藏广场，收藏内容展示
    user_id = request.form.get('userid')
    label = request.form.get("label")
    modal = request.form.get("modality")
    
    contro = Controller(user_id, vecDB, sqlDB, conversation)
    # 确保用户ID和文件都被提供
    datas = contro.readSqlite(labels=label, modality=modal)
    resp = json.dumps(datas, ensure_ascii=False)
    return response.json({'status': 'success', 'message': '为您找到以下相关的内容...', 'data':f'{resp}'})

@app.listener("before_server_stop")
async def before_server_stop(request, loop):
    vecDB.save()
    sqlDB.close_connection()
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6006, debug=True)