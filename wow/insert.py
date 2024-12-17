import socket

server_ip = "127.0.0.1"  
producer_port = 8880

def main():
    while True:
        try:
            number = input("Enter a number to send (or 'exit' to quit): ")
            if number.lower() == 'exit':
                break

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, producer_port))
            client_socket.send(number.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")
            client_socket.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
