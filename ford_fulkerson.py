import tkinter as tk
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from display_utils import display_graph_result

def run_ford_fulkerson(frame, vertices):
    try:
        # Generate a random flow network
        graph = nx.DiGraph()
        
        # Add nodes
        graph.add_nodes_from(range(vertices))
        
        # Add random edges with capacities
        for i in range(vertices):
            for j in range(i+1, vertices):
                if np.random.random() < 0.4:  # 40% chance of edge
                    graph.add_edge(i, j, capacity=np.random.randint(1, 15))
        
        # Ensure source (0) and sink (vertices-1) are connected
        if not nx.has_path(graph, 0, vertices-1):
            path = nx.shortest_path(graph.to_undirected(), 0, vertices-1)
            for i in range(len(path)-1):
                if not graph.has_edge(path[i], path[i+1]):
                    graph.add_edge(path[i], path[i+1], capacity=np.random.randint(1, 15))
        
        # Calculate maximum flow
        flow_value, flow_dict = nx.maximum_flow(graph, 0, vertices-1)
        
        # Create visualization
        plt.clf()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot original graph with capacities
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, ax=ax1, node_color='lightblue', arrows=True)
        edge_labels = nx.get_edge_attributes(graph, 'capacity')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax1)
        ax1.set_title("Original Network (Capacities)")
        
        # Create flow graph
        flow_graph = nx.DiGraph(graph)
        for u in flow_dict:
            for v, flow in flow_dict[u].items():
                flow_graph[u][v]['flow'] = flow
        
        # Plot flow graph
        nx.draw(flow_graph, pos, with_labels=True, ax=ax2, node_color='lightblue', arrows=True)
        edge_labels = {(u, v): f"{flow_dict[u][v]}/{graph[u][v]['capacity']}"
                      for u, v in graph.edges()}
        nx.draw_networkx_edge_labels(flow_graph, pos, edge_labels=edge_labels, ax=ax2)
        ax2.set_title("Maximum Flow Network (Flow/Capacity)")
        
        # Prepare result text
        result_text = f"Ford-Fulkerson Maximum Flow\n\n"
        result_text += f"Maximum Flow Value: {flow_value}\n\n"
        result_text += "Flow Details:\n"
        for u in sorted(flow_dict.keys()):
            for v in sorted(flow_dict[u].keys()):
                if flow_dict[u][v] > 0:
                    result_text += f"Edge {u}->{v}: Flow = {flow_dict[u][v]}, Capacity = {graph[u][v]['capacity']}\n"
        
        # Display the result
        display_graph_result(frame, fig, result_text)
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Error in Ford-Fulkerson algorithm: {str(e)}") 