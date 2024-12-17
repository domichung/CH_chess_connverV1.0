import json
import os
import Sys_add_account as aac

current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, '_data_u.json')
blst = {'.','/'}

def addmoney(account,point):
    if not os.path.exists(filename):
        aac.ctreat_file()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for key, value in data.items():
        if value["account"] == account:
            value["coupons"] = (value["coupons"] + point )
            break
    else:
        print(f"Account {account} not found.")
        return 0
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        

def check_account_money(account,needmoney):
    if not os.path.exists(filename):
        aac.ctreat_file()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for key, value in data.items():
        if value["account"] == account:
            money = value["coupons"] 
            break
    
    if (int(money)>=int(needmoney)):
        return True
    else:
        return False

def Buy_music_channel(account):
    cost = 799  # Cost for the music channel
    if not check_account_money(account, cost):
        return f"你的餘額不足"
    
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for key, value in data.items():
        if value["account"] == account:
            if value["music_ch"] == 1:
                return f"你早就有音樂頻道了"
            value["music_ch"] = 1  # Activate music channel
            value["coupons"] -= cost  # Deduct cost for music channel
            break
    else:
        return f"未知帳戶"
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    return f"+帳號 {account} 成功購買音樂頻道"


def Buy_VIP(account):
    cost = 3999  # Cost for VIP access
    if not check_account_money(account, cost):
        return f"你的餘額不足"
    
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for key, value in data.items():
        if value["account"] == account:
            if value["vip"] == 1:
                return f"你早就有VIP了"
            value["vip"] = 1  # Activate VIP access
            value["coupons"] -= cost  # Deduct cost for VIP access
            break
    else:
        return f"未知帳戶"
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    return f"+帳號 {account} 成功購買VIP"


def Buy_RANK(account):
    cost = 100  # Cost for rank point
    if not check_account_money(account, cost):
        return f"你的餘額不足"
    
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for key, value in data.items():
        if value["account"] == account:
            value["rank_point"] += 10  # Increase rank point by 1
            value["coupons"] -= cost  # Deduct cost for rank point
            break
    else:
        return f"未知帳戶"
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    return f"+帳戶 {account}成功購買牌位積分"