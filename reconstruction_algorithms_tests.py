import sys
from Servidor import reconstruction_algorithms as ra

def CGNETest():
    signal_matrix_path = "Cliente/data/g-30x30-1.csv"
    model_matrix_path = "Servidor/data/H-2.csv"
    csv_delimiter = ","

    g = genfromtxt(signal_matrix_path, delimiter=csv_delimiter)
    H = genfromtxt(model_matrix_path, delimiter=csv_delimiter)
    initial_guess = zeros((900,1))
    print(initial_guess)
    print(H)

    ra.conjugate_gradient_normal_error(g, H, initial_guess, max_cycles=12)


def CGNRTest():
    signal_matrix_path = "Cliente/data/g-30x30-1.csv"
    model_matrix_path = "Servidor/data/H-2.csv"
    csv_delimiter = ","

    g = genfromtxt(signal_matrix_path, delimiter=csv_delimiter)
    H = genfromtxt(model_matrix_path, delimiter=csv_delimiter)
    initial_guess = zeros((900,1))
    print(initial_guess)
    print(H)

    ra.conjugate_gradient_normal_residual(g, H, initial_guess, max_cycles=5)


def main():
    CGNETest()


if __name__ == '__main__':
	main()
