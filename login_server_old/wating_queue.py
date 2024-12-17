import queue

Wating_q = queue.Queue()

Wating_q.put('Bob')
Wating_q.put('Alice')
Wating_q.put('coco')
Wating_q.put('VIP')
#Wating_q.put('hahaha')
#Wating_q.qsize()
#Wating_q.get()

while ( Wating_q.qsize() > 0 ):
    if ( Wating_q.qsize() > 0 and Wating_q.qsize() != 1 ):
        playera = Wating_q.get()
        playerb = Wating_q.get()
        print(playera + ' VS ' + playerb)
    elif ( Wating_q.qsize() == 1 ):
        print('尚餘一人...等待中...')
        break    