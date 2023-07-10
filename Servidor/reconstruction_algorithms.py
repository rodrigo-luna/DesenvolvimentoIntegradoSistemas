import numpy as np

def calculate_error(residue: np.array, previous_residue: np.array) -> np.array:
    return np.linalg.norm(residue) - np.linalg.norm(previous_residue)


def conjugate_gradient_normal_error(base_signal: np.array,
                                    model_matrix: np.matrix,
                                    initial_guess: np.array,
                                    error_threshold: float = 0.0001,
                                    max_cycles: int = 1000) -> np.array:
    model_matrix_transpose = np.transpose(model_matrix)
    f = initial_guess
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
        error = np.linalg.norm(r_next) - np.linalg.norm(r)
        if (error < error_threshold):
            return f_next

        p_next = np.matmul(model_matrix_transpose, r_next) + np.matmul(beta, p)

        f = f_next
        r = r_next
        p = p_next
        alpha_numerator = beta_num
        r_transpose = r_next_transpose
        print(str(error))
        


    return f


def conjugate_gradient_normal_residual(base_signal: np.array,
                                       model_matrix: np.matrix,
                                       initial_guess: np.array,
                                       error_threshold: float = 0.0001,
                                       max_cycles: int = 1000) -> np.array:
     f = initial_guess
     r = base_signal - np.matmul(model_matrix, f)
     z = np.matmul(np.transpose(model_matrix), r)
     p = z

     alpha_num = np.linalg.norm(z)^2
     for i in range(max_cycles):
         w = np.matmul(model_matrix, p)
         alpha = alpha_num / np.linalg.norm(w)^2
         f_next = f + alpha * p
         r_next = r - alpha * w

         error = np.linalg.norm(r_next) - np.linalg.norm(r)
         if (error < error_threshold):
             return f_next

         z_next = np.matmul(np.transpose(model_matrix), r_next)
         beta = np.linalg.norm(z_next)^2 / alpha_num
         p_next = z_next + beta * p

         f = f_next
         r = r_next
         z = z_next
         p = p_next
         alpha_num = np.linalg.norm(z_next)^2
         print(str(error))


     return f
