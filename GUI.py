import os
import sys
import tkinter as tk
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

from display_utils import display_graph_result, display_matrix_result
from welsh_powell import run_welsh_powell


# Define algorithms list
algorithms = ["Welsh-Powell", "Dijkstra", "Kruskal", "Bellman-Ford", "Ford-Fulkerson", "North-West Corner", "Least Cost", "Stepping-Stone", "Potential Method"]

def create_credits_frame(parent):
    """Create a professionally styled credits frame"""
    credits_frame = tk.Frame(parent, bg='#f0f0f0', relief=tk.RIDGE, bd=1)
    credits_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    credits_text = tk.Label(
        credits_frame,
        text="Développé par El Oumami Ahmed Amine\nSous l'encadrement de Prof. Mouna El Mkhalet",
        font=("Helvetica", 10),
        bg='#f0f0f0',
        fg='#555555',
        pady=5
    )
    credits_text.pack()

def setup_main_window():
    root = tk.Tk()
    root.title("Algorithmes de Recherche Opérationnelle")
    root.geometry("800x600")
    
    # Set window background color
    root.configure(bg='#ffffff')
    
    # Create main container with padding
    main_container = tk.Frame(root, bg='#ffffff', padx=20, pady=20)
    main_container.pack(fill=tk.BOTH, expand=True)
    
    # Load and display logo
    try:
        if getattr(sys, 'frozen', False):

            # If the application is frozen (running as an executable)

            base_path = sys._MEIPASS

        else:

            # If the application is running in a normal Python environment

            base_path = os.path.dirname(__file__)



        logo_path = os.path.join(base_path, 'img', 'logo emsi.png')

        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((500, 150), Image.LANCZOS)  # Adjust size as needed
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(main_container, image=logo_photo, bg='#ffffff')
        logo_label.image = logo_photo  # Keep a reference
        logo_label.pack(pady=(0, 20))
    except Exception as e:
        print(f"Could not load logo: {e}")
    
    # Title with enhanced styling
    title_label = tk.Label(
        main_container,
        text="Algorithmes de Recherche Opérationnelle",
        font=("Helvetica", 20, "bold"),
        bg='#ffffff',
        fg='#2c3e50'
    )
    title_label.pack(pady=(0, 30))
    
    # Main button with hover effect
    class HoverButton(tk.Button):
        def __init__(self, master, **kw):
            tk.Button.__init__(self, master=master, **kw)
            self.defaultBackground = self["background"]
            self.bind("<Enter>", self.on_enter)
            self.bind("<Leave>", self.on_leave)

        def on_enter(self, e):
            self['background'] = '#2980b9'
            self['fg'] = 'white'

        def on_leave(self, e):
            self['background'] = self.defaultBackground
            self['fg'] = 'black'
    
    btn_algorithm = HoverButton(
        main_container,
        text="Algorithmes RO",
        width=20,
        command=open_algorithm_interface,
        font=("Helvetica", 12),
        relief=tk.RAISED,
        bg='#3498db',
        fg='white',
        padx=20,
        pady=10
    )
    btn_algorithm.pack(pady=20)
    
    # Control buttons frame
    control_frame = tk.Frame(main_container, bg='#ffffff')
    control_frame.pack(pady=20)
    
    btn_entry = HoverButton(
        control_frame,
        text="Entrée",
        width=12,
        command=lambda: print("Entrée clicked"),
        font=("Helvetica", 11),
        bg='#2ecc71',
        fg='white'
    )
    btn_entry.pack(side=tk.LEFT, padx=10)
    
    btn_exit = HoverButton(
        control_frame,
        text="Sortie",
        width=12,
        command=root.quit,
        font=("Helvetica", 11),
        bg='#e74c3c',
        fg='white'
    )
    btn_exit.pack(side=tk.LEFT, padx=10)
    
    # Add credits at the bottom
    create_credits_frame(main_container)
    
    return root

def open_algorithm_interface():
    algo_window = tk.Toplevel(root)
    algo_window.title("Interface des Algorithmes")
    algo_window.geometry("600x500")
    algo_window.configure(bg='#ffffff')
    
    frame = tk.Frame(algo_window, bg='#ffffff')
    frame.pack(pady=20)
    
    title_label = tk.Label(
        frame,
        text="Sélectionner un Algorithme",
        font=("Helvetica", 16, "bold"),
        bg='#ffffff',
        fg='#2c3e50'
    )
    title_label.pack(pady=15)
    
    for i in range(0, len(algorithms), 3):
        button_frame = tk.Frame(frame, bg='#ffffff')
        button_frame.pack(pady=5)
        for algo in algorithms[i:i+3]:
            btn = tk.Button(
                button_frame,
                text=algo,
                width=20,
                command=lambda a=algo: open_algorithm_window(a),
                font=("Helvetica", 11),
                bg='#3498db',
                fg='white',
                relief=tk.RAISED
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)

def open_algorithm_window(algo_name):
    algo_window = tk.Toplevel(root)
    algo_window.title(f"{algo_name} Interface")
    algo_window.geometry("800x600")

    frame = tk.Frame(algo_window)
    frame.pack(pady=20)

    title_label = tk.Label(frame, text=f"Algorithm: {algo_name}", font=("Helvetica", 14, "bold"))
    title_label.pack(pady=10)

    # Get input frame and its entries
    input_frame, input_fields = create_algorithm_inputs(frame, algo_name)

    def execute_algorithm():
        try:
            vertices = int(input_fields['vertices'].get())
            if vertices <= 0:
                raise ValueError("Number of vertices must be positive")

            # Get additional inputs based on algorithm type
            kwargs = {'vertices': vertices}
            
            if algo_name in ["Dijkstra", "Bellman-Ford"]:
                kwargs['source'] = int(input_fields['source'].get())
            elif algo_name in ["North-West Corner", "Least Cost", "Stepping-Stone", "Potential Method"]:
                kwargs['supply'] = [int(x) for x in input_fields['supply'].get().split(',')]
                kwargs['demand'] = [int(x) for x in input_fields['demand'].get().split(',')]

            display_algorithm_code_and_result(algo_name, **kwargs)
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    btn_execute = tk.Button(frame, text="Execute", width=20, command=execute_algorithm)
    btn_execute.pack(pady=10)

def display_algorithm_code_and_result(algo_name, **kwargs):
    result_window = tk.Toplevel(root)
    result_window.title(f"{algo_name} Result")
    result_window.geometry("800x600")

    frame = tk.Frame(result_window)
    frame.pack(pady=20)

    title_label = tk.Label(frame, text=f"{algo_name} Result", font=("Helvetica", 14, "bold"))
    title_label.pack(pady=10)

    # Call the respective algorithm module based on the algorithm name
    if algo_name == "Welsh-Powell":
        from welsh_powell import run_welsh_powell
        run_welsh_powell(frame, kwargs['vertices'])
    elif algo_name == "Dijkstra":
        from dijkstra import run_dijkstra
        run_dijkstra(frame, kwargs['vertices'])
    elif algo_name == "Kruskal":
        from kruskal import run_kruskal
        run_kruskal(frame, kwargs['vertices'])
    elif algo_name == "Bellman-Ford":
        from bellman_ford import run_bellman_ford
        run_bellman_ford(frame, kwargs['vertices'], kwargs['source'])
    elif algo_name == "Ford-Fulkerson":
        from ford_fulkerson import run_ford_fulkerson
        run_ford_fulkerson(frame, kwargs['vertices'])
    elif algo_name == "North-West Corner":
        from north_west_corner import run_north_west_corner
        run_north_west_corner(frame, kwargs['vertices'])
    elif algo_name == "Least Cost":
        from least_cost import run_least_cost_method
        run_least_cost_method(frame, kwargs['vertices'])
    elif algo_name == "Stepping-Stone":
        from stepping_stone import run_stepping_stone_method
        run_stepping_stone_method(frame, kwargs['vertices'])
    elif algo_name == "Potential Method":
        from potential_method import run_potential_method
        run_potential_method(frame, kwargs['vertices'])
        
        
    # Display Graph Result
def display_graph_result(frame, fig, result):
    result_label = tk.Label(frame, text=result, font=("Arial", 12), wraplength=700)
    result_label.pack(pady=10)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Display Matrix Result
def display_matrix_result(frame, matrix, supply, demand, result):
    result_label = tk.Label(frame, text=result, font=("Arial", 12), wraplength=700)
    result_label.pack(pady=10)

def create_welsh_powell_frame(parent):
    frame = tk.Frame(parent)
    
    # Create a frame for the results
    result_frame = tk.Frame(frame)
    result_frame.pack(fill=tk.BOTH, expand=True)
    
    # Input for number of vertices
    vertices_frame = tk.Frame(frame)
    vertices_frame.pack(pady=5)
    
    vertices_label = tk.Label(vertices_frame, text="Number of vertices:")
    vertices_label.pack(side=tk.LEFT)
    
    vertices_entry = tk.Entry(vertices_frame)
    vertices_entry.insert(0, "5")  # Default value
    vertices_entry.pack(side=tk.LEFT)
    
    def run_algorithm():
        # Clear previous results
        for widget in result_frame.winfo_children():
            widget.destroy()
            
        try:
            vertices = int(vertices_entry.get())
            if vertices <= 0:
                raise ValueError("Number of vertices must be positive")
            run_welsh_powell(result_frame, vertices)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    # Run button
    run_button = tk.Button(frame, text="Run Welsh-Powell", command=run_algorithm)
    run_button.pack(pady=5)
    
    return frame

def create_algorithm_inputs(frame, algo_name):
    input_frame = tk.Frame(frame)
    input_frame.pack(pady=10)
    
    # Dictionary to store all input fields
    input_fields = {}
    
    # Common vertices input
    vertices_frame = tk.Frame(input_frame)
    vertices_frame.pack(pady=5)
    
    vertices_label = tk.Label(vertices_frame, text="Number of vertices:")
    vertices_label.pack(side=tk.LEFT)
    
    vertices_entry = tk.Entry(vertices_frame)
    vertices_entry.insert(0, "5")
    vertices_entry.pack(side=tk.LEFT, padx=5)
    input_fields['vertices'] = vertices_entry
    
    # Algorithm-specific inputs
    if algo_name in ["Dijkstra", "Bellman-Ford"]:
        source_frame = tk.Frame(input_frame)
        source_frame.pack(pady=5)
        
        source_label = tk.Label(source_frame, text="Source vertex:")
        source_label.pack(side=tk.LEFT)
        
        source_entry = tk.Entry(source_frame)
        source_entry.insert(0, "0")
        source_entry.pack(side=tk.LEFT, padx=5)
        input_fields['source'] = source_entry
        
    elif algo_name in ["North-West Corner", "Least Cost", "Stepping-Stone", "Potential Method"]:
        supply_frame = tk.Frame(input_frame)
        supply_frame.pack(pady=5)
        
        supply_label = tk.Label(supply_frame, text="Supply (comma-separated):")
        supply_label.pack(side=tk.LEFT)
        
        supply_entry = tk.Entry(supply_frame)
        supply_entry.insert(0, "20,30,25")
        supply_entry.pack(side=tk.LEFT, padx=5)
        input_fields['supply'] = supply_entry
        
        demand_frame = tk.Frame(input_frame)
        demand_frame.pack(pady=5)
        
        demand_label = tk.Label(demand_frame, text="Demand (comma-separated):")
        demand_label.pack(side=tk.LEFT)
        
        demand_entry = tk.Entry(demand_frame)
        demand_entry.insert(0, "15,25,35")
        demand_entry.pack(side=tk.LEFT, padx=5)
        input_fields['demand'] = demand_entry
    
    return input_frame, input_fields



root = setup_main_window()

root.mainloop()