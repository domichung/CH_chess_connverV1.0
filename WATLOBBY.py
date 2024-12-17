import tkinter as tk
from tkinter import messagebox
import pygame
import socket
import time
import threading
import queue
import os
from PIL import Image , ImageTk
import json
import Sys_waitlobby_item as SWI
import tkinter.simpledialog as simpledialog


class WaitingLobby:
    def __init__(self, account):
        pygame.init()
        self.GUI = tk.Tk()
        self.GUI.title('瘋狂象棋 (大廳介面)')
        self.account = account
        self.music_value = 0.1
        self.server_connection = None
        self.keep_alive = True
        self.message_queue = queue.Queue()
        self.lobby_background = ImageTk.PhotoImage(Image.open('back3.jpg'))
        self.ingame = 0
        self.game_window = None 
        
        pygame.mixer.music.set_volume(self.music_value)
        
        self.GUI.protocol("WM_DELETE_WINDOW", self.exit_program)
        
        # 設置定期檢查消息隊列的方法
        self.GUI.after(100, self.check_message_queue)

    def connect_to_server(self):
        try:
            self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_connection.connect(("127.0.0.1", 75))
            self.server_connection.sendall(f"LOGIN:{self.account}".encode('utf-8'))
            response = self.server_connection.recv(1024).decode('utf-8')
            print(f"伺服器回應: {response}")

            threading.Thread(target=self.heartbeat_loop, daemon=True).start()
        except Exception as e:
            self.message_queue.put(('error', f"無法連接伺服器: {e}"))

    def check_message_queue(self):
        """定期檢查消息隊列並在主線程處理"""
        try:
            while not self.message_queue.empty():
                msg_type, msg = self.message_queue.get_nowait()
                
                if msg_type == 'error':
                    messagebox.showerror("錯誤", msg)
                    self.exit_program()
                elif msg_type == 'disconnect':
                    messagebox.showerror("連線中斷", msg)
                    self.exit_program()
                elif msg_type == 'music_permission':
                    # Handle permission response for music change
                    self.music_permission_response(msg)
        except queue.Empty:
            pass
        
        # 持續檢查消息隊列
        if self.keep_alive:
            self.GUI.after(100, self.check_message_queue)

    def heartbeat_loop(self):
        """持續向伺服器發送心跳以保持在線"""
        try:
            while self.keep_alive:
                self.server_connection.sendall("HEARTBEAT".encode('utf-8'))
                response = self.server_connection.recv(1024).decode('utf-8')
                print(f"{response}")
                
                if response != "HEARTBEAT_OK":
                    raise ConnectionError("心跳回應異常")
                
                time.sleep(5)  # 每 5 秒發送一次心跳
        except Exception as e:
            self.keep_alive = False
            # 將異常消息放入佇列，在主線程處理
            self.message_queue.put(('disconnect', f"與伺服器的連線中斷: {e}"))

    def music_mode(self):
        SWI.MusicSettingWindow(self)

    def shop_mode(self):
        SWI.ShopSettingWindow(self)
        
    def Rank_Show(self):
        SWI.LeaderboardWindow(self)
    
    def exit_program(self):
        confirm = messagebox.askyesno('瘋狂象棋', '主公你忍心離開我們嗎？')
        if confirm:
            self.keep_alive = False

            # 關閉網絡連接
            if self.server_connection:
                try:
                    self.server_connection.sendall("LOGOUT".encode('utf-8'))
                    self.server_connection.close()
                except Exception as e:
                    print(f"退出時發生錯誤: {e}")
        
            # 停止音樂
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception:
                pass

            # 確保只執行一次銷毀
            if self.GUI.winfo_exists():
                self.GUI.quit()
                self.GUI.destroy()

    def fin_play_music(self):
        pygame.mixer.music.load("music/Travel_to_Your_World.mp3") #Loading File Into Mixer
        pygame.mixer.music.play(55) #Playing It In The Whole Device
        pygame.mixer.music.set_volume(0.1)
        
    def window_items(self):
        """建立大廳介面"""
        self.fin_play_music()
        bg_label = tk.Label(self.GUI, image=self.lobby_background)
        bg_label.place(relwidth=1, relheight=1)  # 將背景圖片覆蓋整個視窗

        # 取得圖片大小，並鎖定視窗大小
        img_width, img_height = self.lobby_background.width(), self.lobby_background.height()
        self.GUI.geometry(f"{img_width}x{img_height}")
        self.GUI.resizable(False, False)  # 鎖定視窗大小
        
        img_width, img_height = self.lobby_background.width(), self.lobby_background.height()
        
        center_x = img_width // 2
        center_y = img_height // 2
        
        welcome_label = tk.Label(self.GUI, text=f"歡迎：{self.account}", font=("Helvetica", 16))
        welcome_label.pack(pady=20)
        
        start_button = tk.Button(self.GUI, text="開始遊戲", command=self.start_game)
        start_button.pack(pady=20)

        showrank_button = tk.Button(self.GUI, text="排行榜", command=self.Rank_Show)
        showrank_button.pack(pady=20)
        
        shop_button = tk.Button(self.GUI, text="商城", command=self.shop_mode)
        shop_button.pack(pady=20)
        
        music_button = tk.Button(self.GUI, text="🎵", command=self.music_mode)
        music_button.place(x=0,y=center_y*2-30, width=30, height=30)

        exit_button = tk.Button(self.GUI, text="離開遊戲", command=self.exit_program)
        exit_button.pack(pady=20)

    def start_game(self):
        """Start game, bring the existing window to the front if already created"""
        if self.game_window and self.game_window.winfo_exists():
            self.game_window.lift()
        else:
            self.game_window = GameStartWindow(self)  
    
    def wake_lobby(self):
        """初始化並啟動大廳"""
        self.connect_to_server()
        #self.window_size()
        self.window_items()
        self.GUI.mainloop()

    def music_permission_response(self, response):
        """處理伺服器回應的音樂變更許可"""
        if response == "CAN_CHANGE":
            messagebox.showinfo("音樂控制", "您可以更改音樂設定")
        else:
            messagebox.showwarning("音樂控制", "您無權更改音樂設定")
        

class GameStartWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent.GUI)
        self.parent = parent
        self.title('開始遊戲')
        self.geometry(f"{450}x{380}")
        self.resizable(False, False)

        # Set up socket connection here
        self.server_ip = '127.0.0.1'  # Change this to your server's IP
        self.server_port = 85  # Change this to your server's port
        self.socket = None

        # Try to connect to the server
        self.connect_to_server()

        self.create_widgets()

    def create_widgets(self):
        """建立開始遊戲介面元件"""
        tk.Label(self, text="遊戲選單", font=("Arial", 16)).pack(pady=20)

        # 巔峰對決按鈕
        tk.Button(self, text="巔峰對決", font=("Arial", 14), command=self.start_peak_duel).pack(pady=10)

        # 休閒競賽按鈕
        tk.Button(self, text="休閒競賽", font=("Arial", 14), command=self.show_casual_competition).pack(pady=10)

        # 觀看對局按鈕
        tk.Button(self, text="觀看對局", font=("Arial", 14), command=self.watch_match).pack(pady=10)

        # 關閉介面按鈕
        tk.Button(self, text="關閉介面", font=("Arial", 14), command=self.close_window).pack(pady=10)

    def start_peak_duel(self):
        messagebox.showinfo("系統公告", "賽季已結束但能透過商城繼續買分")

    def show_casual_competition(self):
        """彈出新窗口顯示創建或加入房間選項"""
        casual_window = CasualCompetitionWindow(self)
        casual_window.grab_set() 

    def watch_match(self):
        """Create a window to input the room number"""
        self.watch_window = tk.Toplevel(self)
        self.watch_window.title("請輸入要觀戰的房間號碼")
        self.watch_window.geometry("350x150")

        # Add a label and input field for the room number
        tk.Label(self.watch_window, text="前往觀戰的房間號碼:", font=("Arial", 12)).pack(pady=10)
        self.room_number_entry = tk.Entry(self.watch_window, font=("Arial", 12))
        self.room_number_entry.pack(pady=10)

        # Add the "Submit" button
        tk.Button(self.watch_window, text="提交", font=("Arial", 12), command=self.submit_room_number).pack(pady=10)

    def submit_room_number(self):
        """Submit the room number and start watching"""
        room_number = self.room_number_entry.get()
        if room_number.isdigit() and 1 <= int(room_number) <= 9999 and len(room_number) == 4:
            
            self.socket.sendall(f"CAN_I_WATCH:{room_number}".encode('utf-8'))
            gstatus = self.socket.recv(1024).decode('utf-8')
            #print(gstatus)
            if (gstatus == 'playing'):
                self.watch_window.destroy()
                self.Watching_window(room_number)
            else:
                if (gstatus == 'end'):
                    tk.messagebox.showerror("錯誤", "遊戲已結束下次請早！")
                elif (gstatus == 'waiting'):
                    tk.messagebox.showerror("錯誤", "遊戲尚未開始晚點再來！")
                elif (gstatus == 'not_exist'):
                    tk.messagebox.showerror("錯誤", "遊戲房間不存在")
                else:
                    tk.messagebox.showerror("錯誤", "被你玩壞了 = =")
        else:
            tk.messagebox.showerror("錯誤", "房間號碼必須是介於 0001 到 9999 的四位數字！")

    def Watching_window(self, room_number):
        """Create a new window with a grid-based chessboard"""
        self.playing_window = tk.Toplevel(self)
        self.playing_window.title("觀戰中")
        self.playing_window.geometry("700x700")

        # Add a label for the room number
        tk.Label(self.playing_window, text=f"觀戰房間編號: {room_number}", font=("Arial", 12)).pack()

        # Create a frame for the chessboard
        self.board_frame = tk.Frame(self.playing_window)
        self.board_frame.pack(pady=20)

        # Create the chessboard grid
        self.board_cells = []
        for row in range(10):
            row_cells = []
            for col in range(9):
                cell = tk.Label(self.board_frame, text="", width=4, height=2, borderwidth=1, relief="solid", font=("Arial", 14))
                cell.grid(row=row, column=col, padx=2, pady=2)
                row_cells.append(cell)
            self.board_cells.append(row_cells)

        # Add a turn indicator label
        self.turn_label = tk.Label(self.playing_window, text="", font=("Arial", 12))
        self.turn_label.pack(pady=10)

        # Exit button
        tk.Button(self.playing_window, text="離開", font=("Arial", 14), command=self.playing_window.destroy).pack(pady=10)

        # Periodically check the game status
        self.check_game_status(room_number)

    def update_board(self, board_data, name, team):
        """Update the chessboard display with new data"""
        red_pieces = {'俥', '傌', '相', '仕', '帥', '炮', '兵'}
        blue_pieces = {'車', '馬', '象', '士', '將', '砲', '卒'}

        for row in range(10):
            for col in range(9):
                piece = board_data[row][col]
                cell = self.board_cells[row][col]
                cell.config(text=piece)

                # Set cell background color based on piece type
                if piece in red_pieces:
                    cell.config(bg="red", fg="white")
                elif piece in blue_pieces:
                    cell.config(bg="blue", fg="white")
                else:
                    cell.config(bg="white", fg="black")

        # Update turn label
        if team == 'red':
            team = '紅'
            cf = 'red'
        elif team == 'black':
            team = '黑'
            cf = 'blue'
            
        self.turn_label.config(text=f"現在輪到 {team}方 的 {name}",fg=cf)

    def check_game_status(self, room_number):
        """Check game status and update the board periodically"""
        if self.socket:
            try:                
                # Request the board state
                self.socket.sendall(f"GIVE_ME_BOARD:{room_number}".encode('utf-8'))
                board_json = self.socket.recv(1024).decode('utf-8')
                board_data = json.loads(board_json)

                # Request the current player's turn
                self.socket.sendall(f"NOW_MOVE:{room_number}".encode('utf-8'))
                name = self.socket.recv(1024).decode('utf-8')

                self.socket.sendall(f"NOW_TEAM:{room_number}".encode('utf-8'))
                team = self.socket.recv(1024).decode('utf-8')

                # Update the board
                self.update_board(board_data, name, team)

            except Exception as e:
                print(f"Error updating board: {e}")

            # Schedule the next update
            self.playing_window.after(2000, self.check_game_status, room_number)

    def connect_to_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            print("成功連接到伺服器！")
        except Exception as e:
            print(f"連接伺服器時發生錯誤: {e}")
            tk.messagebox.showerror("錯誤", f"連接伺服器時發生錯誤: {e}")

    def close_window(self):
        if self.socket:
            self.socket.sendall(f"disconn".encode('utf-8'))
            self.socket.close()
        self.destroy()


class CasualCompetitionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("休閒競賽")
        self.geometry("300x200")
        self.resizable(False, False)
        self.parent = parent  # Reference to the parent window

        self.create_widgets()

    def create_widgets(self):
        """建立休閒競賽選項介面"""
        tk.Label(self, text="自定義模式", font=("Arial", 16)).pack(pady=20)

        # 創建房間按鈕
        tk.Button(self, text="創建房間", font=("Arial", 14), command=self.create_room).pack(pady=10)

        # 加入房間按鈕
        tk.Button(self, text="加入房間", font=("Arial", 14), command=self.join_room).pack(pady=10)

    def create_room(self):
        """創建房間並向伺服器發送請求"""
        try:
            self.parent.socket.sendall(f"CREATE_ROOM:{self.parent.parent.account}".encode('utf-8'))
            response = self.parent.socket.recv(1024).decode('utf-8')

            print(response)
            if response.startswith("success"):
                roomid = response.split(":")[1]
                self.open_waiting_window(roomid)
            else:
                tk.messagebox.showerror("錯誤", "你正在遊玩其他房間 請離線5分鐘後再回來試！")
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"創建房間時發生錯誤: {e}")

    def open_waiting_window(self, roomid):
        """打開等待視窗並輪詢房間狀態"""
        waiting_window = tk.Toplevel(self)
        waiting_window.title("等待中")
        waiting_window.geometry("300x150")
        tk.Label(waiting_window, text=f"等待房間 (房號: {roomid})", font=("Arial", 14)).pack(pady=20)
        status_label = tk.Label(waiting_window, text="狀態: Waiting", font=("Arial", 12))
        status_label.pack(pady=10)

        def check_room_status():
            while True:
                try:
                    self.parent.socket.sendall(f"Checkroomstatus:{roomid}".encode('utf-8'))
                    response = self.parent.socket.recv(1024).decode('utf-8')
                    if response == "waiting":
                        time.sleep(2)
                    elif response == "playing":
                        waiting_window.destroy()
                        self.open_game_interface(roomid)
                        break
                    else:
                        waiting_window.destroy()
                        tk.messagebox.showerror("錯誤", "發生未預期之錯誤請重啟遊戲")
                        break
                except Exception as e:
                    waiting_window.destroy()
                    tk.messagebox.showerror("錯誤", f"檢查房間狀態時發生錯誤: {e}")
                    break

        threading.Thread(target=check_room_status, daemon=True).start()

    def open_game_interface(self, roomid):
        """打開遊戲介面，顯示 9x10 的按鍵"""
        game_window = tk.Toplevel(self)
        game_window.title("遊戲中")
        game_window.geometry("500x600")
        buttons = []

        def button_clicked(x, y):
            """按鈕被按下時顯示座標"""
            print(f"按下了座標: ({x}, {y})")
            self.parent.socket.sendall(f"NOW_MOVE:{roomid}".encode('utf-8'))
            response = self.parent.socket.recv(1024).decode('utf-8')
            
            if (response != self.parent.parent.account):
                tk.messagebox.showerror("錯誤", f"現在不是你的回合")
                return
            
            new_x = simpledialog.askstring("輸入框", f"座標: ({x}, {y})\n你要把它移去哪呢? 請輸入新的 y 值：")
            if new_x is None or not new_x.isdigit() or not (0 <= int(new_x) <= 8):
                tk.messagebox.showerror("錯誤", f"無效x值")
                return
            new_y = simpledialog.askstring("輸入框", f"座標: ({x}, {y})\n你要把它移去哪呢? 請輸入新的 x 值：")
            if new_y is None or not new_y.isdigit() or not (0 <= int(new_y) <= 9):
                tk.messagebox.showerror("錯誤", f"無效y值")
                return
            if ( x == new_x and y == new_y):
                tk.messagebox.showerror("錯誤", f"你沒有進行位置的移動")
                return
            
            if new_x and new_y:
                self.parent.socket.sendall(f"Movechess:{str(x)}{str(y)}{str(new_x)}{str(new_y)}:{roomid}".encode('utf-8'))
                response = self.parent.socket.recv(1024).decode('utf-8')
                if (response == 'success'):
                    tk.messagebox.showinfo("移動成功", response)
                    return
                else:
                    tk.messagebox.showerror("移動失敗",response)
                    return
            else:
                print("取消輸入")
        
        # 創建9x10的按鍵並存儲在buttons列表
        for i in range(10):
            row = []
            for j in range(9):
                # 將 x, y 傳遞到 button_clicked 方法
                btn = tk.Button(game_window, text="", width=4, height=2, font=("Arial", 12),
                                command=lambda x=i, y=j: button_clicked(x, y))
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            buttons.append(row)

        def refresh_board():
            while True:
                try:
                    red_pieces = {'俥', '傌', '相', '仕', '帥', '炮', '兵'}
                    blue_pieces = {'車', '馬', '象', '士', '將', '砲', '卒'}
                    self.parent.socket.sendall(f"GIVE_ME_BOARD:{roomid}".encode('utf-8'))
                    response = self.parent.socket.recv(1024).decode('utf-8')
                    
                    self.parent.socket.sendall(f"Checkroomstatus:{roomid}".encode('utf-8'))
                    finalresponse = self.parent.socket.recv(1024).decode('utf-8')
                    
                    if (finalresponse == 'end'):
                        self.parent.socket.sendall(f"CheckWHOWIN:{roomid}".encode('utf-8'))
                        winner = self.parent.socket.recv(1024).decode('utf-8')
                        if (winner == self.parent.parent.account):
                            tk.messagebox.showinfo("獲勝", "戴著帽子的敵人被掃地僧打飛了...")
                        else:
                            tk.messagebox.showinfo("失敗", "你上課偷去廁所被掃地僧打飛了...")
                        
                        break
                    
                    board = eval(response)  # 假設伺服器回傳的是一個9x10陣列的字串，如[[...], [...], ...]
                    for i in range(10):
                        for j in range(9):
                            piece = board[i][j]
                            if piece in red_pieces:
                                color = "red"
                            elif piece in blue_pieces:
                                color = "blue"
                            else:
                                color = "black"  # 默認顏色
                            buttons[i][j].config(text=piece, fg=color)
                    time.sleep(1)
                except Exception as e:
                    game_window.destroy()
                    tk.messagebox.showerror("錯誤", f"刷新遊戲介面時發生錯誤: {e}")
                    break

        threading.Thread(target=refresh_board, daemon=True).start()

    def join_room(self):
        try:
            # 彈出輸入框讓用戶輸入房間號
            roomid = simpledialog.askstring("加入房間", "請輸入房間號:")
            if not roomid:  # 如果沒有輸入房間號
                tk.messagebox.showerror("錯誤", "房間號不可為空")
                return
        
            # 驗證房間號是否合法（>0，<10000，長度為4）
            if not roomid.isdigit():  # 檢查是否為數字
                tk.messagebox.showerror("錯誤", "房間號必須是數字")
                return
        
            roomid_int = int(roomid)
            if roomid_int <= 0 or roomid_int >= 10000:
                tk.messagebox.showerror("錯誤", "房間號必須大於 0 且小於 10000")
                return
            if len(roomid) != 4:
                tk.messagebox.showerror("錯誤", "房間號長度必須為 4 位")
                return
        
            # 發送加入房間請求到伺服器，將account和roomid加入請求中
            self.parent.socket.sendall(f"CAN_I_JOIN:{self.parent.parent.account}:{roomid}".encode('utf-8'))
            response = self.parent.socket.recv(1024).decode('utf-8')

            if response.startswith("success"):
                tk.messagebox.showinfo("成功", "成功加入房間")
                # 房間加入成功後，打開棋盤界面
                self.open_game_interface(roomid)
            else:
                tk.messagebox.showerror("錯誤", response)
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"加入房間時發生錯誤: {e}")
        
        

##def main():
#    # 主程式入口
#    lobby = WaitingLobby(account='test')
#    lobby.wake_lobby()
    


#if __name__ == "__main__":
#    main()