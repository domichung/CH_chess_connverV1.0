import json
import os
import Sys_add_account as aac

current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, '_data_u.json')
blst = {'.','/'}

def can_i_change_music(account):
    if not os.path.exists(filename):
        aac.ctreat_file()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for finder in data.values():
        if ( finder['account'] == account ):
            return finder['music_ch']
        
    return 'error'

def coupons_i_have(account):
    if not os.path.exists(filename):
        aac.ctreat_file()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for finder in data.values():
        if ( finder['account'] == account ):
            return finder['coupons']
        
    return 'error'

def am_i_vip(account):
    if not os.path.exists(filename):
        aac.ctreat_file()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for finder in data.values():
        if ( finder['account'] == account ):
            return finder['vip']
        
    return 'error'


def my_rank_point(account):
    if not os.path.exists(filename):
        aac.ctreat_file()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for finder in data.values():
        if ( finder['account'] == account ):
            return finder['rank_point']
        
    return 'error'

def get_top_10_ranked_players():
    
    if not os.path.exists(filename):
        aac.create_file()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    ranked_players = [
        finder for finder in data.values() if finder['rank_point'] >= 50
    ]
    
    if not ranked_players:
        return "-empty"
    
    ranked_players.sort(key=lambda x: x['rank_point'], reverse=True)
    
    top_10_accounts = [finder['account'] for finder in ranked_players[:10]]

    return top_10_accounts

#print(get_top_10_ranked_players())
