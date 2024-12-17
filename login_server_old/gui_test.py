import _tkinter as tk


def login():
    print('hello')

root = tk.Tk()
root.title('瘋狂象棋(登入介面)')

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
size = str(width)+'x'+str(height)

root.geometry(size)

account = tk.StringVar()
passwd = tk.StringVar()

tk.Label(root, text="帳號:").pack()
input_account = tk.Entry(root, textvariable=account)  
input_account.pack()
tk.Label(root, text="密碼:").pack()
input_passwd = tk.Entry(root, textvariable=passwd)  
input_passwd.pack()

btn = tk.Button(root, text='登入', command=login)  
btn.pack()

root.mainloop()