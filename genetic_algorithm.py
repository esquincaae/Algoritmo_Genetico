import math
import random

class GeneticAlgorithm:
    def __init__(
        self,
        tam_poblacion_inicial: int,
        tam_poblacion_max: int,
        p_cruza: float,
        p_mut_ind: float,
        p_mut_bit: float,
        num_generaciones: int,
        A: float,
        B: float,
        delta_x: float
    ):
        self.tam_poblacion_inicial = tam_poblacion_inicial
        self.tam_poblacion_max = tam_poblacion_max
        self.p_cruza = p_cruza
        self.p_mut_ind = p_mut_ind
        self.p_mut_bit = p_mut_bit
        self.num_generaciones = num_generaciones
        self.A = A
        self.B = B
        self.delta_x = delta_x
        self.n = None
        self.bits = None
        self.dx_final = None
        self.max_index = None
        self.poblacion = []

    def f(self, x: float) -> float:
        return 0.1 * x * math.log(1 + abs(x)) * (math.cos(x) ** 2)

    def create_individual(self, num_bits: int) -> str:
        return ''.join(str(random.randint(0, 1)) for _ in range(num_bits))

    def create_population(self, num_bits: int):
        return [self.create_individual(num_bits) for _ in range(self.tam_poblacion_inicial)]

    def decode_to_index(self, bits_str: str) -> int:
        return int(bits_str, 2)

    def fitness(self, individuo: str) -> float:
        i = self.decode_to_index(individuo)
        x_val = self.A + i * self.dx_final
        return self.f(x_val)

    def formar_parejas(self, poblacion):
        poblacion_ordenada = sorted(poblacion, key=lambda ind: self.fitness(ind), reverse=True)
        parejas = []
        for i in range(len(poblacion_ordenada)):
            if random.random() <= self.p_cruza:
                j = random.randint(0, i)
                parejas.append((poblacion_ordenada[i], poblacion_ordenada[j]))
        return parejas

    def cruza_un_punto(self, parejas):
        descendientes = []
        for (ind1, ind2) in parejas:
            l = random.randint(1, self.bits - 1)
            seg1a, seg1b = ind1[:l], ind1[l:]
            seg2a, seg2b = ind2[:l], ind2[l:]
            hijo1 = seg1a + seg2b
            hijo2 = seg2a + seg1b
            descendientes.extend([hijo1, hijo2])
        return descendientes

    def mutacion(self, descendientes):
        mutados = []
        for ind in descendientes:
            if random.random() <= self.p_mut_ind:
                nuevo = [
                    '1' if bit == '0' and random.random() <= self.p_mut_bit else
                    '0' if bit == '1' and random.random() <= self.p_mut_bit else
                    bit
                    for bit in ind
                ]
                mutados.append(''.join(nuevo))
            else:
                mutados.append(ind)
        return mutados

    def poda(self, poblacion, descendientes):
        dict_mejor = {}
        for ind in poblacion + descendientes:
            fit_ind = self.fitness(ind)
            if ind not in dict_mejor or fit_ind > dict_mejor[ind]:
                dict_mejor[ind] = fit_ind

        unicos_ordenados = sorted(dict_mejor.keys(), key=lambda x: dict_mejor[x], reverse=True)
        return unicos_ordenados[:self.tam_poblacion_max]

    def calcular_parametros(self):
        self.n = int((self.B - self.A) / self.delta_x) + 1
        self.bits = math.ceil(math.log2(self.n))

        if (2**self.bits - 1) == (self.n - 1):
            self.dx_final = self.delta_x
        else:
            self.dx_final = (self.B - self.A) / (2**self.bits - 1)

        self.max_index = self.n - 1

    def run(self):
        self.calcular_parametros()
        self.poblacion = self.create_population(self.bits)
        fitness_generaciones = []

        for gen in range(self.num_generaciones):
            parejas = self.formar_parejas(self.poblacion)
            descendientes = self.cruza_un_punto(parejas)
            descendientes_mutados = self.mutacion(descendientes)
            self.poblacion = self.poda(self.poblacion, descendientes_mutados)

            fits = [self.fitness(ind) for ind in self.poblacion]
            best_fit = max(fits)
            worst_fit = min(fits)
            avg_fit = sum(fits) / len(fits)

            fitness_generaciones.append((best_fit, worst_fit, avg_fit))
            #print(f"Generación {gen+1}: Mejor = {best_fit:.6f}, Peor = {worst_fit:.6f}, Promedio = {avg_fit:.6f}")

        best_ind = max(self.poblacion, key=lambda ind: self.fitness(ind))
        best_fit = self.fitness(best_ind)
        best_i = self.decode_to_index(best_ind)
        best_x = self.A + best_i * self.dx_final

        return best_x, best_fit, fitness_generaciones
