import tkinter as tk

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x250')

tk.Label(root, bitmap='error').pack()
tk.Label(root, bitmap='hourglass').pack()
tk.Label(root, bitmap='info').pack()
tk.Label(root, bitmap='questhead').pack()
tk.Label(root, bitmap='question').pack()
tk.Label(root, bitmap='warning').pack()
tk.Label(root, bitmap='gray12').pack()
tk.Label(root, bitmap='gray25').pack()
tk.Label(root, bitmap='gray50').pack()
tk.Label(root, bitmap='gray75').pack()

root.mainloop()