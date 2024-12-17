import os
import json
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, '_data_a.json')

def main():
    
    if ( len(sys.argv) < 3):
        print("創建帳號失敗 格式 addadmin account password")
        exit()

    account = sys.argv[1]
    password = sys.argv[2]

    new_admin_data = {
        'account': account,
        'password': password
    }

    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump({}, file)

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if data:
        next_id = str(int(max(data.keys()))+1)
    else:
        next_id = '1'

    new_admin_data['id'] = next_id
    data[next_id] = new_admin_data

    with open(filename,'w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False,indent=4)

if __name__ == '__main__':
	main()