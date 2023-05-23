# ==================================================
# CLIENTE
# ==================================================

import socket

def main():
    host = '127.0.0.1'
    port = 8000

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    s.connect((host,port))

    i = 1

    while True:
        message = "Teste número " + str(i)
        i += 1
        
        s.send(message.encode('utf-8'))

        data = s.recv(1024)

        print('Recebi do servidor:', str(data.decode('utf-8')))

        ans = input('\nDeseja continuar? (s/n) ')
        if ans == 's':
            continue
        else:
            break

    s.close()

if __name__ == '__main__':
	main()