import tkinter as tk
from tkinter import messagebox
import pygame
import socket
import time
import threading
import queue
import os
from PIL import Image , ImageTk


class MusicSettingWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent.GUI)
        self.parent = parent
        self.title('瘋狂象棋 (音量調整)')
        self.geometry(f"{450}x{380}")
        self.resizable(False, False)  # 鎖定視窗大小
        self.create_widgets()

        # 初始化權限變數
        self.has_permission = False

    def create_widgets(self):
        """建立子視窗內的音量調整元件"""
        tk.Label(self, text="音量調整", font=("Arial", 16)).pack(pady=20)
    
        self.check_music_permission()
    
        # 音量控制框架
        volume_frame = tk.Frame(self)
        volume_frame.pack(pady=10)

        # 音量滑桿
        self.volume_slider = tk.Scale(
            volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
            command=self.update_volume
        )
        self.volume_slider.set(self.parent.music_value * 100)  # 初始化滑桿值
        self.volume_slider.pack(side=tk.LEFT, padx=10)

        # 靜音按鈕
        self.mute_button = tk.Button(
            volume_frame, text="🔊", font=("Arial", 14), bg="Green", fg="white", command=self.toggle_mute
        )
        self.mute_button.pack(side=tk.LEFT)

        # 音樂檔案選擇下拉選單和切換音樂按鈕的框架
        music_frame = tk.Frame(self)
        music_frame.pack(pady=10)

        # 音樂檔案選擇下拉選單
        self.music_files = self.load_music_files()  # 讀取音樂檔案
        self.selected_music = tk.StringVar(self)
        self.selected_music.set(self.music_files[0] if self.music_files else "")  # 預設為第一首

        # 顯示提示標籤 (顯示是否有權限)
        self.permission_label = tk.Label(self, text="", font=("Arial", 12))
        self.permission_label.pack(pady=10)

        # 如果有權限顯示音樂選擇和切換音樂按鈕
        if self.has_permission:
            music_dropdown = tk.OptionMenu(music_frame, self.selected_music, *self.music_files)
            music_dropdown.pack(side=tk.LEFT, padx=10)

            # 更換音樂按鈕，放置於右邊
            self.change_music_button = tk.Button(
                music_frame, text="切換音樂", font=("Arial", 14), command=self.change_music
            )
            self.change_music_button.pack(side=tk.LEFT)
        else:
            # 如果沒有權限，只顯示提示
            self.permission_label.config(text="付費以解鎖更換背景音樂", fg="red")

        # 音量狀態顯示
        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

        # 確定按鈕
        tk.Button(self, text="退出介面", font=("Arial", 14), command=self.close_window).pack(pady=10)

    def load_music_files(self):
        """加載/music資料夾中的所有.mp3檔案"""
        music_dir = "music"
        if not os.path.exists(music_dir):
            os.makedirs(music_dir)  # 如果資料夾不存在就建立
        return [f for f in os.listdir(music_dir) if f.endswith('.mp3')]

    def check_music_permission(self):
        """向伺服器發送請求，檢查是否可以更改音樂"""
        message = f"CAN_I_CHANGE_MUSIC:{self.parent.account}"
        self.parent.server_connection.sendall(message.encode('utf-8'))
        response = self.parent.server_connection.recv(1024).decode('utf-8')

        # 根據伺服器回應決定是否有權限
        if response == "MUSIC_CHANGE_OK":
            self.has_permission = True
        else:
            self.has_permission = False

    def change_music(self):
        """切換背景音樂"""
        selected_music = self.selected_music.get()
        if not selected_music:
            return  # 如果沒有選擇音樂，則什麼都不做

        
        pygame.mixer.music.load(f"music/{selected_music}")
        pygame.mixer.music.play(loops=-1, start=0.0)
        self.status_label.config(text=f"背景音樂已更換為: {selected_music}", fg="green")
        

    def update_volume(self, val):
        """即時更新音量數值"""
        volume = int(val) / 100  # 將滑桿值轉換到 0~1 範圍
        self.parent.music_value = volume  # 更新父視窗的音量變數
        pygame.mixer.music.set_volume(volume)  # 更新音樂音量
        print(f"音量設定為: {volume}")

    def toggle_mute(self):
        """切換靜音狀態"""
        if self.parent.music_value == 0:
            # 從靜音恢復至原音量
            self.parent.music_value = self.previous_volume
            self.volume_slider.set(self.previous_volume * 100)  # 恢復滑桿值
            pygame.mixer.music.set_volume(self.previous_volume)
            self.mute_button.config(text="🔊", bg="Green", fg="white")
        else:
            # 記錄目前音量並靜音
            self.previous_volume = self.parent.music_value
            self.parent.music_value = 0
            self.volume_slider.set(0)  # 靜音時滑桿設為0
            pygame.mixer.music.set_volume(0)
            self.mute_button.config(text="🔈", bg="Red", fg="white")
        print(f"音量設定為: {self.parent.music_value}")

    def close_window(self):
        """關閉子視窗"""
        self.destroy()

class ShopSettingWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent.GUI)
        self.parent = parent
        self.title('瘋狂象棋 (商店)')
        self.geometry(f"{450}x{380}")
        self.resizable(False, False)  # 鎖定視窗大小
        self.create_widgets()

    def create_widgets(self):
        """建立子視窗內的商店元件"""

        # 左上角顯示優惠券與儲值按鈕
        top_frame = tk.Frame(self)
        top_frame.pack(anchor="nw", padx=10, pady=10)
        self.coupons_label = tk.Label(top_frame, text="我的優惠券: 未知", font=("Arial", 12), bg="gold")
        self.coupons_label.pack(side="left", padx=5)
        # 儲值按鈕，當按下時創建一個新的儲值子視窗
        tk.Button(top_frame, text="儲值", font=("Arial", 10), command=self.open_recharge_window).pack(side="left", padx=5)

        # 中間區域
        content_frame = tk.Frame(self)
        content_frame.pack(expand=True)

        # 音樂切換狀態
        self.music_label = tk.Label(content_frame, text="音樂切換: 未知", font=("Arial", 12))
        self.music_label.grid(row=0, column=0, pady=10)
        self.music_button = tk.Button(content_frame, text="購買", font=("Arial", 10), command=lambda: self.confirm_purchase('音樂頻道', 799))
        self.music_button.grid(row=0, column=1, pady=10)

        # VIP 狀態
        self.vip_status_label = tk.Label(content_frame, text="VIP 狀態: 未知", font=("Arial", 12))
        self.vip_status_label.grid(row=1, column=0, pady=10)
        self.vip_button = tk.Button(content_frame, text="購買", font=("Arial", 10), command=lambda: self.confirm_purchase('VIP', 3999))
        self.vip_button.grid(row=1, column=1, pady=10)

        # 排名點數
        self.rank_points_label = tk.Label(content_frame, text="排名點數: 未知", font=("Arial", 12))
        self.rank_points_label.grid(row=2, column=0, pady=10)
        self.rank_button = tk.Button(content_frame, text="購買", font=("Arial", 10), command=lambda: self.confirm_purchase('排名點數', 100))
        self.rank_button.grid(row=2, column=1, pady=10)

        # 確定按鈕
        tk.Button(self, text="退出介面", font=("Arial", 14), command=self.close_window).pack(pady=10)

        # 從伺服器獲取資訊 (使用線程)
        threading.Thread(target=self.load_shop_info, daemon=True).start()

    def confirm_purchase(self, item, price):
        """顯示確認購買的彈窗"""
        confirmation_window = tk.Toplevel(self)
        confirmation_window.title(f"確認購買 {item}")
        confirmation_window.geometry("300x150")
        confirmation_window.resizable(False, False)

        message = f"是否確認購買{item} ({price}元)?"
        label = tk.Label(confirmation_window, text=message, font=("Arial", 12))
        label.pack(pady=20)

        def proceed_purchase():
            """處理購買流程"""
            confirmation_window.destroy()
            
            try:
                # 根據不同的購買項目，發送不同的伺服器請求
                if item == '排名點數':
                    message = f"buy_rank:{self.parent.account}"
                elif item == 'VIP':
                    message = f"buy_vip:{self.parent.account}"
                elif item == '音樂頻道':
                    message = f"buy_music_channel:{self.parent.account}"
                else:
                    print(f"未知的購買項目: {item}")
                    return
            
                # 發送購買請求
                self.parent.server_connection.sendall(message.encode('utf-8'))
                
                # 接收伺服器回覆
                response = self.parent.server_connection.recv(1024).decode('utf-8')
                
                # 顯示購買結果
                if response[0] == "+":
                    self.show_purchase_result(f"{item}購買成功", "green")
                else:
                    self.show_purchase_result(f"{item}購買失敗: {response}", "red")
            
            except Exception as e:
                self.show_purchase_result(f"購買失敗: {e}", "red")

        def cancel_purchase():
            """取消購買"""
            confirmation_window.destroy()

        proceed_button = tk.Button(confirmation_window, text="確認", command=proceed_purchase)
        proceed_button.pack(side="left", padx=20, pady=10)
        cancel_button = tk.Button(confirmation_window, text="取消", command=cancel_purchase)
        cancel_button.pack(side="right", padx=20, pady=10)

    def show_purchase_result(self, message, color):
        """顯示購買結果的彈窗"""
        result_window = tk.Toplevel(self)
        result_window.title("購買結果")
        result_window.geometry("300x150")
        result_window.resizable(False, False)

        # 顯示回應訊息
        result_label = tk.Label(result_window, text=message, font=("Arial", 12), fg=color)
        result_label.pack(pady=30)

        # 確定按鈕，點擊後關閉彈窗並重新載入商店資訊
        close_button = tk.Button(result_window, text="確定", command=lambda: [result_window.destroy(), threading.Thread(target=self.load_shop_info, daemon=True).start()])
        close_button.pack()

    def open_recharge_window(self):
        """創建儲值子視窗"""
        recharge_window = tk.Toplevel(self)
        recharge_window.title("儲值")
        recharge_window.geometry("300x150")
        recharge_window.resizable(False, False)

        # 輸入框與送出按鈕
        tk.Label(recharge_window, text="請輸入儲值碼:").pack(pady=10)
        amount_entry = tk.Entry(recharge_window)
        amount_entry.pack(pady=5)

        def submit_recharge():
            """提交儲值金額"""
            redeem_code = amount_entry.get()
            if redeem_code:
                # 發送儲值請求給伺服器
                try:
                    message = f"redeem_code_trade:{self.parent.account}:{redeem_code}"
                    self.parent.server_connection.sendall(message.encode('utf-8'))
                    
                    # 接收伺服器回覆
                    response = self.parent.server_connection.recv(1024).decode('utf-8')
                    
                    # 根據回覆處理
                    if response == "REDEEM_OK":
                        self.show_recharge_result("儲值成功！", "green")
                        recharge_window.destroy()  # 關閉儲值視窗
                    elif response == "REDEEM_FAILED":
                        self.show_recharge_result("儲值失敗，請檢查儲值碼", "red")
                    else:
                        self.show_recharge_result(response, "green" if "成功" in response else "red")
                except Exception as e:
                    self.show_recharge_result(f"伺服器連接錯誤: {e}", "red")
            else:
                self.show_recharge_result("請輸入有效的儲值碼", "red")

        submit_button = tk.Button(recharge_window, text="送出", command=submit_recharge)
        submit_button.pack(pady=10)

    def show_recharge_result(self, message, color):
        """顯示儲值結果的彈窗"""
        result_window = tk.Toplevel(self)
        result_window.title("儲值結果")
        result_window.geometry("300x150")
        result_window.resizable(False, False)

        # 顯示回應訊息
        result_label = tk.Label(result_window, text=message, font=("Arial", 12), fg=color)
        result_label.pack(pady=30)

        # 確定按鈕，點擊後關閉彈窗
        close_button = tk.Button(result_window, text="確定", command=result_window.destroy)
        close_button.pack()

    def load_shop_info(self):
        """從伺服器加載 VIP 狀態、排名點數和優惠券資訊"""
        try:
            if not self.parent.account:
                raise ValueError("帳戶資訊缺失")

            # 音樂切換狀態
            self.parent.server_connection.sendall(f"CAN_I_CHANGE_MUSIC:{self.parent.account}".encode('utf-8'))
            response = self.parent.server_connection.recv(1024).decode('utf-8')
            is_music_enabled = response == "MUSIC_CHANGE_OK"
            self.update_label(self.music_label, 
                              text="音樂切換 : 啟用" if is_music_enabled else "音樂切換 : 未啟用", 
                              fg="green" if is_music_enabled else "red")
            if is_music_enabled:
                self.music_button.grid_forget()  # 音樂切換啟用時移除按鈕

            # VIP 狀態
            self.parent.server_connection.sendall(f"am_i_vip:{self.parent.account}".encode('utf-8'))
            vip_response = self.parent.server_connection.recv(1024).decode('utf-8')
            is_vip = vip_response == "UR_VIP"
            self.update_label(self.vip_status_label, 
                              text="VIP 狀態: 是" if is_vip else "VIP 狀態: 否", 
                              fg="green" if is_vip else "red")
            if is_vip:
                self.vip_button.grid_forget()  # VIP 為 "是" 時移除按鈕

            # 排名點數
            self.parent.server_connection.sendall(f"my_rank_point:{self.parent.account}".encode('utf-8'))
            rank_points = self.parent.server_connection.recv(1024).decode('utf-8')
            self.update_label(self.rank_points_label, text=f"排名點數: {rank_points}")

            # 優惠券資訊
            self.parent.server_connection.sendall(f"coupons_i_have:{self.parent.account}".encode('utf-8'))
            coupons = self.parent.server_connection.recv(1024).decode('utf-8')
            self.update_label(self.coupons_label, text=f"我的優惠券: {coupons}")

        except ValueError as ve:
            self.update_label(self.vip_status_label, text=f"錯誤: {ve}", fg="red")
            self.update_label(self.rank_points_label, text="排名點數: 無法加載")
            self.update_label(self.coupons_label, text="我的優惠券: 無法加載")
        except Exception as e:
            print(f"伺服器連接錯誤: {e}")
            self.update_label(self.vip_status_label, text="VIP 狀態: 加載失敗", fg="red")
            self.update_label(self.rank_points_label, text="排名點數: 加載失敗")
            self.update_label(self.coupons_label, text="我的優惠券: 加載失敗")

    def update_label(self, label, **kwargs):
        """安全地更新 Tkinter Label 的內容"""
        if self.winfo_exists():  # 確認視窗仍然存在
            self.after(0, lambda: label.config(**kwargs))  # 主線程更新 GUI

    def close_window(self):
        """關閉子視窗"""
        self.destroy()

class LeaderboardWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent.GUI)
        self.parent = parent
        self.title('排行榜')
        self.geometry(f"{450}x{380}")
        self.resizable(False, False)  # 鎖定視窗大小
        self.create_widgets()
        self.fetch_rankings()

    def create_widgets(self):
        """建立排行榜介面元件"""
        tk.Label(self, text="排行榜", font=("Arial", 16)).pack(pady=20)

        # 排行榜顯示區域
        self.rank_display = tk.Label(self, text="載入中...", font=("Arial", 12))
        self.rank_display.pack(pady=10)

        # 確定按鈕
        tk.Button(self, text="關閉視窗", font=("Arial", 14), command=self.close_window).pack(pady=10)

    def fetch_rankings(self):
        """向伺服器請求排行榜資料"""
        message = "get_rank_now"  # 發送請求
        self.parent.server_connection.sendall(message.encode('utf-8'))
        
        # 接收伺服器回應
        response = self.parent.server_connection.recv(1024).decode('utf-8')
        
        # 顯示排行榜資料
        self.display_rankings(response)

    def display_rankings(self, data):
        """顯示排行榜資料"""
        try:
            if ( data == "-empty" ):  # 如果回傳的資料是空的
                self.rank_display.config(text="排行統計中...", fg="orange")
                return

            # 假設資料是以字串形式傳來，並轉換成列表格式
            rank_data = eval(data)  # 這會把伺服器返回的字串轉換為 Python 資料結構 (例如：列表)
            
            # 加入emoji並格式化前三名
            formatted_rank = ""
            for i in range(len(rank_data)):
                if i == 0:
                    formatted_rank += f"🥇 {rank_data[i]}\n"
                elif i == 1:
                    formatted_rank += f"🥈 {rank_data[i]}\n"
                elif i == 2:
                    formatted_rank += f"🥉 {rank_data[i]}\n"
                else:
                    formatted_rank += f"{i+1}. {rank_data[i]}\n"

            # 更新排行榜顯示
            self.rank_display.config(text=formatted_rank, fg="black")

        except Exception as e:
            self.rank_display.config(text="無法載入排行榜", fg="red")
            print(f"Error: {e}")

    def close_window(self):
        """關閉子視窗"""
        self.destroy()