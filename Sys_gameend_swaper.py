import os
import json
import time

# 設定資料夾路徑
folder_path = "game_room"

# 持續掃描資料夾中的 JSON 檔案
while True:
    # 取得資料夾內所有檔案名稱
    files = [filename for filename in os.listdir(folder_path) if filename.endswith(".json")]
    
    # 遍歷所有檔案
    for filename in files:
        file_path = os.path.join(folder_path, filename)

        # 讀取 JSON 檔案
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        # 檢查是否需要跳過這個檔案
        if data["gamestatus"] in ["end", "waiting"]:
            continue
        
        # 檢查棋盤中是否有「將」和「帥」
        red_player1_found = False
        black_player2_found = False

        for row in data["board"]:
            if "帥" in row:
                black_player2_found = True
            if "將" in row:
                red_player1_found = True

        # 根據棋盤狀況更新檔案
        if not red_player1_found:
            data["now_move"] = data["red_player1"]
            data["gamestatus"] = "end"
        elif not black_player2_found:
            data["now_move"] = data["black_player2"]
            data["gamestatus"] = "end"
        
        # 將修改後的資料寫回檔案
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        print(f"{filename} 已更新。")
    
    # 等待一段時間再從頭開始掃描
    print('swaper2 alive')
    time.sleep(2)  # 每 5 秒檢查一次資料夾
