import json
import os
import time

def game_swaper(interval=10):
    while True:
        # Path to the player data file
        user_data_file = './_data_u.json'
        # Check if the user data file exists
        if not os.path.exists(user_data_file):
            print("User data file not found.")
            return

        # Load user data from _data_u.json
        with open(user_data_file, 'r', encoding='utf-8') as f:
            user_data = json.load(f)

        # Path to the game room directory
        room_dir = './game_room'
        # Check if the game room directory exists
        if not os.path.exists(room_dir):
            print("Game room directory not found.")
            return

        # Iterate over all room files in the directory
        for file in os.listdir(room_dir):
            if file.endswith('.json'):
                room_path = os.path.join(room_dir, file)
                # Load room data
                with open(room_path, 'r', encoding='utf-8') as f:
                    room_info = json.load(f)

                # Check if the game status is 'playing'
                if room_info.get('gamestatus') == 'playing':
                    # Extract players from the room
                    player1 = room_info.get('red_player1')
                    player2 = room_info.get('black_player2')

                    # Check online status for player1 and player2
                    player1_online = any(user.get('account') == player1 and user.get('online') == 1 for user in user_data.values())
                    player2_online = any(user.get('account') == player2 and user.get('online') == 1 for user in user_data.values())

                    # If either player is offline, end the game
                    if not player1_online or not player2_online:
                        room_info['gamestatus'] = 'end'
                        if not player1_online:
                            room_info['now_move'] = player2
                        elif not player2_online:
                            room_info['now_move'] = player1
                        with open(room_path, 'w', encoding='utf-8') as f:
                            json.dump(room_info, f, ensure_ascii=False, indent=4)
                        print(f"Game in room {file} has ended due to inactive player.")
                    
                    # Check if the king pieces are missing (將 or 帥)
                    red_king_found = False
                    black_king_found = False
                    board = room_info.get('board', [])

                    # Scan the board for the pieces "將" (red king) and "帥" (black king)
                    for row in board:
                        if "將" in row:
                            red_king_found = True
                        if "帥" in row:
                            black_king_found = True

                    # If the red king (將) is missing, end the game and set the turn to black_player2
                    if not red_king_found:
                        room_info['gamestatus'] = 'end'
                        room_info['now_move'] = player2  # Black wins
                        with open(room_path, 'w', encoding='utf-8') as f:
                            json.dump(room_info, f, ensure_ascii=False, indent=4)
                        print(f"Game in room {file} has ended because red's king (將) is missing.")

                    # If the black king (帥) is missing, end the game and set the turn to red_player1
                    elif not black_king_found:
                        room_info['gamestatus'] = 'end'
                        room_info['now_move'] = player1  # Red wins
                        with open(room_path, 'w', encoding='utf-8') as f:
                            json.dump(room_info, f, ensure_ascii=False, indent=4)
                        print(f"Game in room {file} has ended because black's king (帥) is missing.")

                elif room_info.get('gamestatus') == 'waiting':
                    player1 = room_info.get('red_player1')
                    player1_online = any(user.get('account') == player1 and user.get('online') == 1 for user in user_data.values())
                    if not player1_online:
                        room_info['gamestatus'] = 'end'
                        # Save updated room data back to the file
                        with open(room_path, 'w', encoding='utf-8') as f:
                            json.dump(room_info, f, ensure_ascii=False, indent=4)
                        print(f"Game in room {file} has ended due to inactive player.")
                        
        # Wait for the specified interval before running again
        time.sleep(interval)
        print('swaper alive')



# Example usage:
game_swaper(interval=10)  # Scans every 10 seconds (you can stop it with Ctrl+C).
