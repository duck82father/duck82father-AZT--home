import socket
import json

# 챗봇 엔진 서버 접속 정보
host = "127.0.0.1"
port = 5050

# 클라이언트 프로그램 시작
def chatbot_client(query):
    if (quit == "exit"):
        exit(0)
    print("-"*40)

    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 챗봇 엔진 질의 요청
    json_data = {
        'Query' : query,
        'BotType' : 'MyService'
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data) # json 형태 문자열을 json 객체로 변환
    
    mySocket.close()

    return ret_data['Answer']


# def request_check(data):
#     answer = data['key']
#     if answer ==