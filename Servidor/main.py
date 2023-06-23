# ==================================================
# SERVIDOR
# ==================================================

import socket
import os
from _thread import *
import random
import time
import json

# ==================================================

def atendeClient(connection, address):
	connection.send(str.encode('Server is working:'))
	while True:
		data = connection.recv(2048)
		if not data:
			break

		dataJSON = json.loads(data.decode('utf-8'))
		dataJSON.update({ "address" : address[0] + ':' + str(address[1]) })

		filePath = 'backup/' + dataJSON['id'] + ".txt"
		file = open(filePath, "w")
		file.write(str(dataJSON) + ',\n')
		file.close()

		response = "Recebi a matriz do cliente " + dataJSON["id"] + ' (endereço ' + dataJSON["address"] + ')'

		# processar o sinal
		time.sleep(1 + random.random()*4)
		# fim processar o sinal

		connection.sendall(str.encode(response))

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