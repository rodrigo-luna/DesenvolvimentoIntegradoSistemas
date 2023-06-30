# ==================================================
# CLIENTE
# ==================================================

import json
import numpy as np
import random
import socket
import time
from _thread import *
from SignalBooster import SignalBooster

# ==================================================

HOST = '127.0.0.1'
PORT = 2004

# ==================================================

# apenas para teste
def generateRandomSignal(length):
    signal = ''
    for i in range (length):
        signal += str(random.randint(1000,9999)) + ','
    return signal

def should_boost_signal() -> bool:
    return random.randint(0,1) == 0

def boost_signal(matrix: np.matrix, s: int, n: int) -> np.matrix:
    return SignalBooster.boost(matrix, s, n)

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
        "mod": 1,
        "sig": generateRandomSignal(20)
    }

    ClientMultiSocket.send( str.encode( json.dumps(msg) ) )
    res = ClientMultiSocket.recv(2048)
    resJSON = json.loads( res.decode('utf-8') )
    print("Recebi resposta do cliente: " + resJSON["id"])

    ClientMultiSocket.close()


def main():
    for i in range (50):
        start_new_thread(client, (i,))
        time.sleep(1)
        
if __name__ == '__main__':
	main()
