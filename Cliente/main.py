# ==================================================
# CLIENTE
# ==================================================

import socket
import time
import random
import json
from _thread import *

# ==================================================

HOST = '127.0.0.1'
PORT = 2004

# ==================================================

# apenas para teste
def generateRandomMatrix(length):
    matrix = ''
    for i in range (length):
        matrix += str(random.randint(1000,9999)) + ','
    return matrix

def client(i):
    ClientMultiSocket = socket.socket()
    print('Cliente número ' + str(i) + ' tentando conectar...')
    try:
        ClientMultiSocket.connect((HOST, PORT))
    except socket.error as e:
        print(str(e))
    res = ClientMultiSocket.recv(1024)
    
    msg = {
        "id": str(i),
        "mat": generateRandomMatrix(20)
    }

    ClientMultiSocket.send( str.encode( json.dumps(msg) ) )
    res = ClientMultiSocket.recv(2048)
    print(res.decode('utf-8'))

    ClientMultiSocket.close()


def main():
    for i in range (50):
        start_new_thread(client, (i,))
        time.sleep(1)
        i += 1
        
if __name__ == '__main__':
	main()