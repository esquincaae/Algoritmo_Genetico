import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_graph(fitness_generaciones, poblacion, A, B, dx_final, f, best_x):
    graph_window = tk.Toplevel()
    graph_window.title("Evolución del Fitness y de los Individuos")

    fig = Figure(figsize=(6, 8), dpi=100)

    # Gráfica de la evolución del fitness
    ax1 = fig.add_subplot(211)
    generaciones = list(range(1, len(fitness_generaciones) + 1))
    mejores = [gen[0] for gen in fitness_generaciones]
    peores = [gen[1] for gen in fitness_generaciones]
    promedios = [gen[2] for gen in fitness_generaciones]

    ax1.plot(generaciones, mejores, label="Mejor Fitness", color="blue", marker="o")
    ax1.plot(generaciones, peores, label="Peor Fitness", color="red", linestyle="dashed", marker="x")
    ax1.plot(generaciones, promedios, label="Promedio Fitness", color="green", linestyle="dotted", marker="s")
    
    ax1.set_xlabel("Generaciones")
    ax1.set_ylabel("Fitness")
    ax1.set_title("Evolución del Fitness")
    ax1.legend()

    # Gráfica de f(x) con población
    ax2 = fig.add_subplot(212)
    
    # Generar valores de x en el rango [A, B]
    num_puntos = 1000  # Mayor resolución para la función
    x_vals = [A + (B - A) * i / (num_puntos - 1) for i in range(num_puntos)]  # Generar valores en el intervalo [A, B]
    fx_vals = [f(x) for x in x_vals]
    
    # Graficar la función f(x)
    ax2.plot(x_vals, fx_vals, label="f(x)", color="black")

    # Graficar los individuos
    individuos_x = []
    individuos_fx = []
    
    # Muestra solo una parte representativa de la población si es muy grande
    max_individuos = 500  # Ajusta el tamaño máximo de individuos a graficar
    poblacion_a_graficar = poblacion[:max_individuos]  # Tomamos solo los primeros max_individuos
    
    for ind in poblacion_a_graficar:
        i = int(ind, 2)  # Convierte binario a índice
        x_val = A + i * dx_final
        individuos_x.append(x_val)
        individuos_fx.append(f(x_val))

    ax2.scatter(individuos_x, individuos_fx, color='red', label="Individuos", zorder=5)

    # Graficar la mejor solución (best_x) en f(x)
    best_f_x = f(best_x)  # Calcular f(x) para la mejor solución
    ax2.scatter(best_x, best_f_x, color='green', label="Mejor Solución", zorder=10, marker='*', s=100)

    ax2.set_xlabel("Individuo (x)")
    ax2.set_ylabel("f(x)")
    ax2.set_title("Individuos en el Espacio de f(x)")
    ax2.legend()

    # Ajustar límites de los ejes
    ax2.set_xlim(A, B)  # Ajustar los límites del eje X
    ax2.set_ylim(min(fx_vals) - 1, max(fx_vals) + 1)  # Ajustar el eje Y

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Botón de cerrar
    tk.Button(graph_window, text="Cerrar", command=graph_window.destroy).pack()
