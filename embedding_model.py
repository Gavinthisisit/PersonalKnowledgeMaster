from sentence_transformers import SentenceTransformer
import time
sentences_1 = ["样例数据-1", "样例数据-2"]
sentences_2 = ["样例数据-3", "样例数据-4"]
def get_embeddings(querys):
    model = SentenceTransformer(r'C:\Users\zhaofangCN\PycharmProjects\bge-large-zh-v1.5')
    embeddings = model.encode(querys, normalize_embeddings=True)
    # embeddings_2 = model.encode(sentences_2, normalize_embeddings=True)
    # similarity = embeddings_1 @ embeddings_2.T
    # print(similarity)
    # time.sleep(10)
    return embeddings
