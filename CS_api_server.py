from flask import Flask, request, jsonify
import paramiko
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import time
from tqdm import tqdm
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=10)



@app.route('/homepage')
def start_homepage():
	return 'hello world'

# C에서 업로드한 파일을 A로 전송, A에서 명령어 실행
@app.route('/run-commands-with-file', methods=['POST'])
def run_commands_with_file():
    print('Transferring File..')
    # 파일 처리
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400
    local_file_path = os.path.join('/home/dke/shlee/upload_files', file.filename)    
    file.save(local_file_path) # B 로컬에 파일 저장
    file_size = os.path.getsize(local_file_path)  # 파일 크기 계산

    print('File is saved in API Server')
    # 명령어 처리
    commands_data = request.form.get('commands')
    if not commands_data:
        return jsonify({"error": "No commands provided"}), 400
    commands = json.loads(commands_data)
    results = []
    for command_info in commands:
        # A 서버의 파일 경로 설정 (예시)
        remote_file_path = os.path.join("/home/dke/shlee/download_files", file.filename)
        # 파일을 A 서버로 전송
        transfer_file_to_a_server(local_file_path, remote_file_path, command_info, file_size)
        print("File transfer completed to port:", command_info.get('port'))


    futures = [executor.submit(execute_ssh_command, cmd['host'], cmd['port'], cmd['username'], cmd['password'], cmd['command']) for cmd in commands]
    for future in as_completed(futures):
        result = future.result()
        results.append(result)
    
    execute_ssh_command("10.0.0.0", 22, "dke", "asdf", "python3 /home/lwjeong/request.py")
    
    # B에서 파일 삭제
    os.remove(local_file_path)
    return jsonify(results)

# A 서버로 파일 전송
def transfer_file_to_a_server(local_path, remote_path, command_info, file_size):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(command_info['host'], port=command_info.get('port', 10100), 
                username=command_info['username'], password=command_info['password'])
    sftp = ssh.open_sftp()

    with tqdm(total=file_size, unit='B', unit_scale=True, desc=f'Uploading {os.path.basename(local_path)}') as progress:
        def progress_bar(transferred, to_be_transferred):
            progress.update(transferred - progress.n)  # 진행 상태 업데이트
        
        sftp.put(local_path, remote_path, callback=progress_bar)

    sftp.close()
    ssh.close()

# A에서 명령어 실행
def execute_ssh_command(host, port, username, password, command):
    print("Executing command on host:", host, "port:", port)
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()
        client.close()
        return {"host": host, "output": output, "error": error, "command": command}
    except Exception as e:
        return {"host": host, "error": str(e), "command": command}


# B 서버에서 C 서버로 파일 전송
def transfer_file_to_c_server(local_path, remote_path, c_server_info):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(c_server_info['host'], port=c_server_info.get('port', 22), 
                username=c_server_info['username'], password=c_server_info['password'])
    sftp = ssh.open_sftp()
    sftp.put(local_path, remote_path)  # 파일을 C 서버의 지정된 경로로 전송
    print("Transfer file to Client")
    sftp.close()
    ssh.close()

# 연산 완료 파일을 A -> B -> C로 전송
@app.route('/download-file', methods=['POST'])
def download_file():

    # 파일이 request에 포함되어 있는지 확인
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    c_server_info = {
    'host': '10.0.0.0',
    'port': 22,  # SSH 기본 포트
    'username': 'dke',
    'password': 'asdf'
    }
    
    # 파일 저장 경로 설정
    file_path = os.path.join('/home/dke/shlee/download_files', file.filename) # B path
    remote_path = os.path.join('/home/dke/shlee/download_file', file.filename) # C path
    # 파일 저장
    file.save(file_path)
    transfer_file_to_c_server(file_path, remote_path, c_server_info)
    return jsonify({"message": "File uploaded successfully", "path": file_path})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

