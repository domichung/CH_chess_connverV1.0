#象棋遊戲登入/註冊伺服器
import socket
import threading
import Sys_login
import logging
import Sys_add_account as Saa
import time
import Sys_getuser_info as Sgi
import Sys_reedom as Sr
import Sys_shop as Ss
import json
import Sys_game_spector as GS
import Sys_game_room as Sgr
import move_serch_r
import move_serch_b

server_ip = '127.0.0.1'
login_server_port = 55
register_server_port = 65
lobby_server_port = 75
game_server_port = 85
number_of_max_con = 20
msg_moneynot_enought = '-notenought'
msg_success = '+success'
msg_faild_online = '-alreadyonline'
msg_faild = '-faild'
msg_exsist = '-exsist'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def lobby_server(conn, addr):
    logging.info(f"\033[33m來源: {addr[0]}:{addr[1]} 的大廳請求\033[0m")
    account = None  # 初始化 account 變數
    is_game_started = False  # Track if the game has started
    try:
        while True:
            message = conn.recv(1024).decode('utf-8')
            
            if message.startswith("LOGIN:"):
                account = message.split(":")[1]  # 儲存 account
                logging.info(f"玩家 {account} 已進入大廳")
                conn.sendall("WELCOME_TO_LOBBY".encode('utf-8'))
                
            elif message == "HEARTBEAT":
                conn.sendall("HEARTBEAT_OK".encode('utf-8'))
                
            elif message == "LOGOUT":
                logging.info(f"玩家 {addr[0]}:{addr[1]} 已登出")
                break
                          
            elif message.startswith("CAN_I_CHANGE_MUSIC:"):
                # 處理音量更改請求
                user_id = message.split(":")[1]
                can_change = Sgi.can_i_change_music(user_id)
                if can_change:
                    conn.sendall("MUSIC_CHANGE_OK".encode('utf-8'))
                else:
                    conn.sendall("MUSIC_CHANGE_DENIED".encode('utf-8'))
                    
            elif message.startswith("am_i_vip:"):
                user_id = message.split(":")[1]
                is_vip = Sgi.am_i_vip(user_id)
                if is_vip:
                    conn.sendall("UR_VIP".encode('utf-8'))
                else:
                    conn.sendall("UN_VIP".encode('utf-8'))
                    
            elif message.startswith("my_rank_point:"):
                user_id = message.split(":")[1]
                rkpoint = Sgi.my_rank_point(user_id)
                conn.sendall(str(rkpoint).encode('utf-8'))
                
            elif message.startswith("coupons_i_have:"):
                user_id = message.split(":")[1]
                coupons = Sgi.coupons_i_have(user_id)
                conn.sendall(str(coupons).encode('utf-8'))
                
            elif message.startswith("redeem_code_trade:"):
                try:
                    _, user_id, code = message.split(":")
                    amount = Sr.redeem_code_input(code)
                    if amount is None:
                        response = "此序號已被使用/不存在"
                    else:
                        response = f"儲值成功 ({amount}) 元"
                        print(user_id, int(amount))
                        Ss.addmoney(user_id, int(amount))
                    conn.sendall(response.encode('utf-8'))
                except ValueError:
                    conn.sendall("無效的消息格式".encode('utf-8'))
                
            elif message.startswith("buy_rank:"):
                user_id = message.split(":")[1]
                info = Ss.Buy_RANK(user_id)
                conn.sendall(str(info).encode('utf-8'))
                
            elif message.startswith("buy_vip:"):
                user_id = message.split(":")[1]
                info = Ss.Buy_VIP(user_id)
                conn.sendall(str(info).encode('utf-8'))
                
            elif message.startswith("buy_music_channel:"):
                user_id = message.split(":")[1]
                info = Ss.Buy_music_channel(user_id)
                conn.sendall(str(info).encode('utf-8'))
                
            elif message.startswith("get_rank_now"):
                info = Sgi.get_top_10_ranked_players()
                conn.sendall(str(info).encode('utf-8'))
                
            else:
                logging.warning(f"未知訊息: {message}")
                
    except Exception as e:
        logging.error(f"處理大廳請求時發生錯誤: {e}")
        
    finally:
        #if account and not is_game_started:  # Ensure changeonline is not called when the game has started
        Sys_login.changeonline(account)
        conn.close()
    
def register_server(conn ,addr):
    
    logging.info(f"\033[33m來源: {addr[0]}:{addr[1]} 的註冊請求\033[0m")
    
    try:
        account = conn.recv(1024)
        account_from_client = account.decode('utf-8')
       
        print(f"註冊帳號為 : {account_from_client} \n")

        conn.sendall(msg_success.encode('utf-8'))

        #==============

        passwd = conn.recv(1024)
        passwd_from_client = passwd.decode('utf-8')
        
        conn.sendall(msg_success.encode('utf-8'))
        
        email = conn.recv(1024)
        email_from_client = email.decode('utf-8')
        
        re = Saa.addaccount(account_from_client,passwd_from_client,email_from_client)
       
        if (re == 'success'):
            logging.info(f"\033[32m來源: {addr[0]}:{addr[1]} 註冊成功\033[0m")
            conn.sendall(msg_success.encode('utf-8'))
        else:
            logging.warning(f"\033[31m來源: {addr[0]}:{addr[1]} 註冊失敗\033[0m")
            conn.sendall(msg_exsist.encode('utf-8'))
    except Exception as e:
        logging.error(f"\033[31m來源: {addr[0]}:{addr[1]} 註冊時發生錯誤: {e}\033[0m")
    finally:
        conn.close()
    
    print("###=========================###")
    print(f"\033[46m以結束與 {addr[0]}:{addr[1]} 的登入連線\033[0m" )
    print("###=========================###")

def login_server(conn ,addr):
    
    logging.info(f"\033[33m來源: {addr[0]}:{addr[1]} 的登入請求\033[0m")
    
    try:
        account = conn.recv(1024)
        account_from_client = account.decode('utf-8')
       
        print(f"登入帳號為 : {account_from_client} \n")

        conn.sendall(msg_success.encode('utf-8'))

        #==============

        passwd = conn.recv(1024)
        passwd_from_client = passwd.decode('utf-8')
       
        if(Sys_login.onlinecheck(account_from_client)):
            conn.sendall(msg_faild_online.encode('utf-8'))
            logging.warning(f"\033[31m來源: {addr[0]}:{addr[1]} 登入失敗\033[0m")
        elif (Sys_login.login(account_from_client,passwd_from_client)):
            logging.info(f"\033[32m來源: {addr[0]}:{addr[1]} 登入成功\033[0m")
            conn.sendall(msg_success.encode('utf-8'))
            Sys_login.changeonline(account_from_client)
        else:
            logging.warning(f"\033[31m來源: {addr[0]}:{addr[1]} 登入失敗\033[0m")
            conn.sendall(msg_faild.encode('utf-8'))
    except Exception as e:
        logging.error(f"\033[31m來源: {addr[0]}:{addr[1]} 時發生錯誤: {e}\033[0m")
    finally:
        conn.close()
    
    print("###=========================###")
    print(f"\033[46m以結束與 {addr[0]}:{addr[1]} 的登入連線\033[0m" )
    print("###=========================###")
 
def game_server(conn, addr):
    _trashkiller = 0 
    logging.info(f"\033[33m來源: {addr[0]}:{addr[1]} 的遊戲請求\033[0m")
    try:
        while True:
            message = conn.recv(1024).decode('utf-8')
                          
            if message.startswith("CAN_I_WATCH:"):
                roomid = message.split(":")[1]
                re = GS.get_gamestatus('r'+str(roomid))
                conn.sendall(re.encode('utf-8'))
            elif message.startswith("GIVE_ME_BOARD:"):
                roomid = message.split(":")[1]
                re = GS.get_board_as_2d_array('r'+str(roomid))
                board_json = json.dumps(re)
                conn.sendall(board_json.encode('utf-8'))
            elif message.startswith("NOW_MOVE:"):
                roomid = message.split(":")[1]
                re = GS.get_nowmove('r'+str(roomid))
                conn.sendall(re.encode('utf-8'))
            elif message.startswith("NOW_TEAM:"):
                roomid = message.split(":")[1]
                re = GS.get_nowteam('r'+str(roomid))
                conn.sendall(re.encode('utf-8'))
            elif message.startswith("CREATE_ROOM:"):
                userid = message.split(":")[1]
                re = Sgr.can_i_create(str(userid))
                if (re == True):
                    roomnum = Sgr.createroom(userid,'classic')
                    reback = f'success:{roomnum:04}'
                else:
                    reback = 'faild'                    
                conn.sendall(reback.encode('utf-8'))
            elif message.startswith("CAN_I_JOIN:"):
                userid = message.split(":")[1]
                roomid ='r'+message.split(":")[2]
                re2 = Sgr.can_i_create(userid)
                if (re2 == True):
                    re = Sgr.joinroom(roomid,userid)
                else:
                    re = 'faild'
                if (re == 'success' and re2 == True):
                    reback = f'success'
                else:
                    if (re2 == True):
                        reback = '找不到房間 / 房間已滿'
                    else:
                        reback = '你是花心大蘿蔔(你已經在其他房間了!)'                  
                conn.sendall(reback.encode('utf-8'))
            
            elif message.startswith("Checkroomstatus:"):
                room = message.split(":")[1]
                reback = Sgr.get_room_status(room)
                conn.sendall(reback.encode('utf-8'))
                
            elif message.startswith("CheckWHOWIN:"):
                room = message.split(":")[1]
                reback = Sgr.get_who_win(room)
                conn.sendall(reback.encode('utf-8'))
                  
            elif message.startswith("Movechess:"):
                
                red_pieces = {'俥', '傌', '相', '仕', '帥', '炮', '兵'}
                black_pieces = {'車', '馬', '象', '士', '將', '砲', '卒'}
                
                locate = message.split(":")[1]
                roomnum = message.split(":")[2]
                
                #print(locate)
                #print(roomnum)
                
                x1 = int(locate[0])
                y1 = int(locate[1])
                x2 = int(locate[2])
                y2 = int(locate[3])
                
                team = GS.get_nowteam('r'+str(roomid))
                arr = GS.get_board_as_2d_array('r'+str(roomid))
                
                print(arr[x1][y1])
                if (team == 'red'):
                    if (arr[x1][y1] not in red_pieces):
                        #print(arr[y1][x1])
                        conn.sendall("不可以動別人的棋子".encode('utf-8'))
                    else:
                        #print("duck")
                        looogiccc = move_serch_r.r_move_main(arr[x1][y1],x1,y1,arr,x2,y2)
                        if (looogiccc == 'success'):
                            print(GS.move_piece_and_save(('r'+str(roomid)),x1,y1,x2,y2))
                            conn.sendall("success".encode('utf-8'))
                        else:
                            conn.sendall("無效的移動步驟".encode('utf-8'))
                elif (team == 'black'):
                    if (arr[x1][y1] not in black_pieces):
                        #print(arr[y1][x1])
                        conn.sendall("不可以動別人的棋子".encode('utf-8'))
                    else:
                        #print("duck")
                        looogiccc = move_serch_b.b_move_main(arr[x1][y1],x1,y1,arr,x2,y2)
                        if (looogiccc == 'success'):
                            print(GS.move_piece_and_save(('r'+str(roomid)),x1,y1,x2,y2))
                            conn.sendall("success".encode('utf-8'))
                        else:
                            conn.sendall("無效的移動步驟".encode('utf-8'))
            
            elif message == 'disconn':
                print(addr[0],addr[1],'中斷遊戲大廳連線')
                break
            else:
                logging.warning(f"aaaa未知訊息: {message}")
                _trashkiller+=1
                if (_trashkiller >10000):
                    break
                
    except Exception as e:
        logging.error(f"處理大廳請求時發生錯誤: {e}")
        
    finally:
        conn.close()

def run_server(port,handler):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', port))
        server_socket.listen(number_of_max_con)  
        
        print("###=========================###")
        print(f"\033[33mwarning : { handler } 開始監聽 \033[0m\n")
        print("監聽於 port " , port)
        print("最大監聽數: ",number_of_max_con )
        print("###=========================###")


        while True:
            try:
                client_socket, client_address = server_socket.accept()
                threading.Thread(target=handler, args=(client_socket,client_address,)).start()
                #logging.info(f"目前活動的連線數: {threading.active_count() - 1}")
            except Exception as e:
                logging.error(f"接受連線時發生錯誤: {e}")


if __name__ == '__main__':
    #run_server()
    threading.Thread(target=run_server,args=(login_server_port,login_server)).start()
    time.sleep(1)
    threading.Thread(target=run_server,args=(register_server_port,register_server)).start()
    time.sleep(1)
    threading.Thread(target=run_server, args=(lobby_server_port, lobby_server)).start()
    time.sleep(1)
    threading.Thread(target=run_server, args=(game_server_port, game_server)).start()