import numpy as np

def calculate_error(residue: np.vector, previous_residue: np.vector) -> np.vector:
    return np.linalg.norm(residue) - np.linalg.norm(previous_residue)


def conjugate_gradient_normal_error(base_signal: np.vector,
                                    model_matrix: np.matrix,
                                    initial_guess: np.vector,
                                    error_threshold: float = 0.0001,
                                    max_cycles: int = 1000) -> np.vector:
    model_matrix_transpose = np.transpose(model_matrix)
    f = initial_guess;
    r = base_signal - np.matmul(model_matrix, f)
    p = np.matmul(model_matrix_transpose, r)

    r_transpose = np.transpose(r)
    alpha_numerator = np.matmul(r_transpose, r)
    for i in range(max_cycles):
        p_transpose = np.transpose(p)
        alpha_den = np.matmul(p_transpose, p)
        reversed_alpha_den = np.linalg.inv(alpha_den)
        alpha = np.matmul(alpha_numerator, reversed_alpha_den)
        f_next = f + np.matmul(alpha, p)
        alpha_H = np.matmul(alpha, model_matrix)
        r_next = r - np.matmul(alpha_H, p)
        r_next_transpose = np.transpose(r_next)
        beta_num = np.matmul(r_next_transpose, r_next)
        reversed_beta_den = np.linalg.inv(alpha_numerator)
        beta = np.matmul(beta_num, reversed_beta_den)
        error = calculate_error(r_next, r)
        if (error < error_threshold):
            return f_next

        p_next = np.matmul(model_matrix_transpose, r_next) + np.matmul(beta, p)

        f = f_next
        r = r_next
        p = p_next
        alpha_numerator = beta_num


    return f
