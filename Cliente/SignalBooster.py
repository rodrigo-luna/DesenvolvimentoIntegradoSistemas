import numpy as np

class SignalBooster(object):

    @staticmethod
    def boost(matrix: np.matrix, s: int, n: int) -> np.matrix:
        result = matrix
        for c in range(n):
            for l in range(s):
                gamma = 100 + 1/20 * l * np.sqrt(l)
                print(gamma)

                result[c+l] = matrix[c+l] * gamma

            c = c + s

        return result
