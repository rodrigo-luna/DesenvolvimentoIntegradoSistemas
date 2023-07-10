# ==================================================
# SERVIDOR
# ==================================================

import socket
import os
from _thread import *
import random
import time
import timeit
import json
import reconstruction_algorithms

from numpy import genfromtxt, zeros

# ==================================================

error_threshold = 0.1
max_calc_cycles = 10
processing = 0

def decide_reconstruction_algorithm() -> str:
	return "CGNE"

def atendeClient(connection, address):
	global processing
	connection.send(str.encode('Server is working:'))
	while True:
		data = connection.recv(65536)
		if not data:
			break
		d = data.decode('utf-8')
		print (d)
		dataJSON = json.loads(d)
		dataJSON.update({ "address" : address[0] + ':' + str(address[1]) })

		filePath = 'backup/client_' + dataJSON['id'] + ".txt"
		file = open(filePath, "w")
		file.write(str(dataJSON) + ',\n')
		file.close()

		# ========== processar o sinal ==========
		startTime = timeit.default_timer ()

		model_matrix = []
		initial_guess = []
		if dataJSON["model"] == 1:
			# reconstrói a imagem com modelo 1
			# model_matrix = genfromtxt("Servidor/data/H-1.csv", delimiter=",")
			# initial_guess = zeros((3600),1)
			sizeInPixels = 3600
		elif dataJSON["model"] == 2:
			# reconstrói a imagem com modelo 2
			# model_matrix = genfromtxt("Servidor/data/H-2.csv", delimiter=",")
			# initial_guess = zeros((900,1))
			sizeInPixels = 900
		else:
			break

		image = []
		# if (decide_reconstruction_algorithm() == "CGNE"):
		# 	image = reconstruction_algorithms.conjugate_gradient_normal_error(
		# 		dataJSON["signal"],
		# 		model_matrix,
		# 		initial_guess,
		# 		error_threshold=error_threshold,
		# 		max_cycles=max_calc_cycles)

		# else: 
		# 	image = reconstruction_algorithms.conjugate_gradient_normal_residual(
		# 		dataJSON["signal"],
		# 		model_matrix,
		# 		initial_guess, 
		# 		error_threshold=error_threshold,
		# 		max_cycles=max_calc_cycles)
		numberIterations = 0

		# simular o processamento
		time.sleep(random.randint(3,5))

		finishTime = timeit.default_timer ()
		# ========== fim processar o sinal ==========

		del dataJSON['signal']
		dataJSON.update({
			"startTime" : startTime,
			"finishTime" : finishTime,
			"sizeInPixels" : sizeInPixels,
			"numberIterations" : numberIterations,
			"image" : image
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
	ServerSideSocket.listen(5)

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
