import socket
import time

server_ip = "127.0.0.1"  # 修改為伺服器的 IP
consumer_port = 8881

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, consumer_port))
    print("Connected to server. Waiting for data...")

    while True:
        try:
            response = client_socket.recv(1024).decode('utf-8')
            if response.isdigit():
                print(f"Received number: {response}")
                break
            else:
                print(response)
            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

if __name__ == '__main__':
    main()
