import json
import os

def get_board_as_2d_array(roomid):
    # Path to the room file
    room_filename = f'./game_room/{roomid}.json'
    
    # Check if the room file exists
    if not os.path.exists(room_filename):
        return f"Room {roomid} does not exist."
    
    # Load the room data
    with open(room_filename, 'r', encoding='utf-8') as f:
        room_info = json.load(f)
    
    # Check if the 'board' key exists in the room data
    if 'board' not in room_info:
        return f"No board data found for room {roomid}."
    
    # Return the board as a 2D array
    return room_info['board']

#================================================================

def get_gamestatus(roomid):
    # Path to the room file
    room_filename = f'./game_room/{roomid}.json'
    
    # Check if the room file exists
    if not os.path.exists(room_filename):
        return f"not_exist"
    
    with open(room_filename, 'r', encoding='utf-8') as f:
        room_info = json.load(f)

    if 'gamestatus' not in room_info:
        return f"error {roomid}."
    
    return room_info['gamestatus']


#================================================================

def get_nowmove(roomid):
    # Path to the room file
    room_filename = f'./game_room/{roomid}.json'
    
    # Check if the room file exists
    if not os.path.exists(room_filename):
        return f"not_exist"
    
    with open(room_filename, 'r', encoding='utf-8') as f:
        room_info = json.load(f)

    if 'now_move' not in room_info:
        return f"error {roomid}."
    
    return room_info['now_move']

#================================================================
def get_nowteam(roomid):
    # Path to the room file
    room_filename = f'./game_room/{roomid}.json'
    
    # Check if the room file exists
    if not os.path.exists(room_filename):
        return f"not_exist"
    
    with open(room_filename, 'r', encoding='utf-8') as f:
        room_info = json.load(f)

    if 'now_move' not in room_info:
        return f"error {roomid}."
    
    if (room_info['now_move'] == room_info['red_player1']):
        return 'red'
    elif (room_info['now_move'] == room_info['black_player2']):
        return 'black'
    else:
        return 'null'
    
#print(get_nowteam('r0001'))


# Example usage:
#room_status = get_gamestatus('r0001')
#print(room_status)

#================================================================
# Example usage:
#print( get_board_as_2d_array('r0001')[9][8])

#if isinstance(room_board, list):  # Check if we got a valid board
#    for row in room_board:
#        print(" ".join(row))  # Print the 2D board as a readable format
#        #print(room_board)
#else:
#    print(room_board)


def move_piece_and_save(roomid, x1, y1, x2, y2):
    # Path to the room file
    room_filename = f'./game_room/{roomid}.json'
    
    # Check if the room file exists
    if not os.path.exists(room_filename):
        return f"Room {roomid} does not exist."
    
    # Load the room data
    with open(room_filename, 'r', encoding='utf-8') as f:
        room_info = json.load(f)
    
    # Check if the 'board' key exists in the room data
    if 'board' not in room_info:
        return f"No board data found for room {roomid}."
    
    # Get the board data
    board = room_info['board']
    
    # Validate coordinates
    if not (0 <= x1 < len(board) and 0 <= y1 < len(board[0]) and
            0 <= x2 < len(board) and 0 <= y2 < len(board[0])):
        return "Invalid coordinates."
    
    # Move the piece
    piece = board[x1][y1]  # Get the piece at (x1, y1)
    board[x1][y1] = "空"   # Replace (x1, y1) with "空"
    board[x2][y2] = piece  # Place the piece at (x2, y2)
    
    # Switch the 'now_move' field
    if room_info['now_move'] == room_info['red_player1']:
        room_info['now_move'] = room_info['black_player2']
    else:
        room_info['now_move'] = room_info['red_player1']
    
    # Update the room data
    room_info['board'] = board
    
    # Save the updated room data back to the JSON file
    with open(room_filename, 'w', encoding='utf-8') as f:
        json.dump(room_info, f, ensure_ascii=False, indent=4)
    
    #return f"Moved piece from ({x1}, {y1}) to ({x2}, {y2}) successfully, and replaced the original position with '空'. Now it's {room_info['now_move']}'s turn."
    return 'success'

#print(move_piece_and_save('r0001',0,4,0,5))#y,x