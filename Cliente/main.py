# ==================================================
# CLIENTE
# ==================================================

import json
import numpy as np
import random
import socket
import time
import csv
import cv2
from _thread import *
from SignalBooster import SignalBooster

# ==================================================

HOST = '127.0.0.1'
PORT = 2004
DATA_PATH = 'C:/Users/rluna/Desktop/digo/UTFPR/Desenvolvimento Integrado de Sistemas/DesenvolvimentoIntegradoSistemas/Cliente/data/'

# ==================================================

def should_boost_signal():
    return False
    # return random.randint(0,1) == 0

def boost_signal(matrix: np.matrix, s: int, n: int) -> np.matrix:
    return SignalBooster.boost(matrix, s, n)

def new_signal(m, s):
    if m == 1:
        if s == 1: fileName = 'G-1.csv'
        elif s == 2: fileName = 'G-2.csv'
        elif s == 3: fileName = 'A-60x60-1.csv'
    else:
        if s == 1: fileName = "g-30x30-1.csv"
        elif s == 2: fileName = 'g-30x30-2.csv'
        elif s == 3: fileName = 'A-30x30-1.csv'

    file = open('Cliente/data/' + fileName, "r")
    g = list(csv.reader(file))
    file.close()

    if should_boost_signal():
        g = boost_signal(g, 436, 64)

    return g

def client(i):
    ClientMultiSocket = socket.socket()
    print('Cliente número ' + str(i) + ' enviando novo sinal...')
    try:
        ClientMultiSocket.connect((HOST, PORT))
    except socket.error as e:
        print(str(e))
    res = ClientMultiSocket.recv(65536)

    # model = random.randint(1,2)
    model = 2
    msg = {
        "id": str(i),
        "model": model,
        "signal": new_signal(model, random.randint(1,3))
    }

    ClientMultiSocket.send( str.encode( json.dumps(msg) ) )
    res = ClientMultiSocket.recv(65536*32)
    resJSON = json.loads( res.decode('utf-8') )
    print("Recebi a imagem do cliente " + resJSON["id"])
    # print (resJSON)

    image = np.array(resJSON["image"], float)
    image = np.reshape(image, (30,30))
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite ('Cliente/relatorio/client_' + str(i) + '.png', image)

    file = open('Cliente/relatorio/client_' + resJSON["id"] + '.txt', "w")
    file.write(
        "ID: " + str(resJSON["id"]) +
        "\nTamanho (pixels): " + str(resJSON["sizeInPixels"]) +
        "\nNúmero de iterações: " + str(resJSON["numberIterations"]) +
        "\nTempo de reconstrução (segundos): " + str(resJSON["reconstructionTime"])
        )
    file.close()

    ClientMultiSocket.close()

def main():
    for i in range (50):
        start_new_thread(client, (i,))
        time.sleep(400 + random.randint(1,6))

if __name__ == '__main__':
	main()
