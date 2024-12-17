import obj_Login
import sys
import tkinter


def main():
    
    while(1):
        showgui = obj_Login.login_gui()
        #showgui.window_size()
        showgui.window_item()
        temp = showgui.wake()
                
        if (temp == 1):
            break    
    

if __name__ == '__main__':
    main()