# ==================================================
# SERVIDOR
# ==================================================

import socket

from _thread import *
import threading

print_lock = threading.Lock()

def threaded(c):

	while True:
		data = c.recv(1024)
		
		if not data:
			print('Erro')
			
			print_lock.release()
			break

		c.send(data)

	c.close()


def main():
	host = ""
	port = 8000
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("Socket vinculado à porta", port)

	s.listen(5)
	print("O socket está ouvindo...")

	while True:
		c, addr = s.accept()

		print_lock.acquire()
		print('Conectado a: ', addr[0], ':', addr[1])

		start_new_thread(threaded, (c,))
	s.close()


if __name__ == '__main__':
	main()