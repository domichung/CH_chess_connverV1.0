import socket
import threading
import logging

server_ip = '127.0.0.1'
server_port = 12345
number_of_max_con = 3

accounts = {
    "user1": "password1",
    "user2": "password2",
    "admin": "admin123"
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(conn, addr):
    logging.info(f"來源: {addr[0]}:{addr[1]} 的登入請求")
    try:
        account = conn.recv(1024).decode('utf-8')
        conn.sendall(b"Password: ")  
        password = conn.recv(1024).decode('utf-8')

        logging.info(f"帳號: {account}, 密碼: {password}")

        if accounts.get(account) == password:
            conn.sendall(b"+success")
            logging.info(f"來源: {addr[0]}:{addr[1]} 登入成功")
        else:
            conn.sendall(b"-failed")
            logging.warning(f"來源: {addr[0]}:{addr[1]} 登入失敗")
    except Exception as e:
        logging.error(f"處理來源: {addr[0]}:{addr[1]} 時發生錯誤: {e}")
    finally:
        conn.close()

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(number_of_max_con)
        logging.info(f"伺服器已啟動，正在 {server_ip}:{server_port} 等待連線...")

        while True:
            try:
                conn, addr = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                client_thread.start()
                logging.info(f"目前活動的連線數: {threading.active_count() - 1}")
            except Exception as e:
                logging.error(f"接受連線時發生錯誤: {e}")

if __name__ == '__main__':
    run_server()
