import tkinter as tk
from tkinter import messagebox
from genetic_algorithm import GeneticAlgorithm
from graph import show_graph  # Importar la función de las gráficas

class GeneticAlgorithmGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Algoritmo Genético")

        # Etiquetas y campos de entrada
        self.label1 = tk.Label(master, text="Tamaño de la población inicial:")
        self.label1.grid(row=0, column=0)
        self.tam_poblacion_inicial_entry = tk.Entry(master)
        self.tam_poblacion_inicial_entry.grid(row=0, column=1)

        self.label2 = tk.Label(master, text="Tamaño máximo de la población:")
        self.label2.grid(row=1, column=0)
        self.tam_poblacion_max_entry = tk.Entry(master)
        self.tam_poblacion_max_entry.grid(row=1, column=1)

        self.label3 = tk.Label(master, text="Probabilidad de cruza:")
        self.label3.grid(row=2, column=0)
        self.p_cruza_entry = tk.Entry(master)
        self.p_cruza_entry.grid(row=2, column=1)

        self.label4 = tk.Label(master, text="Probabilidad de mutación de individuo:")
        self.label4.grid(row=3, column=0)
        self.p_mut_ind_entry = tk.Entry(master)
        self.p_mut_ind_entry.grid(row=3, column=1)

        self.label5 = tk.Label(master, text="Probabilidad de mutación de bit:")
        self.label5.grid(row=4, column=0)
        self.p_mut_bit_entry = tk.Entry(master)
        self.p_mut_bit_entry.grid(row=4, column=1)

        self.label6 = tk.Label(master, text="Número de generaciones:")
        self.label6.grid(row=5, column=0)
        self.num_generaciones_entry = tk.Entry(master)
        self.num_generaciones_entry.grid(row=5, column=1)

        self.label7 = tk.Label(master, text="Inicio del intervalo (A):")
        self.label7.grid(row=6, column=0)
        self.A_entry = tk.Entry(master)
        self.A_entry.grid(row=6, column=1)

        self.label8 = tk.Label(master, text="Fin del intervalo (B):")
        self.label8.grid(row=7, column=0)
        self.B_entry = tk.Entry(master)
        self.B_entry.grid(row=7, column=1)

        self.label9 = tk.Label(master, text="Delta X inicial:")
        self.label9.grid(row=8, column=0)
        self.delta_x_entry = tk.Entry(master)
        self.delta_x_entry.grid(row=8, column=1)

        # Área de texto para mostrar los resultados
        self.result_text = tk.Text(master, height=7, width=40)
        self.result_text.grid(row=9, column=0, columnspan=2)

        # Botón para ejecutar el algoritmo
        self.run_button = tk.Button(master, text="Ejecutar Algoritmo", command=self.run_algorithm)
        self.run_button.grid(row=10, column=0, columnspan=2)

    def run_algorithm(self):
        try:
            # Obtener los valores de los campos de entrada
            tam_poblacion_inicial = int(self.tam_poblacion_inicial_entry.get())
            tam_poblacion_max = int(self.tam_poblacion_max_entry.get())
            p_cruza = float(self.p_cruza_entry.get())
            p_mut_ind = float(self.p_mut_ind_entry.get())
            p_mut_bit = float(self.p_mut_bit_entry.get())
            num_generaciones = int(self.num_generaciones_entry.get())
            A = float(self.A_entry.get())
            B = float(self.B_entry.get())
            delta_x = float(self.delta_x_entry.get())

            # Validaciones de los valores ingresados
            error_message = ""
            if tam_poblacion_inicial < 1 or type(tam_poblacion_inicial) != int:
                error_message += "-El valor de la población inicial debe ser un entero positivo\n"
            if type(tam_poblacion_max) != int:
                error_message += "-El valor de la población maxima debe ser entero positivo\n"
            if tam_poblacion_inicial > tam_poblacion_max:
                error_message += "-El tamaño de la población inicial no puede ser mayor que el tamaño máximo.\n"
            if A >= B:
                error_message += "-El valor de A debe ser menor que el valor de B.\n"
            if not (0 <= p_cruza <= 1):
                error_message += "-La probabilidad de cruza debe estar entre 0 y 1.\n"
            if not (0 <= p_mut_ind <= 1):
                error_message += "-La probabilidad de mutación de individuo debe estar entre 0 y 1.\n"
            if not (0 <= p_mut_bit <= 1):
                error_message += "-La probabilidad de mutación de bit debe estar entre 0 y 1.\n"

            if error_message:
                messagebox.showerror("Error", error_message)
                return

            # Crear el algoritmo genético
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

            # Ejecutar el algoritmo y obtener los resultados
            best_x, best_f_x, fitness_generaciones = ga.run()

            # Calcular la representación binaria correctamente
            best_i = round((best_x - A) / ga.dx_final)  # Obtener el índice en la escala binaria
            best_x_binary = bin(best_i)[2:].zfill(ga.bits)  # Convertir a binario con la longitud correcta

            # Mostrar los resultados en el área de texto
            self.result_text.delete(1.0, tk.END)  # Limpiar el área de texto
            self.result_text.insert(tk.END, f"Mejor x: {best_x}\nMejor f(x): {best_f_x}\nBits de la mejor solucion: {best_x_binary}")

            # Mostrar la gráfica en una nueva ventana
            show_graph(fitness_generaciones, ga.poblacion, A, B, ga.dx_final, ga.f, best_x)

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese todos los datos correctamente.")
