import json
import os
import Sys_add_account as aac
#==============Define===============
current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, '_data_u.json')
blst = {'.','/'}

def login(account,passwd):
    
    if not os.path.exists(filename):
        aac.ctreat_file()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for finder in data.values():
        if ( finder['account'] == account ):
            if (finder['password'] == passwd):
                return 1
        
    return 0   

def onlinecheck(account):
    if not os.path.exists(filename):
        aac.ctreat_file()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for finder in data.values():
        if ( finder['account'] == account ):
            if (finder['online'] == 1):
                return 1
        
    return 0

def changeonline(account):
    if not os.path.exists(filename):
        aac.ctreat_file()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for key, value in data.items():
        if value["account"] == account:
            value["online"] = (value["online"] + 1) % 2
            print(f"Account {account} online status updated to {value['online']}")
            break
    else:
        print(f"Account {account} not found.")
        return 0
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    
#print(addaccount('aa','bb'))
#login('aa','bb')
#changeonline('aa')