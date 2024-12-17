import json
import os

def createroom(user, mode):
    # Define the board layout
    board = [
        ['車', '馬', '象', '士', '將', '士', '象', '馬', '車'],
        ['空', '空', '空', '空', '空', '空', '空', '空', '空'],
        ['空', '砲', '空', '空', '空', '空', '空', '砲', '空'],
        ['卒', '空', '卒', '空', '卒', '空', '卒', '空', '卒'],
        ['空', '空', '空', '空', '空', '空', '空', '空', '空'],
        ['空', '空', '空', '空', '空', '空', '空', '空', '空'],
        ['兵', '空', '兵', '空', '兵', '空', '兵', '空', '兵'],
        ['空', '炮', '空', '空', '空', '空', '空', '炮', '空'],
        ['空', '空', '空', '空', '空', '空', '空', '空', '空'],
        ['俥', '傌', '相', '仕', '帥', '仕', '相', '傌', '俥']
    ]
    
    # Define the room information, including the 'now_move' field
    room_info = {
        'board': board,
        'red_player1': user,
        'black_player2': 'empty',
        'gamestatus': 'waiting',
        'gamemode': mode,
        'now_move': user  # Set the first player to move
    }

    # Ensure the directory exists
    os.makedirs('./game_room', exist_ok=True)

    # Find the highest existing room number
    existing_files = os.listdir('./game_room')
    max_room_number = 0
    for file in existing_files:
        if file.startswith('r') and file.endswith('.json'):
            try:
                room_number = int(file[1:5])
                max_room_number = max(max_room_number, room_number)
            except ValueError:
                pass  # Ignore files that don't match the naming convention

    # Increment the room number to the next available one
    room_number = max_room_number + 1

    # Define the file name for the new room
    room_filename = f'./game_room/r{room_number:04}.json'

    # Write the room information to the file
    with open(room_filename, 'w', encoding='utf-8') as f:
        json.dump(room_info, f, ensure_ascii=False, indent=4)

    return f'{room_number:04}'


def joinroom(roomid, user):
    room_filename = f'./game_room/{roomid}.json'

    # Check if the room file exists
    if not os.path.exists(room_filename):
        return f"Room {roomid} does not exist."
    
    # Read the existing room data
    with open(room_filename, 'r', encoding='utf-8') as f:
        room_info = json.load(f)
    
    # Check if player2 is already occupied
    if room_info['black_player2'] != 'empty':
        return f"Roomfull"
    
    # Add the player to player2
    room_info['black_player2'] = user
    room_info['gamestatus'] = 'playing'  # Change game status to playing

    # Write the updated room data back to the file
    with open(room_filename, 'w', encoding='utf-8') as f:
        json.dump(room_info, f, ensure_ascii=False, indent=4)
    
    return f"success"


def can_i_create(playerid):
    # Get the list of existing room files
    existing_files = os.listdir('./game_room')

    # Check each file for game status and player presence
    for file in existing_files:
        if file.startswith('r') and file.endswith('.json'):
            try:
                # Open the room JSON file and load its content
                with open(f'./game_room/{file}', 'r', encoding='utf-8') as f:
                    room_info = json.load(f)

                # Check if the game is waiting or playing, and if the player is already in the room
                if room_info['gamestatus'] in ['waiting', 'playing']:
                    if room_info['red_player1'] == playerid or room_info['black_player2'] == playerid:
                        # Player is already in a game, return False
                        return False
            except (json.JSONDecodeError, IOError):
                pass  # Ignore errors while reading files

    return True

def get_room_status(room_number):
    # 確保房間號是 4 位數格式
    room_filename = f'./game_room/r{int(room_number):04}.json'

    if not os.path.exists(room_filename):
        return "Room not found"

    try:
        with open(room_filename, 'r', encoding='utf-8') as f:
            room_info = json.load(f)
            # 返回 `gamestatus` 欄位
            return room_info.get('gamestatus', "Status not found")
    except (json.JSONDecodeError, IOError):
        return "Error reading room file"
    
def get_who_win(room_number):
    room_filename = f'./game_room/r{int(room_number):04}.json'

    if not os.path.exists(room_filename):
        return "Room not found"

    try:
        with open(room_filename, 'r', encoding='utf-8') as f:
            room_info = json.load(f)
            return room_info.get('now_move', "Status not found")
    except (json.JSONDecodeError, IOError):
        return "Error reading room file"

#createroom('aa', 'classic')
#joinroom('r0001', 'w')
#print(can_i_create('w'))
#print(joinroom('r0004','w'))
#print(get_room_status('0002'))