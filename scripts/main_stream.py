from knowledgeDb import KnowledgeDataBase
from Controller import Controller

vecDB = KnowledgeDataBase("./DataBase/first_try", 5)

## parse from request
user_id = "user_test_1"
## 用户上传的文件
file = "../data/xxx"
## 用户输入文本
text = ""
## 收藏夹名称
collection = ""

controller = Controller(user_id, vecDB, mysql)
###用户上传文件，更新index
if file:
    if controller.is_file_stored(file):
        print("%s 已经在收藏夹中" % (file))
    else:
        controller.add_file(file, collection)
        print("%s 已成功加入收藏夹中" % (file))
    ##return
if text:
    info = controller.search(text)
    ## return info
