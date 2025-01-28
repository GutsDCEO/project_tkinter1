import tkinter as tk
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from display_utils import display_graph_result

# Welsh-Powell Algorithm for graph coloring
def run_welsh_powell(frame, vertices):
    try:
        # Generate a random graph
        graph = nx.erdos_renyi_graph(vertices, 0.5)
        
        # Perform graph coloring
        coloring = nx.coloring.greedy_color(graph, strategy="largest_first")
        
        # Create a new figure
        plt.clf()  # Clear any existing figures
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Plot the graph with coloring
        pos = nx.spring_layout(graph)
        colors = [coloring[node] for node in graph.nodes()]
        nx.draw(graph, pos, with_labels=True, node_color=colors, cmap=plt.cm.Set3, ax=ax)
        nx.draw_networkx_edges(graph, pos, edge_color="black", ax=ax)
        
        # Show the graph in the GUI
        display_graph_result(frame, fig, f"Welsh-Powell Coloring:\n{coloring}")
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Error in Welsh-Powell algorithm: {str(e)}")
