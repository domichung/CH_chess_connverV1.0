import socket
import threading
from queue import Queue
import time

QUEUE_MAX_SIZE = 5
producer_port = 8880
consumer_port = 8881
queue = Queue(maxsize=QUEUE_MAX_SIZE)

def handle_insert(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            number = int(data)
            if queue.full():
                client_socket.send("Error: Queue is full.".encode('utf-8'))
            else:
                print('input',number)
                queue.put(number)
                client_socket.send("Success: Number added to Queue.".encode('utf-8'))
        except Exception as e:
            print(f"Producer error: {e}")
            break
    client_socket.close()

def handle_pop(client_socket):
    while True:
        if not queue.empty():
            number = queue.get()
            client_socket.send(str(number).encode('utf-8'))
            break
        else:
            client_socket.send("Waiting for data...".encode('utf-8'))
            time.sleep(2)
    client_socket.close()

def server(port, handler):
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_socket.bind(('', port))
    srv_socket.listen(5)
    print(f"Server started on port {port}.")
    
    while True:
        client_socket, client_address = srv_socket.accept()
        print(f"Connection from {client_address} on port {port}.")
        threading.Thread(target=handler, args=(client_socket,)).start()

if __name__ == '__main__':
    threading.Thread(target=server, args=(producer_port, handle_insert)).start()
    threading.Thread(target=server, args=(consumer_port, handle_pop)).start()
