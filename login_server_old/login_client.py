#象棋遊戲登入用戶端
import socket
from getpass import getpass

server_ip = '127.0.0.1'
server_port = 55

def run_client():

    send = input("account : ")
    send2 = getpass("password : ")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            
            client_socket.connect((server_ip, server_port))
        
            client_socket.sendall(send.encode('utf-8'))

            data = client_socket.recv(1024)
            recive = data.decode('utf-8')
            
            print(recive)

            #=============================================
            client_socket.sendall(send2.encode('utf-8'))

            data = client_socket.recv(1024)
            recive = data.decode('utf-8')
            
            print(recive)
    except ConnectionRefusedError:
        print("無法連線到伺服器，請稍後。")
    except Exception as e:
        print(f"發生錯誤: {e}\n請聯繫系統管理員")
   

if __name__ == '__main__':
    run_client()
