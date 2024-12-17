import socket

server_ip = '127.0.0.1'
server_port = 12345

def run_client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))
            print("已連接到伺服器。")

            account = input("輸入帳號: ")
            client_socket.sendall(account.encode('utf-8'))

            prompt = client_socket.recv(1024).decode('utf-8')
            print(prompt, end="")

            password = input()
            client_socket.sendall(password.encode('utf-8'))

            response = client_socket.recv(1024).decode('utf-8')
            if response == "+success":
                print("登入成功！")
            elif response == "-failed":
                print("登入失敗，帳號或密碼錯誤。")
            else:
                print(f"未知的伺服器回應: {response}")
    except ConnectionRefusedError:
        print("無法連線到伺服器，請稍後。")
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == '__main__':
    run_client()
