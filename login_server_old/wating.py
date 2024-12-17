import tkinter as tk
import math

class LoadingSpinner:
    def __init__(self):
        # 初始化主視窗
        self.root = tk.Tk()
        self.root.title("轉圈圈介面")
        self.root.geometry("300x300")

        # 建立 Canvas
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="white")
        self.canvas.pack()

        # 初始參數
        self.angle = 0  # 旋轉的角度
        self.arc = None  # 圓弧對象
        self.radius = 50  # 圓的半徑
        self.center_x = 150  # 圓心 x
        self.center_y = 150  # 圓心 y

        # 啟動動畫
        self.start_animation()

    def draw_spinner(self):
        # 刪除之前的圓弧
        if self.arc:
            self.canvas.delete(self.arc)

        # 計算圓弧位置和角度
        start_angle = self.angle
        extent_angle = 120  # 圓弧的角度範圍
        x0 = self.center_x - self.radius
        y0 = self.center_y - self.radius
        x1 = self.center_x + self.radius
        y1 = self.center_y + self.radius

        # 繪製圓弧
        self.arc = self.canvas.create_arc(
            x0, y0, x1, y1, start=start_angle, extent=extent_angle, style=tk.ARC, outline="blue", width=5
        )

    def update_spinner(self):
        # 更新旋轉角度
        self.angle = (self.angle + 10) % 360  # 每次增加 10 度，360 度後重置
        self.draw_spinner()  # 重繪轉圈圈
        self.root.after(50, self.update_spinner)  # 每隔 50 毫秒更新動畫

    def start_animation(self):
        self.update_spinner()  # 開始更新動畫
        self.root.mainloop()  # 啟動主事件迴圈

# 創建並啟動轉圈圈介面
LoadingSpinner()
