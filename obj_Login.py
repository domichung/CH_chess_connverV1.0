import tkinter as tk
import socket
from tkinter import messagebox
import WATLOBBY
import obj_Newaccount as ONC
from PIL import Image , ImageTk
import pygame

class login_status:
    def __init__(self, port, account, passwd, addr = ''):
        if (addr == ''):
            self.relocate = 0
            self.login_serveerip = '127.0.0.1'
            self.login_serveerport = 55
        else:
            self.relocate = 1
            self.login_serveerip = addr
            self.login_serveerport = port
            
        self.account  = account
        self.passwd   = passwd
        self.account_null = 1
        self.passwd_null = 1
        
    def w_account(self,account):
        self.account = account
        if ( account != '' ):
            self.account_null = 0
    
    def w_password(self,password):
        self.passwd = password
        if ( password != '' ):
            self.passwd_null = 0
    
    def login(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            
                client_socket.connect((self.login_serveerip, self.login_serveerport))
        
                client_socket.sendall(self.account.encode('utf-8'))


                data = client_socket.recv(1024)
                recive = data.decode('utf-8')
            
                #print(recive)

                #=============================================
                client_socket.sendall(self.passwd.encode('utf-8'))

                data = client_socket.recv(1024)
                recive2 = data.decode('utf-8')
            
                #print(recive2)
                
                if (recive == '+success' and recive2 == '+success'):
                    self.window_success(self.account)
                    return '+success'
                elif (recive2 =='-alreadyonline'):
                    self.window_faild('同名帳戶已於線上')
                    return '-faild'
                else:
                    self.window_faild('登入帳號/密碼有誤')
                    return '-faild'
        except ConnectionRefusedError:
            self.window_faild('無法連線到伺服器，請稍後。')
            return '-faild'
            #print("無法連線到伺服器，請稍後。")
        except Exception as e:
            self.window_faild(f"發生錯誤: {e}\n請聯繫系統管理員")
            return '-faild'
            #print(f"發生錯誤: {e}\n請聯繫系統管理員")
        
    def window_faild(self,reason):
        messagebox.showinfo('登入失敗', reason)
        
    def window_success(self,account):
        messagebox.showinfo('登入成功', ('歡迎使用者:'+ account))

class login_gui(login_status):
    def __init__(self):
        pygame.init()
        self.GUI = tk.Tk()
        self.GUI.title('瘋狂象棋(登入介面)')
        self.account = tk.StringVar()
        self.passwd = tk.StringVar()
        self.conn = login_status(account='',passwd='',port='')
        self.login_background = ImageTk.PhotoImage(Image.open('back.jpg'))
        self.exit_process = 0
        self.play_music_silence = 0
                        
    def login_try(self):
        
        self.conn.account_null = 1
        self.conn.passwd_null = 1
        self.conn.passwd = ''
        self.conn.account = ''

        self.conn.w_account(str(self.account.get()))
        self.conn.w_password(str(self.passwd.get()))
            
        if (self.conn.account_null == 1 or self.conn.passwd_null == 1):
            self.conn.window_faild('未輸入帳號 / 密碼')
            self.GUI.destroy()
            return 1
        else:
            status = self.conn.login()
            if (status == '+success'):
                self.GUI.quit()
                self.GUI.destroy()
               
                lobbygui = WATLOBBY.WaitingLobby(account=self.account.get())
                lobbygui.wake_lobby()  
                self.exit_process = 1
            else:
                self.GUI.destroy()
    
    
    def exit_program(self):
        confirm = messagebox.askyesno('瘋狂象棋', '主公你忍心離開我們嗎？')
        if confirm:
            self.exit_process = 1
            self.GUI.destroy()
    
    def marquee_move(self):
    # 跑馬燈移動的邏輯
        x = self.marquee_label.winfo_x()  # 取得目前跑馬燈的 x 位置
        width = self.marquee_label.winfo_width()  # 取得跑馬燈的寬度
        new_x = x - 2  # 調整跑馬燈移動速度 (每次左移 2 像素)
    
        # 如果跑馬燈完全移出畫面，則將它移回右邊
        if new_x + width < 0:
            new_x = self.GUI.winfo_width()  # 將跑馬燈放回視窗右側
    
        self.marquee_label.place(x=new_x, y=10)  # 設定新位置
        self.GUI.after(50, self.marquee_move)  # 每 50 毫秒更新一次位置，實現動畫效果
    
    def create_account(self):
        #print("fix")
        self.GUI.destroy()
        while (1):
            new_account_gui = ONC.New_account_interface()
            tmp = new_account_gui.wake_interface()
            if (tmp == 1):
                break
    
    def play_music(self):
        pygame.mixer.music.load("music/Travel_to_Your_World.mp3") #Loading File Into Mixer
        pygame.mixer.music.play(55) #Playing It In The Whole Device
        pygame.mixer.music.set_volume(0.1)
    
    def play_music_volum(self):
        self.play_music_silence = (self.play_music_silence+1)%2
        if (self.play_music_silence == 0):
            pygame.mixer.music.set_volume(0.1)
            self.music_btn.configure( text="🔊",bg="Green", fg="white")
        else:
            pygame.mixer.music.set_volume(0)
            self.music_btn.configure( text="🔈",bg="Red", fg="white")
    
    def window_item(self):
        
        self.play_music()  
        self.GUI.iconbitmap('wow.ico')
          
        bg_label = tk.Label(self.GUI, image=self.login_background)
        bg_label.place(relwidth=1, relheight=1)  # 將背景圖片覆蓋整個視窗

        # 取得圖片大小，並鎖定視窗大小
        img_width, img_height = self.login_background.width(), self.login_background.height()
        self.GUI.geometry(f"{img_width}x{img_height}")
        self.GUI.resizable(False, False)  # 鎖定視窗大小

        center_x = img_width // 2
        center_y = img_height // 2

        # 跑馬燈
        self.marquee_back = tk.Label(self.GUI, text="", bg="yellow", font=("Arial", 12))
        self.marquee_back.place(x=0, y=10, width=img_width, height=30)
        self.marquee_label = tk.Label(self.GUI, text="你也想成為棋靈王?!快來下棋吧!", bg="yellow", font=("Arial", 12))
        self.marquee_label.place(x=0, y=10, width=img_width, height=30)
        self.marquee_move()  # 開始跑馬燈移動
        
        # 帳號輸入框
        tk.Label(self.GUI, text="帳號:", bg="white", font=("Arial", 12)).place(x=center_x - 150, y=center_y - 40, width=50, height=25)
        input_account = tk.Entry(self.GUI, textvariable=self.account, font=("Arial", 12))
        input_account.place(x=center_x - 90, y=center_y - 40, width=200, height=25)
        input_account.configure(bg='#ffffff', highlightbackground='#cccccc', highlightthickness=1)

        # 密碼輸入框
        tk.Label(self.GUI, text="密碼:", bg="white", font=("Arial", 12)).place(x=center_x - 150, y=center_y + 10, width=50, height=25)
        input_passwd = tk.Entry(self.GUI, textvariable=self.passwd, show="*", font=("Arial", 12))
        input_passwd.place(x=center_x - 90, y=center_y + 10, width=200, height=25)
        input_passwd.configure(bg='#ffffff', highlightbackground='#cccccc', highlightthickness=1)

        # 登入按鈕
        login_btn = tk.Button(self.GUI, text='登入', command=self.login_try, bg="blue", fg="white", font=("Arial", 12))
        login_btn.place(x=center_x - 100, y=center_y + 60, width=100, height=30)
        
        # 註冊按鈕
        register_btn = tk.Button(self.GUI, text='註冊', command=self.create_account, bg="blue", fg="white", font=("Arial", 12))
        register_btn.place(x=center_x + 0, y=center_y + 60, width=100, height=30)
        
        # 離開按鈕
        leave_btn = tk.Button(self.GUI, text='結束程式', command=self.exit_program, bg="red", fg="white", font=("Arial", 12))
        leave_btn.place(x=center_x*2-100, y=center_y*2-30, width=100, height=30)
        
        # 音樂按鈕
        self.music_btn = tk.Button(self.GUI, text="🔊", command=self.play_music_volum, bg="Green", fg="white", font=("Arial", 12))
        self.music_btn.place(x=0,y=center_y*2-30, width=30, height=30)
        
    def wake(self):
        self.GUI.mainloop()
        return self.exit_process
        