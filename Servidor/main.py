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
		addressJSON = { "address" : address[0] + ':' + str(address[1]) }
		dataJSON.update(addressJSON)

		file = open("log.txt", "a")
		file.write(str(dataJSON) + ',\n')
		file.close()

		response = "Recebi a matriz do cliente " + dataJSON["id"] + ' (endereço ' + dataJSON["address"] + ')'

		time.sleep(1 + random.random()*4)

		connection.sendall(str.encode(response))
	connection.close()

def main():
	ServerSideSocket = socket.socket()
	host = '127.0.0.1'
	port = 2004
	threadCount = 0
	try:
		ServerSideSocket.bind((host, port))
	except socket.error as e:
		print(str(e))
	print('Socket is listening..')
	ServerSideSocket.listen(5)

	file = open("log.txt", "w")
	file.write('')
	file.close()

	while True:
		Client, address = ServerSideSocket.accept()
		print('Connected to: ' + address[0] + ':' + str(address[1]))
		start_new_thread(atendeClient, (Client, address,))
		threadCount += 1
		print('Thread Number: ' + str(threadCount))
	ServerSideSocket.close()

if __name__ == '__main__':
	main()