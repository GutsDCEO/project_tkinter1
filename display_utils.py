import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def display_graph_result(frame, fig, result):
    try:
        if frame.winfo_exists():
            result_label = tk.Label(frame, text=result, font=("Arial", 12), wraplength=700)
            result_label.pack(pady=10)
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack()
    except tk.TclError:
        print("Window was closed before displaying results")

def display_matrix_result(frame, matrix, supply, demand, result):
    try:
        if frame.winfo_exists():
            result_label = tk.Label(frame, text=result, font=("Arial", 12), wraplength=700)
            result_label.pack(pady=10)
    except tk.TclError:
        print("Window was closed before displaying results")
