red_pieces = {'俥', '傌', '相', '仕', '帥', '炮', '兵'}
black_pieces = {'車', '馬', '象', '士', '將', '砲', '卒'}

def r_soldier(x,y,zone):
    
    x = int(x)
    y = int(y)
    
    boundary = []

    if ( y >= 5 ):
        if (zone[y-1][x] not in red_pieces):
            boundary += str(x)+str(y-1)
    else:
        if ( y-1 >= 0 ):
            if (zone[y-1][x] not in red_pieces):
                boundary+=str(x)+str(y-1)
        if ( x-1 >= 0 ):
            if (zone[y][x-1] not in red_pieces):
                boundary+=str(x-1)+str(y)
        if ( x+1 <= 8 ):
            if (zone[y][x+1] not in red_pieces):
                boundary+=str(x+1)+str(y)
        

    return boundary

def r_car(x,y,zone):
    
    x = int(x)
    y = int(y)

    boundary = []

    t_y = y
    
    while (t_y-1>=0):
        t_y-=1
        if (zone[t_y][x] in red_pieces):
            break
        boundary += str(int(x))+str(int(t_y))
        if (zone[t_y][x] in black_pieces):
            break
        #print(boundary)

    t_y = y

    while (t_y+1<=9):
        t_y+=1
        if (zone[t_y][x] in red_pieces):
            break
        boundary += str(int(x))+str(int(t_y))
        if (zone[t_y][x] in black_pieces):
            break

    t_x = x

    while (t_x-1>=0):
        t_x-=1
        if (zone[y][t_x] in red_pieces):
            break
        boundary += str(int(t_x))+str(int(y))
        if (zone[y][t_x] in black_pieces):
            break
    
    t_x = x

    while (t_x+1<=8):
        t_x+=1
        if (zone[y][t_x] in red_pieces):
            break
        boundary += str(int(t_x))+str(int(y))
        if (zone[y][t_x] in black_pieces):
            break
    
    #print(boundary)
    return boundary

def r_artillery(x,y,zone):

    x = int(x)
    y = int(y)

    boundary = []

    t_y = y
    eat_flag = 0

    while (t_y-1>=0):
        t_y-=1
        if (eat_flag==0):
            if ((zone[t_y][x] in red_pieces) or (zone[t_y][x] in black_pieces)):
                eat_flag = 1
                continue
            else:
                boundary += str(int(x))+str(int(t_y))
                continue
        if (zone[t_y][x] in red_pieces):
            break
        if (zone[t_y][x] in black_pieces):
            boundary += str(int(x))+str(int(t_y))
            break

    t_y = y      
    eat_flag = 0

    while (t_y+1<=9):
        t_y+=1
        if (eat_flag==0):
            if ((zone[t_y][x] in red_pieces) or (zone[t_y][x] in black_pieces)):
                eat_flag = 1
                continue
            else:
                boundary += str(int(x))+str(int(t_y))
                continue
        if (zone[t_y][x] in red_pieces):
            break
        if (zone[t_y][x] in black_pieces):
            boundary += str(int(x))+str(int(t_y))
            break
    
    t_x = x
    eat_flag = 0

    while (t_x-1>=0):
        t_x-=1
        if (eat_flag==0):
            if ((zone[y][t_x] in red_pieces) or (zone[y][t_x] in black_pieces)):
                eat_flag = 1
                continue
            else:
                boundary += str(int(t_x))+str(int(y))
                continue
        if (zone[y][t_x] in red_pieces):
            break
        if (zone[y][t_x] in black_pieces):
            boundary += str(int(t_x))+str(int(y))
            break
    
    t_x = x
    eat_flag = 0

    while (t_x+1<=8):
        t_x+=1
        if (eat_flag==0):
            if ((zone[y][t_x] in red_pieces) or (zone[y][t_x] in black_pieces)):
                eat_flag = 1
                continue
            else:
                boundary += str(int(t_x))+str(int(y))
                continue
        if (zone[y][t_x] in red_pieces):
            break
        if (zone[y][t_x] in black_pieces):
            boundary += str(int(t_x))+str(int(y))
            break

    #print(boundary)
    return boundary

def r_horse(x,y,zone):
    
    x = int(x)
    y = int(y)

    boundary = []

    #上左上右
    if ( x-1 >= 0 and y-2 >= 0 ):
        if (zone[y-2][x-1] not in red_pieces):
            if ( zone[y-1][x] not in red_pieces and zone[y-1][x] not in black_pieces):
                boundary+=str(x-1)+str(y-2)
    if ( x+1 <= 8 and y-2 >= 0 ):
        if (zone[y-2][x+1] not in red_pieces):
            if ( zone[y-1][x] not in red_pieces and zone[y-1][x] not in black_pieces):
                boundary+=str(x+1)+str(y-2)
    #左上左下
    if ( x-2 >= 0 and y-1 >= 0 ):
        if (zone[y-1][x-2] not in red_pieces):
            if ( zone[y][x-1] not in red_pieces and zone[y][x-1] not in black_pieces):
                boundary+=str(x-2)+str(y-1)
    if ( x-2 >= 0 and y+1 <= 9 ):
        if (zone[y+1][x-2] not in red_pieces):
            if ( zone[y][x-1] not in red_pieces and zone[y][x-1] not in black_pieces):
                boundary+=str(x-2)+str(y+1)
    #下左下右
    if ( x-1 >= 0 and y+2 <= 9 ):
        if (zone[y+2][x-1] not in red_pieces):
            if ( zone[y+1][x] not in red_pieces and zone[y+1][x] not in black_pieces):
                boundary+=str(x-1)+str(y+2)
    if ( x+1 <= 8 and y+2 <= 9 ):
        if (zone[y+2][x+1] not in red_pieces):
            if ( zone[y+1][x] not in red_pieces and zone[y+1][x] not in black_pieces):
                boundary+=str(x+1)+str(y+2)
    #右上右下
    if ( x+2 <= 8 and y-1 >= 0 ):
        if (zone[y-1][x+2] not in red_pieces):
            if ( zone[y][x+1] not in red_pieces and zone[y][x+1] not in black_pieces):
                boundary+=str(x+2)+str(y-1)
    if ( x+2 <= 8 and y+1 <= 9 ):
        if (zone[y+1][x+2] not in red_pieces):
            if ( zone[y][x+1] not in red_pieces and zone[y][x+1] not in black_pieces):
                boundary+=str(x+2)+str(y+1)
    
    return boundary

def r_elephant(x,y,zone):

    x = int(x)
    y = int(y)

    boundary = []

    if ( x-2 >= 0 and y-2 >= 5 ):
        if (zone[y-2][x-2] not in red_pieces):
            if ( zone[y-1][x-1] not in red_pieces and zone[y-1][x-1] not in black_pieces):
                boundary+=str(x-2)+str(y-2)
    if ( x+2 <= 8 and y-2 >= 5 ):
        if (zone[y-2][x+2] not in red_pieces):
            if ( zone[y-1][x+1] not in red_pieces and zone[y-1][x+1] not in black_pieces):
                boundary+=str(x+2)+str(y-2)
    if ( x-2 >= 0 and y+2 <= 9 ):
        if (zone[y+2][x-2] not in red_pieces):
            if ( zone[y+1][x-1] not in red_pieces and zone[y+1][x-1] not in black_pieces):
                boundary+=str(x-2)+str(y+2)
    if ( x+2 <= 8 and y+2 <= 9 ):
        if (zone[y+2][x+2] not in red_pieces):      
            if ( zone[y+1][x+1] not in red_pieces and zone[y+1][x+1] not in black_pieces):
                boundary+=str(x+2)+str(y+2)

    return boundary

def r_sergeant(x,y,zone):
    
    x = int(x)
    y = int(y)

    boundary = []

    if ( x-1 >= 3 and y-1 >= 7 ):
        if (zone[y-1][x-1] not in red_pieces):
            boundary+=str(x-1)+str(y-1)
    if ( x+1 <= 5 and y-1 >= 7 ):
        if (zone[y-1][x+1] not in red_pieces):
            boundary+=str(x+1)+str(y-1)
    if ( x-1 >= 3 and y+1 <= 9 ):
        if (zone[y+1][x-1] not in red_pieces):
            boundary+=str(x-1)+str(y+1)
    if ( x+1 <= 5 and y+1 <= 9 ):
        if (zone[y+1][x+1] not in red_pieces):      
            boundary+=str(x+1)+str(y+1)

    return boundary  

def r_king(x,y,zone):
    
    x = int(x)
    y = int(y)

    boundary = []

    if (x-1>=3):
        if (zone[y][x-1] not in red_pieces):
            boundary+=str(x-1)+str(y)
    if (x+1<=5):
        if (zone[y][x+1] not in red_pieces):
            boundary+=str(x+1)+str(y)
    if (y-1>=7):
        if (zone[y-1][x] not in red_pieces):
            boundary+=str(x)+str(y-1)
    if (y+1<=9):
        if (zone[y+1][x] not in red_pieces):
            boundary+=str(x)+str(y+1)

    return boundary