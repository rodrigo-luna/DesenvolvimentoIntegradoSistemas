# ==================================================
# CLIENTE
# ==================================================

import socket
import time
from _thread import *

def teste(i):
    host = '127.0.0.1'
    port = 2004
        
    ClientMultiSocket = socket.socket()
    print('Cliente número ' + str(i) + ' esperando resposta...')
    try:
        ClientMultiSocket.connect((host, port))
    except socket.error as e:
        print(str(e))
    res = ClientMultiSocket.recv(1024)
    
    msg = 'cliente número ' + str(i)
    ClientMultiSocket.send(str.encode(msg))
    res = ClientMultiSocket.recv(1024)
    print(res.decode('utf-8'))

    ClientMultiSocket.close()


def main():
    for i in range (1, 30):
        start_new_thread(teste, (i,))
        time.sleep(1)
        i += 1
        
if __name__ == '__main__':
	main()