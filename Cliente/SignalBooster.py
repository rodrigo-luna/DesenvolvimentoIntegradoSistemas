import numpy as np

class SignalBooster(object):

    @staticmethod
    def boost(matrix: np.matrix, s: int, n: int) -> np.matrix:
        for c in range(n):
            for l in range(s):
                gamma = 100 + 1/20 * l * np.sqrt(l)

                matrix[l][c] = matrix[l][c] * gamma

        return matrix
