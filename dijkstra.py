import tkinter as tk
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from display_utils import display_graph_result

def run_dijkstra(frame, vertices, source=0):
    try:
        # Generate a random weighted graph
        graph = nx.erdos_renyi_graph(vertices, 0.5)
        
        # Add random positive weights to edges
        for (u, v) in graph.edges():
            graph[u][v]['weight'] = np.random.randint(1, 10)
        
        # Ensure the graph is connected
        while not nx.is_connected(graph):
            v1, v2 = np.random.randint(0, vertices, 2)
            if not graph.has_edge(v1, v2):
                graph.add_edge(v1, v2, weight=np.random.randint(1, 10))
        
        # Calculate shortest paths using Dijkstra's algorithm
        shortest_paths = nx.single_source_dijkstra_path(graph, source)
        path_lengths = nx.single_source_dijkstra_path_length(graph, source)
        
        # Create a new figure
        plt.clf()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot original graph
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, ax=ax1)
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax1)
        ax1.set_title("Original Graph")
        
        # Create a new graph for shortest paths
        shortest_path_graph = nx.Graph()
        for target in shortest_paths:
            path = shortest_paths[target]
            for i in range(len(path)-1):
                shortest_path_graph.add_edge(path[i], path[i+1])
        
        # Plot shortest paths
        nx.draw(graph, pos, with_labels=True, ax=ax2, edge_color='gray', width=1)
        nx.draw_networkx_edges(graph, pos, ax=ax2, 
                             edgelist=shortest_path_graph.edges(), 
                             edge_color='r', width=2)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax2)
        ax2.set_title(f"Shortest Paths from Source {source}")
        
        # Prepare result text
        result_text = f"Dijkstra's Shortest Paths from vertex {source}\n\n"
        for target in sorted(path_lengths.keys()):
            if target != source:
                path = ' → '.join(str(node) for node in shortest_paths[target])
                result_text += f"To vertex {target}: Distance = {path_lengths[target]}, Path = {path}\n"
        
        # Display the result
        display_graph_result(frame, fig, result_text)
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Error in Dijkstra's algorithm: {str(e)}") 