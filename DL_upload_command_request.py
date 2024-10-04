import requests
import json
import sys
import os

if len(sys.argv) < 3:
    print("사용법: python DL_upload_command_request.py <파일명> <옵션>")
    print("옵션: ev, pr")
    sys.exit(1)

file_name = sys.argv[1]
command_option = sys.argv[2]
#조건별 커맨드

if command_option == "pr":
    with open(file_name, 'rb') as file:
        files = {'file': file}

        url = "http://0.0.0.0:8080/run-commands-with-file"
        pr_command = "/home/lwjeong/pr.sh " + os.path.basename(file_name)
        
        commands_pr = json.dumps([
            {
                "host": "10.0.0.0",
                "port": 22,
                "username": "dke",
                "password": "asdf",
                "command": pr_command
            },
            {
                "host": "10.0.0.0",
                "port": 22,
                "username": "dke",
                "password": "asdf",
                "command": pr_command
            },
            {
                "host": "10.0.0.0",
                "port": 22,
                "username": "dke",
                "password": "asdf",
                "command": pr_command
            },
            {
                "host": "10.0.0.0",
                "port": 22,
                "username": "dke",
                "password": "asdf",
                "command": pr_command
            },
            {
                "host": "10.0.0.0",
                "port": 22,
                "username": "dke",
                "password": "asdf",
                "command": pr_command
            }
        ])
        
        # 다른 명령 추가 가능
        response_pr = requests.post(url, files=files, data={'commands': commands_pr})
        print(response_pr.json())
    
elif command_option == "ev":
    with open(file_name, 'rb') as file:
        files = {'file': file}

        url = "http://0.0.0.0:8080/run-commands-with-file"
        ev_command = "/home/lwjeong/ev.sh " + os.path.basename(file_name)
        
        commands_ev = json.dumps([
            {
                "host": "10.0.0.0",
                "port": 22,
                "username": "dke",
                "password": "asdf",
                "command": ev_command
            },
            {
                "host": "10.0.0.0",
                "port": 22,
                "username": "dke",
                "password": "asdf",
                "command": ev_command
            },
            {
                "host": "10.0.0.0",
                "port": 22,
                "username": "dke",
                "password": "asdf",
                "command": ev_command
            },
            {
                "host": "10.0.0.0",
                "port": 22,
                "username": "dke",
                "password": "asdf",
                "command": ev_command
            },
            {
                "host": "10.0.0.0",
                "port": 22,
                "username": "dke",
                "password": "asdf",
                "command": ev_command
            }
        ])
        # 다른 명령 추가 가능
    
        response_ev = requests.post(url, files=files, data={'commands': commands_ev})
        print(response_ev.json())
    
    