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

# ==================================================

def atendeClient(connection, address):
	connection.send(str.encode('Server is working:'))
	while True:
		data = connection.recv(2048)
		if not data:
			break

		dataJSON = json.loads(data.decode('utf-8'))
		dataJSON.update({ "address" : address[0] + ':' + str(address[1]) })

		filePath = 'backup/client_' + dataJSON['id'] + ".txt"
		file = open(filePath, "w")
		file.write(str(dataJSON) + ',\n')
		file.close()

		# response = "Matriz do cliente " + dataJSON["id"] + ' (endereço ' + dataJSON["address"] + ')'

		# processar o sinal
		startTime = timeit.default_timer ()

		time.sleep(1 + random.random()*4)

		if dataJSON["mod"] == 1:
			# reconstrói a imagem com modelo 1
			image = ""
		elif dataJSON["mod"] == 2:
			# reconstrói a imagem com modelo 2
			image = ""

		numberIterations = 0
		sizeInPixels = 0

		finishTime = timeit.default_timer ()
		# fim processar o sinal

		dataJSON.update({
			"startTime" : startTime,
			"finishTime" : finishTime,
			"sizeInPixels" : sizeInPixels,
			"numberIterations" : numberIterations,
			"image" : image
		})

		connection.sendall(str.encode(json.dumps(dataJSON)))

		if os.path.exists(filePath):
			os.remove(filePath)

	connection.close()

def main():
	ServerSideSocket = socket.socket()
	host = '127.0.0.1'
	port = 2004
	queue = []
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
		queue.append([Client, address])

		if len(queue) <= processingLimit:
			Cli, add = queue.pop(0)
			start_new_thread(atendeClient, (Cli, add,))

	ServerSideSocket.close()

if __name__ == '__main__':
	main()
