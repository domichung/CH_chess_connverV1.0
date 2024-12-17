import logic.red

def r_move_main(chess,x,y,zone,newx,newy):
    if (chess == "兵"):
        accept_move = logic.red.r_soldier(y,x,zone)      
    elif (chess == "俥"):
        accept_move = logic.red.r_car(y,x,zone)
    elif (chess == "傌"):
        accept_move = logic.red.r_horse(y,x,zone)
    elif (chess == "炮"):
        accept_move = logic.red.r_artillery(y,x,zone)
    elif (chess == "仕"):
         accept_move = logic.red.r_sergeant(y,x,zone)
    elif (chess == "相"):
         accept_move = logic.red.r_elephant(y,x,zone)
    elif (chess == "帥"):
         accept_move = logic.red.r_king(y,x,zone)
    else:
        return 'err'
    
    for i in range(0, len(accept_move), 2):
        print(accept_move[i],accept_move[i+1],'wwwww',newx,newy)
        if (int(newy) == int(accept_move[i]) and int(newx) == int(accept_move[i+1])):
            return 'success'
    
    return 'faild'