import json
import os

#==============Define===============
current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, '_data_u.json')
blst = {'.','/'}

def ctreat_file():
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump({}, file)
        
    print("warning rebuild account file")


def check_account_exsist(account):
    
    if not os.path.exists(filename):
        ctreat_file()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for finder in data.values():
        if ( finder['account'] == account ):
            return 1
        
    return 0

def check_mail_exsist(mail):
    
    if not os.path.exists(filename):
        ctreat_file()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for finder in data.values():
        if ( finder['mail'] == mail ):
            return 1
        
    return 0

def new_account(new_data):
    
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if data:
        next_id = str(int(max(data.keys()))+1)
    else:
        next_id = '1'

    new_data['id'] = next_id
    data[next_id] = new_data

    with open(filename,'w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False,indent=4)


def addaccount(input_account,input_password,input_mail):
    
    new_user_data = {
        'account': input_account,
        'password': input_password,
        'mail': input_mail,
        'rank_point': 0,
        'music_ch': 0,
        'vip':0,
        "coupons": 0,
        'online':0
    }

    #print("w")
    
    if (check_account_exsist(input_account) ):
        return 'account_exsist'
    elif (check_mail_exsist(input_mail)):
        return 'mail_exsist'
    else:
        new_account(new_user_data)
        return 'success'
    
#print(addaccount('au','b','wwzzz@gmail.com'))