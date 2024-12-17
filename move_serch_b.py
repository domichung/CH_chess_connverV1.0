import logic.black

def b_move_main(chess,x,y,zone,newx,newy):
    if (chess == "卒"):
        accept_move = logic.black.b_soldier(y,x,zone)      
    elif (chess == "車"):
        accept_move = logic.black.b_car(y,x,zone)
    elif (chess == "馬"):
        accept_move = logic.black.b_horse(y,x,zone)
    elif (chess == "砲"):
        accept_move = logic.black.b_artillery(y,x,zone)
    elif (chess == "士"):
         accept_move = logic.black.b_sergeant(y,x,zone)
    elif (chess == "象"):
         accept_move = logic.black.b_elephant(y,x,zone)
    elif (chess == "將"):
         accept_move = logic.black.b_king(y,x,zone)
    else:
        return 'err'
    
    for i in range(0, len(accept_move), 2):
        print(accept_move[i],accept_move[i+1],'wwwww',newx,newy)
        if (int(newy) == int(accept_move[i]) and int(newx) == int(accept_move[i+1])):
            return 'success'
    
    return 'faild'
    