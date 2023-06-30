from numpy import genfromtxt, array_equal
from Cliente import SignalBooster as sb

def boost_test():
     signal_matrix_path = "Cliente/data/g-30x30-1.csv"
     csv_delimiter = ","

     g = genfromtxt(signal_matrix_path, delimiter=csv_delimiter)

     print(g)
     g_boosted = sb.SignalBooster.boost(g, 436, 64)

     print(g_boosted)
     print(array_equal(g, g_boosted))


def main():
    boost_test()

if __name__ == '__main__':
    main()
