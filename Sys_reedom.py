import json
import random
import string

# 定義 JSON 文件名稱
FILE_NAME = "redeem_codes.json"

# 初始化 JSON 文件
def initialize_json():
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(FILE_NAME, "w") as file:
            json.dump({}, file)

# 第一個函式: 生成隨機兌換碼並寫入 JSON 文件
def generate_redeem_code(amount):
    redeem_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
        data[redeem_code] = amount
        with open(FILE_NAME, "w") as file:
            json.dump(data, file)
    except Exception as e:
        return f"Error: {e}"
    return redeem_code

# 第二個函式: 驗證並刪除兌換碼
def redeem_code_input(code):
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
        if code in data:
            amount = data.pop(code)
            with open(FILE_NAME, "w") as file:
                json.dump(data, file)
            return amount
        else:
            return None
    except Exception as e:
        return f"Error: {e}"

# 測試功能
#if __name__ == "__main__":
#    initialize_json()

    # 生成兌換碼
#    input_amount = int(input("輸入金額: "))
#    code = generate_redeem_code(input_amount)
#    print(f"生成的兌換碼: {code}")
#
#    # 輸入兌換碼
#    input_code = input("輸入兌換碼: ")
#    result = redeem_code_input(input_code)
#    if result is None:
#        print("兌換碼不存在或已被使用！")
#    else:
#        print(f"兌換成功！金額為: {result}")