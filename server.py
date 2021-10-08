import socket
import time

import json
import ast

host = '203.246.113.83' # 호스트 ip를 적어주세요
port = 8080            # 포트번호를 임의로 설정해주세요

server_sock = socket.socket(socket.AF_INET)
server_sock.bind((host, port))
server_sock.listen(1)
print("기다리는 중..")
out_data = {"flag" : -1}

while True: #안드로이드에서 연결 버튼 누를 때까지 기다림
    client_sock, addr = server_sock.accept() # 연결 승인

    if client_sock: #client_sock 가 null 값이 아니라면 (연결 승인 되었다면)
        print('Connected by?!', addr) #연결주소 print
        #in_data = client_sock.recv(1024) #안드로이드에서 "refresh" 전송

        # encoding
        in_data = client_sock.recv(4096)
        print(in_data)
        #print(in_data.decode('UTF-8'))

        # print(len(in_data))
        #try:
            #dict_str = json.loads(in_data) #.decode('UTF-8')
            #print(dict_str)
        # my_json = in_data.decode('utf8').replace("'", '"')
        # data = json.loads(my_json)
        # print("Data : ", data)
        # s = json.dumps(data, indent=4)
        # print("S : ", s)
            # my_data = ast.literal_eval(dict_str)
        # print('rcv :', in_data.decode("ISO-8859-1"), len(in_data)) #전송 받은값 디코딩
            # print(repr(mydata))#.decode("ISO-8859-1"))
        # except:
        #     print("exception")
        #     client_sock.close()
        #     server_sock.close()
        # y = {}
        # for key, value in in_data.items():
        #     y[key.decode("utf-8")] = value.decode("utf-8")
            # y = json.load(in_data)

        # print(y)

        # while in_data : #2초마다 안드로이드에 값을 전달함 (추후 , STOP , Connect 옵션 설정 가능)
        json_data=json.dumps(out_data).encode('utf-8')

        client_sock.send(json_data) # int 값을 string 으로 인코딩해서 전송, byte 로 전송하면 복잡함

        print('send :', out_data)
        #out_data = out_data+1 #전송값 +1
        time.sleep(2)

client_sock.close()
server_sock.close()
