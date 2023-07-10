import numpy as np
from Servidor import reconstruction_algorithms as ra
import csv
import cv2

def CGNETest():
    signal_matrix_path = "Cliente/data/G-1.csv"
    model_matrix_path = "Servidor/data/H-1.csv"
    
    print ("Carregando arquivos...")
    file = open(signal_matrix_path, "r")
    g = list(csv.reader(file, delimiter=","))
    g = np.array(g, dtype=float)
    file.close()
    print ("Sinal OK")

    file = open(model_matrix_path, "r")
    H = list(csv.reader(file, delimiter=","))
    H = np.array(H, dtype=float)
    file.close()
    print ("Modelo OK")

    initial_guess = np.zeros((3600,1))
    max_cycles = 15

    print ("Iniciando CGNE...")
    res, i = ra.conjugate_gradient_normal_error(g, H, initial_guess, max_cycles)
    print ("Iterações: " + str(i))
    file = open('teste.csv', "w")
    file.write(str(res))
    file.close()

    res = np.reshape(res, (60,60))
    res = cv2.normalize(res, None, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite ('imagem.png', res)
    

def CGNRTest():
    signal_matrix_path = "Cliente/data/g-30x30-2.csv"
    model_matrix_path = "Servidor/data/H-2.csv"

    print("Carregando arquivos...")

    file = open(signal_matrix_path, "r")
    g = list(csv.reader(file, delimiter=","))
    g = np.array(g, dtype=float)
    file.close()
    print ("Sinal OK")

    file = open(model_matrix_path, "r")
    H = list(csv.reader(file, delimiter=","))
    H = np.array(H, dtype=float)
    file.close()
    print ("Modelo OK")
        
    initial_guess = np.zeros((900,1), dtype=float)
    max_cycles = 25
    print("Iniciando CGNR...")
    res, i = ra.conjugate_gradient_normal_residual(g, H, initial_guess, max_cycles)
    print ("Iterações: " + str(i))
    file = open('resultado.csv', "w")
    file.write(str(res))
    file.close()

    res = np.reshape(res, (30,30))
    res = cv2.normalize(res, None, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite ('imagem.png', res)

def main():
    CGNETest()
    # CGNRTest()


if __name__ == '__main__':
	main()
