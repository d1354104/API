import requests
import os
import time

def transfer_file_to_b_server(file_path, b_server_url):
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        response = requests.post(b_server_url, files=files)
        return response.json()

# B 서버의 파일 업로드 API 엔드포인트
b_server_url = 'http://0.0.0.0:8080/download-file'

# 전송할 파일 경로
file_path = '/home/dke/output.txt' #pagerank 연산 파일

# 파일 전송 실행
response = transfer_file_to_b_server(file_path, b_server_url)

print(response)
