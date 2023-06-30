# ==================================================
# CLIENTE
# ==================================================

import json
import numpy as np
import random
import socket
import time
import csv
from _thread import *
from SignalBooster import SignalBooster

# ==================================================

HOST = '127.0.0.1'
PORT = 2004
DATA_PATH = 'C:/Users/rluna/Desktop/teste/data/'

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

def new_signal(s):
    if s == 1: fileName = 'G-1.csv'
    elif s == 2: fileName = 'G-2.csv'
    elif s == 3: fileName = 'g-30x30-1.csv'
    elif s == 4: fileName = 'g-30x30-2.csv'
    elif s == 5: fileName = 'A-30x30-1.csv'
    elif s == 6: fileName = 'A-30x30-2.csv'

    with open(DATA_PATH + fileName, 'r') as file:
        reader = csv.reader(file)
        M = []
        for row in reader:
            M.append(row)
        return M

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
        "model": random.randint(1,2),
        "signal": new_signal(random.randint(1,6))
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
