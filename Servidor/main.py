# ==================================================
# SERVIDOR
# ==================================================

import socket
import os
from _thread import *
import timeit
import json
import csv
import cv2
import reconstruction_algorithms

import numpy as np

# ==================================================

error_threshold = 0.1
max_calc_cycles = 10
processing = 0

def atendeClient(connection, address):
	global processing
	connection.send(str.encode('Server is working:'))
	while True:
		data = connection.recv(65536*32)
		if not data:
			break
		dataJSON = json.loads(data.decode('utf-8'))
		dataJSON.update({ "address" : address[0] + ':' + str(address[1]) })

		filePath = 'backup/client_' + dataJSON['id'] + ".txt"
		file = open(filePath, "w")
		file.write(str(dataJSON) + ',\n')
		file.close()

		# ========== processar o sinal ==========
		startTime = timeit.default_timer ()

		if dataJSON["model"] == 1:
			file = open('Servidor/data/H-1.csv', "r")
			H = list(csv.reader(file))
			file.close()
			H = np.array(H, dtype=float)
			
			image, numberIterations = reconstruction_algorithms.conjugate_gradient_normal_error(
				np.array(dataJSON["signal"], dtype=float),
				H,
				np.zeros((3600,1)),
				50)
			sizeInPixels = 3600

		elif dataJSON["model"] == 2:
			file = open('Servidor/data/H-2.csv', "r")
			H = list(csv.reader(file))
			file.close()
			H = np.array(H, dtype=float)

			image, numberIterations = reconstruction_algorithms.conjugate_gradient_normal_residual(
				np.array(dataJSON["signal"], float),
				H,
				np.zeros((900,1)),
				50)
			sizeInPixels = 900
		else:
			break

		finishTime = timeit.default_timer ()
		# ========== fim processar o sinal ==========

		del dataJSON['signal']
		dataJSON.update({
			"reconstructionTime" : finishTime - startTime,
			"sizeInPixels" : sizeInPixels,
			"numberIterations" : numberIterations,
			"image" : image.tolist()
		})

		connection.sendall(str.encode(json.dumps(dataJSON)))
		processing -= 1
		if os.path.exists(filePath):
			os.remove(filePath)

	connection.close()

def main():
	global processing
	ServerSideSocket = socket.socket()
	host = '127.0.0.1'
	port = 2004
	queue = []
	queueLimit= 1
	processing = 0
	processingLimit = 5

	try:
		ServerSideSocket.bind((host, port))
	except socket.error as e:
		print(str(e))
	print('Socket is listening..')
	ServerSideSocket.listen(10)

	while True:
		Client, address = ServerSideSocket.accept()
		print('Conectado a: ' + address[0] + ':' + str(address[1]))
		if len(queue) < queueLimit:
			queue.append([Client, address])

		if processing <= processingLimit:
			Cli, add = queue.pop(0)
			processing += 1
			start_new_thread(atendeClient, (Cli, add,))

	ServerSideSocket.close()

if __name__ == '__main__':
	main()
