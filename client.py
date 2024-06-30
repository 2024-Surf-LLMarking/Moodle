import requests

# 通过POST向大模型服务器请求，获取分数
def get_mark(url, data):
    response_csv = requests.post(url, data=data)  # 发送POST请求
    return response_csv
