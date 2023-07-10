import numpy as np

def calculate_error(residue: np.array, previous_residue: np.array) -> np.array:
    return np.linalg.norm(residue) - np.linalg.norm(previous_residue)


def conjugate_gradient_normal_error(base_signal: np.array,
                                    model_matrix: np.matrix,
                                    initial_guess: np.array,
                                    error_threshold: float = 0.0001,
                                    max_cycles: int = 1000) -> np.array:
    print("Starting CGNE Algorithm...")
    r = base_signal - np.matmul(model_matrix, initial_guess)
    print("r calculated")
    p = np.matmul(np.transpose(model_matrix), r)
    print("p calculated")

    for i in range(max_cycles):
        print(i)
        alpha_numerator = np.matmul(np.transpose(r), r)
        alpha_den = np.matmul(np.transpose(p), p)
        alpha = np.matmul(alpha_numerator, np.linalg.inv(alpha_den))

        f_next = initial_guess + np.matmul(alpha, p)
        r_next = r - np.matmul(np.matmul(alpha, model_matrix), p)
        # r_next_transpose = np.transpose(r_next)
        beta_num = np.matmul(np.transpose(r_next), r_next)
        reversed_beta_den = np.linalg.inv(alpha_numerator)
        beta = np.matmul(beta_num, reversed_beta_den)
        # error = calculate_error(r_next, r)
        if (np.linalg.norm(r_next) - np.linalg.norm(r) < error_threshold):
            return f_next

        p_next = np.matmul(np.transpose(model_matrix), r_next) + np.matmul(beta, p)

        initial_guess = f_next
        r = r_next
        p = p_next
        alpha_numerator = beta_num
        # r_transpose = r_next_transpose
        # print(str(error))

    return initial_guess


def conjugate_gradient_normal_residual(base_signal: np.array,
                                       model_matrix: np.matrix,
                                       initial_guess: np.array,
                                       error_threshold: float = 0.0001,
                                       max_cycles: int = 1000) -> np.array:
     print("Starting CGNR Algorithm...")
     model_matrix_transpose = np.transpose(model_matrix)
     f = initial_guess
     r = base_signal - np.matmul(model_matrix, f)
     z = np.matmul(model_matrix_transpose, r)
     p = z

     alpha_num = np.power(np.linalg.norm(z), 2)
     for i in range(max_cycles):
         w = np.matmul(model_matrix, p)
         alpha_den = np.power(np.linalg.norm(w), 2)
         alpha = alpha_num / alpha_den
         f_next = f + alpha * p
         r_next = r - alpha * w

         error = calculate_error(r_next, r)
         if (error < error_threshold):
             return f_next

         z_next = np.matmul(model_matrix_transpose, r_next)
         beta_num = np.power(np.linalg.norm(z_next), 2)
         beta = beta_num / alpha_num
         p_next = z_next + beta * p

         f = f_next
         r = r_next
         z = z_next
         p = p_next
         alpha_num = beta_num
         print(str(error))


     return f
