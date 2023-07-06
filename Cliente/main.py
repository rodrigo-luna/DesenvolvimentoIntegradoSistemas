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
DATA_PATH = 'C:/Users/rluna/Desktop/digo/UTFPR/Desenvolvimento Integrado de Sistemas/DesenvolvimentoIntegradoSistemas/Cliente/data/'

# ==================================================

def should_boost_signal() -> bool:
    return random.randint(0,1) == 0

def boost_signal(matrix: np.matrix, s: int, n: int) -> np.matrix:
    return SignalBooster.boost(matrix, s, n)

def new_signal(m, s):
    if m == 1:
        if s == 1: fileName = 'G-1.csv'
        elif s == 2: fileName = 'G-2.csv'
        elif s == 3: fileName = 'A-60x60-1.csv'
    else:
        if s == 1: fileName = 'g-30x30-1.csv'
        elif s == 2: fileName = 'g-30x30-2.csv'
        elif s == 3: fileName = 'A-30x30-1.csv'

    return np.genfromtxt(DATA_PATH + fileName, delimiter=",")

    # with open(DATA_PATH + fileName, 'r') as file:
    #     reader = csv.reader(file)
    #     M = []
    #     for row in reader:
    #         M.append(row)
    #     return M

def client(i):
    ClientMultiSocket = socket.socket()
    print('Cliente número ' + str(i) + ' tentando conectar...')
    try:
        ClientMultiSocket.connect((HOST, PORT))
    except socket.error as e:
        print(str(e))
    res = ClientMultiSocket.recv(65536)

    model = random.randint(1,2)
    msg = {
        "id": str(i),
        "model": model,
        "signal": str(new_signal(model, random.randint(1,3)))
    }

    ClientMultiSocket.send( str.encode( json.dumps(msg) ) )
    res = ClientMultiSocket.recv(65536)
    resJSON = json.loads( res.decode('utf-8') )
    print("Recebi resposta do cliente: " + resJSON["id"])

    ClientMultiSocket.close()


def main():
    for i in range (50):
        start_new_thread(client, (i,))
        time.sleep(5)
        
if __name__ == '__main__':
	main()
