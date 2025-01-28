import tkinter as tk
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from display_utils import display_graph_result

def run_kruskal(frame, vertices):
    try:
        # Generate a random weighted graph
        graph = nx.erdos_renyi_graph(vertices, 0.5)
        
        # Add random weights to edges
        for (u, v) in graph.edges():
            graph[u][v]['weight'] = np.random.randint(1, 10)
        
        # Find minimum spanning tree using Kruskal's algorithm
        mst = nx.minimum_spanning_tree(graph)
        
        # Create a new figure
        plt.clf()  # Clear any existing figures
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot original graph
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, ax=ax1)
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax1)
        ax1.set_title("Original Graph")
        
        # Plot MST
        nx.draw(mst, pos, with_labels=True, ax=ax2, edge_color='r', width=2)
        mst_edge_labels = nx.get_edge_attributes(mst, 'weight')
        nx.draw_networkx_edge_labels(mst, pos, edge_labels=mst_edge_labels, ax=ax2)
        ax2.set_title("Minimum Spanning Tree")
        
        # Calculate total MST weight
        total_weight = sum(mst[u][v]['weight'] for u, v in mst.edges())
        
        # Show the graph in the GUI
        display_graph_result(frame, fig, f"Kruskal's MST\nTotal Weight: {total_weight}")
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Error in Kruskal's algorithm: {str(e)}") 