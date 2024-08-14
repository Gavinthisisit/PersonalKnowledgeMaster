from sanic import Sanic, response
#from sanic.exceptions import abort
from sanic.log import logger
import os
import sys
import pickle
import general_utils

from knowledgeDB import KnowledgeDataBase
from controller import Controller

# 创建Sanic应用
app = Sanic("FileUploadService")

# # 初始化向量数据库与文件去重map
# vecDB = KnowledgeDataBase("./DataBase", similarity_top_k=5)
# dealed_map_file = "./output/dealed_map.pkl"
# if os.path.exists(dealed_map_file):
#     with open(dealed_map_file, 'rb') as file:
#         dealed_map = pickle.load(file)
# dealed_map = {}

# def get_input():
#     try:
#         user_input = input()
#         index = user_input.find(":")
#         if index != -1:
#             return user_input[:index], user_input[index+1:]
#         return user_input, ""
#     except Exception as e:
#         print(e)
#         return "", ""
# user_id = "test_1234"
# contro = Controller(user_id, vecDB, None)
# r_type = ""
# r_content = ""
# while True:
#     print("请输入您的指令(输入exit退出):")
#     r_type, r_content = get_input()
#     print("req_type: ", r_type, "r_content: ", r_content)
#     if r_type == "exit":
#         sys.exit(0)
#     if r_type == "file":
#         file_path = r_content
#         if contro.is_file_stored(file_path, dealed_map):
#             print({'status': 'success', 'message': f'File {file.name} already dealed!'})
#         else:
#             dealed_map[file_path] = 1
#             contro.add_file(file_path, False)
#             print({'status': 'success', 'message': f'File saved at {file_path}'})
#     elif r_type == "content":
#         content = r_content
#         if general_utils.isURL(content):
#             print("this is url")
#             key = user_id + "_" + content
#             if key in dealed_map:
#                     print({'status': 'success', 'message': f'url {content} already dealed!'})
#             dealed_map[key] = 1
#             contro.add_file(content, True)
#             print({'status': 'success', 'message': f'{content} saved!'})
#         else:
#             if len(content) < 100:
#                 resp = contro.search(content)
#                 print(resp.text)
#                 print({'status': 'success', 'message': f'{resp}'})
#             else:
#                 contro.add_content(content)
#                 print({'status': 'success', 'message': f'{content} saved!'})
#     else:
#         pass

@app.post('/test')
async def upload_file(request):
    # 获取用户ID和文件
    user_id = general_utils.safe_get(request, "userid")
    file = request.files.get('file')
    # 确保用户ID和文件都被提供
    if not user_id:
        return response.json({'error': 'No user info'}, status=400)
    
    if file is not None:
        # 确保/tmp目录存在
        os.makedirs('./tmp', exist_ok=True)
        logger.info("file_body: " + str(len(file.body)))

        # 文件路径
        file_path = f'./tmp/{user_id}_{file.name}'

        # 暂存文件
        logger.info("file_path: " + file_path)
        return response.json({'status': 'success', 'message': f'File saved at {file_path}'})
    else:
        return response.json({'status': 'success', 'message': f'File saved at {file_path}'})


# @app.post('/upload')
# async def upload_file(request):
#     # 获取用户ID和文件
#     user_id = general_utils.safe_get(request, "userid")
#     file = request.files.get('file')
#     # 确保用户ID和文件都被提供
#     if not user_id:
#         return response.json({'error': 'No user info'}, status=400)
#     contro = Controller(user_id, vecDB, None)
#     # 确保/tmp目录存在
#     os.makedirs('./tmp', exist_ok=True)
#     logger.info("file_body: " + str(len(file.body)))

#     # 文件路径
#     file_path = f'./tmp/{user_id}_{file.name}'

#     # 暂存文件
#     logger.info("file_path: " + file_path)
#     with open(file_path, 'wb') as f:
#         f.write(file.body)
#     if contro.is_file_stored(file_path, dealed_map):
#         return response.json({'status': 'success', 'message': f'File {file.name} already dealed!'})
#     dealed_map[file_path] = 1
    
#     ## 处理新增文件
#     contro.add_file(file_path)
#     return response.json({'status': 'success', 'message': f'File saved at {file_path}'})

# @app.post('/query')
# async def upload_file(request):
#     # 获取用户ID和文件
#     user_id = request.form.get('userid')
#     content = request.form.get("content")
    
#     contro = Controller(user_id, vecDB, None)
#     # 确保用户ID和文件都被提供
#     if not user_id or not content:
#         return response.json({'error': 'No user info or user query'}, status=400)

#     if general_utils.isURL(content):
#         key = user_id + "_" + content
#         if key in dealed_map:
#              return response.json({'status': 'success', 'message': f'url {content} already dealed!'})
#         dealed_map[key] = 1
#         contro.add_file(content)
#         return response.json({'status': 'success', 'message': f'{content} saved!'})
#     else:
#         if len(content) < 100:
#             resp = contro.search(content)
#             return response.json({'status': 'success', 'message': f'{resp}'})
#         else:
#             contro.add_content(content)
#             return response.json({'status': 'success', 'message': f'{content} saved!'})

@app.listener("before_server_stop")
async def before_server_stop(request, loop):
    logger.info("save dealed_map")
    # with open(dealed_map_file, 'wb') as file:
    #     pickle.dumps(dealed_map, file)
    # vecDB.save()
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6006, debug=True)