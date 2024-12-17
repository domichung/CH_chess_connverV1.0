import tkinter as tk
from tkinter import messagebox
from PIL import Image , ImageTk
import socket
import pygame

class register_status:
    def __init__(self, port, account, passwd, email, checkpasswd, addr = ''):
        if (addr == ''):
            self.relocate = 0
            self.register_serverip = '127.0.0.1'
            self.register_serverport = 65
        else:
            self.relocate = 1
            self.register_serverip = addr
            self.register_serverport = port
        
        self.email = email
        self.account  = account
        self.passwd   = passwd
        self.checkpasswd = checkpasswd
        self.account_null = 1
        self.passwd_null = 1
        self.checkpasswd_null = 1
        self.email_null = 1
        
    def w_account(self,account):
        self.account = account
        if ( account != '' ):
            self.account_null = 0
    
    def w_password(self,password):
        self.passwd = password
        if ( password != '' ):
            self.passwd_null = 0
    
    def w_email(self,email):
        self.email = email
        if (email != ''):
            self.email_null = 0
    
    def w_checkpasswd(self,checkpasswd):
        self.checkpasswd = checkpasswd
        if (checkpasswd != ''):
            self.checkpasswd_null = 0
    
    def conn_register_server(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.register_serverip, self.register_serverport))
                client_socket.sendall(self.account.encode('utf-8'))
                data = client_socket.recv(1024)
                recive = data.decode('utf-8')
                #print('account_re',recive)
                
                client_socket.sendall(self.passwd.encode('utf-8'))
                data2 = client_socket.recv(1024)
                recive2 = data2.decode('utf-8')
                #print('passwd_re',recive2)
                
                client_socket.sendall(self.email.encode('utf-8'))
                data3 = client_socket.recv(1024)
                recive3 = data3.decode('utf-8')
                #print('mail',recive3)
                if (recive3 == '-exsist'):
                    self.window_faild('帳號/mail 已經存在 請重新註冊')
                    return 'faild'
                elif (recive3 == '+success'):
                    self.window_success('註冊成功,可以去登入了!')
                    return 'success'
                else:
                    self.window_faild("發生錯誤: \n請聯繫系統管理員")
        except ConnectionRefusedError:
            self.window_faild('無法連線到伺服器，請稍後。')
            return '-faild'
            #print("無法連線到伺服器，請稍後。")
        except Exception as e:
            self.window_faild(f"發生錯誤: {e}\n請聯繫系統管理員")
            return '-faild'
            #print(f"發生錯誤: {e}\n請聯繫系統管理員")
    
    def window_faild(self,reason):
        messagebox.showinfo('註冊失敗', reason)
        
    def window_success(self,reason):
        messagebox.showinfo('註冊成功',reason)
            
class New_account_interface(register_status):
    def __init__(self):
        
        pygame.init()
        self.GUI = tk.Tk()
        self.GUI.title('瘋狂象棋 (註冊介面)')
        self.play_music_silence = 0
        self.account = tk.StringVar()
        self.email = tk.StringVar()
        self.passwd = tk.StringVar()
        self.checkpasswd = tk.StringVar()
        self.conn = register_status(account='',passwd='',port='',email='',checkpasswd='')
        self.exit_process = 0
        
    def register_try(self):
        self.conn.email_null = 1
        self.conn.passwd_null = 1
        self.conn.account_null = 1
        self.conn.checkpasswd_null = 1
        self.conn.passwd = ''
        self.conn.account = ''
        self.conn.email = ''
        self.conn.checkpasswd = ''
        
        self.conn.w_account(str(self.account.get()))
        self.conn.w_email(str(self.email.get()))
        self.conn.w_password(str(self.passwd.get()))
        self.conn.w_checkpasswd(str(self.checkpasswd.get()))
        
        if (self.conn.account_null == 1):
            self.conn.window_faild('未輸入帳號')
            self.GUI.destroy()
            return 1
        elif (self.conn.passwd_null == 1):
            self.conn.window_faild('未輸入密碼')
            self.GUI.destroy()
            return 1
        elif (self.conn.checkpasswd_null == 1):
            self.conn.window_faild('未再次確認密碼')
            self.GUI.destroy()
            return 1 
        elif (self.conn.email_null == 1):
            self.conn.window_faild('未輸入電子郵件')
            self.GUI.destroy()
            return 1
        elif(self.conn.passwd != self.conn.checkpasswd):
            self.conn.window_faild('密碼與確認密碼不符')
            self.GUI.destroy()
            return 1
        else:
            tmp = self.conn.conn_register_server()
            if (tmp == 'success'):
                self.exit_process = 1
                
            self.GUI.destroy()
            return 1
        
    def window_size(self):
        width = self.GUI.winfo_screenwidth()
        height = self.GUI.winfo_screenheight()
        size = f"{width}x{height}"
        self.GUI.geometry(size)

    def play_music(self):
        pygame.mixer.music.load("music/Travel_to_Your_World.mp3") #Loading File Into Mixer
        pygame.mixer.music.play(55) #Playing It In The Whole Device
        pygame.mixer.music.set_volume(0.1)
    
    def play_music_volum(self):
        self.play_music_silence = (self.play_music_silence+1)%2
        if (self.play_music_silence == 0):
            pygame.mixer.music.set_volume(0.1)
            self.btn3.configure( text="🔊",bg="Green", fg="white")
        else:
            pygame.mixer.music.set_volume(0)
            self.btn3.configure( text="🔈",bg="Red", fg="white")
    
    def window_items(self):
        
        self.GUI.iconbitmap('wow.ico')
        self.play_music()  
        self.login_background = ImageTk.PhotoImage(Image.open('back.jpg'))
        
        bg_label = tk.Label(self.GUI, image=self.login_background)
        bg_label.place(relwidth=1, relheight=1)  # 將背景圖片覆蓋整個視窗
        
        # 取得圖片大小，並鎖定視窗大小
        img_width, img_height = self.login_background.width(), self.login_background.height()
        self.GUI.geometry(f"{img_width}x{img_height}")
        self.GUI.resizable(False, False)  # 鎖定視窗大小
        
        center_x = img_width // 2
        center_y = img_height // 2
        
        self.header = tk.Label(self.GUI,text="閃亮亮註冊介面",bg="white", font=("Arial", 12)).place(x=280, y=60, width=125, height=25)
        
        tk.Label(self.GUI, text="帳號", bg="white", font=("Arial", 12)).place(x=center_x - 150, y=145, width=50, height=25)
        input_account = tk.Entry(self.GUI, textvariable=self.account, font=("Arial", 12))
        input_account.place(x=center_x - 90, y=145, width=200, height=25)
        input_account.configure(bg='#ffffff', highlightbackground='#cccccc', highlightthickness=1)
        
        # 密碼輸入框
        tk.Label(self.GUI, text="密碼", bg="white", font=("Arial", 12)).place(x=center_x - 150, y=185, width=50, height=25)
        input_passwd = tk.Entry(self.GUI, textvariable=self.passwd, show="*", font=("Arial", 12))
        input_passwd.place(x=center_x - 90, y=185, width=200, height=25)
        input_passwd.configure(bg='#ffffff', highlightbackground='#cccccc', highlightthickness=1)
        
        # 確認密碼輸入框
        tk.Label(self.GUI, text="重複密碼", bg="white", font=("Arial", 12)).place(x=center_x - 170, y=225, width=70, height=25)
        input_checkpasswd = tk.Entry(self.GUI, textvariable=self.checkpasswd, show="*", font=("Arial", 12))
        input_checkpasswd.place(x=center_x - 90, y=225, width=200, height=25)
        input_checkpasswd.configure(bg='#ffffff', highlightbackground='#cccccc', highlightthickness=1)
        
        #電子郵件
        tk.Label(self.GUI, text="電子郵件", bg="white", font=("Arial", 12)).place(x=center_x - 170, y=265, width=70, height=25)
        input_mail = tk.Entry(self.GUI, textvariable=self.email, font=("Arial", 12))
        input_mail.place(x=center_x - 90, y=265, width=200, height=25)
        input_mail.configure(bg='#ffffff', highlightbackground='#cccccc', highlightthickness=1)
        
        btn = tk.Button(self.GUI, text='註冊', command=self.register_try, bg="blue", fg="white", font=("Arial", 12))
        btn.place(x=center_x - 40 , y=305, width=100, height=30)
        
        # 離開程式按鈕
        btn2 = tk.Button(self.GUI, text='結束程式', command=self.exit_program, bg="red", fg="white", font=("Arial", 12))
        btn2.place(x=center_x*2-100, y=center_y*2-30, width=100, height=30)

        # 音樂按鈕
        self.btn3 = tk.Button(self.GUI, text="🔊", command=self.play_music_volum, bg="Green", fg="white", font=("Arial", 12))
        self.btn3.place(x=0,y=center_y*2-30, width=30, height=30)
        
    
    def exit_program(self):
        confirm = messagebox.askyesno('確認退出', '您確定要退出註冊介面嗎？')
        if confirm:
            self.exit_process = 1
            self.GUI.destroy()

    def window_faild(self,reason):
        messagebox.showinfo('註冊失敗', reason)
        
    def wake_interface(self):
        self.window_size()
        self.window_items()
        self.GUI.mainloop()
        return self.exit_process
        