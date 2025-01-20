from genetic_algorithm import GeneticAlgorithm

def run_algorithm(values):
    tam_poblacion_inicial = values[0]
    tam_poblacion_max = values[1]
    p_cruza = values[2]
    p_mut_ind = values[3]
    p_mut_bit = values[4]
    num_generaciones = values[5]
    A = values[6]
    B = values[7]
    delta_x = values[8]

    ga = GeneticAlgorithm(
        tam_poblacion_inicial,
        tam_poblacion_max,
        p_cruza,
        p_mut_ind,
        p_mut_bit,
        num_generaciones,
        A,
        B,
        delta_x
    )
    
    return ga  # Devolvemos el objeto completo 'ga', no los resultados de la ejecución
