import numpy as np

def conjugate_gradient_normal_error(base_signal: np.array,
                                    model_matrix: np.array,
                                    initial_guess: np.array,
                                    max_cycles: int) -> np.array:
    
    f = initial_guess
    r = base_signal - np.matmul(model_matrix, f)
    p = np.matmul(np.transpose(model_matrix), r)

    for i in range(max_cycles):
        r_transpose = np.transpose(r)
        alpha = np.matmul( np.matmul(r_transpose, r), np.linalg.inv( np.matmul(np.transpose(p), p) ) )
        f_next = f + alpha * p
        r_next = r - np.matmul( (alpha * model_matrix), p )
        # r_next_transpose = np.transpose(r_next)
        beta = np.matmul( np.matmul(np.transpose(r_next), r_next), np.linalg.inv( np.matmul(np.transpose(r),r) ) )
        
        error = np.linalg.norm(r_next) - np.linalg.norm(r)
        print ('Erro no ciclo ' + str(i) + ':')
        print (error)
        if (error < 0.0001):
            return f_next

        p_next = np.matmul(np.transpose(model_matrix), r_next) + beta * p

        f = f_next
        r = r_next
        p = p_next

    return f


def conjugate_gradient_normal_residual(base_signal: np.array,
                                    model_matrix: np.array,
                                    initial_guess: np.array,
                                    max_cycles: int):
    
    f = initial_guess
    r = base_signal - np.matmul(model_matrix, f)
    z = np.matmul(model_matrix.transpose(), r)
    p = z

    for i in range(max_cycles):
        w = np.matmul(model_matrix, p)
        alpha = (np.linalg.norm(z, ord=2))**2 / (np.linalg.norm(w, ord=2))**2
        f_next = f + alpha * p
        r_next = r - alpha * w

        error = abs(np.linalg.norm(r_next, ord=2) - np.linalg.norm(r, ord=2))
        print ('Erro no ciclo ' + str(i) + ':')
        print (error)
        if (error < 0.0001):
            return f_next, i+1

        z_next = np.matmul(np.transpose(model_matrix), r_next)
        beta = (np.linalg.norm(z_next))**2 / (np.linalg.norm(z))**2
        p_next = z_next + beta * p

        f = f_next
        r = r_next
        z = z_next
        p = p_next

    return f, i+1
