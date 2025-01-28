import tkinter as tk
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from display_utils import display_graph_result
import random
from typing import Dict, List, Tuple, Optional

class Graph:
    def __init__(self, vertices: int):
        self.V = vertices
        self.edges: List[Tuple[int, int, float]] = []
        self.graph = nx.DiGraph()
        
    def generate_random_graph(self, edge_density: float = 0.3):
        
        # First ensure the graph is connected by creating a random tree
        vertices = list(range(self.V))
        connected = [0]  # Start with vertex 0
        unconnected = vertices[1:]
        
        while unconnected:
            v1 = random.choice(connected)
            v2 = random.choice(unconnected)
            weight = random.randint(1, 100)
            self.add_edge(v1, v2, weight)
            unconnected.remove(v2)
            connected.append(v2)
        
        # Add additional random edges based on edge density
        for i in range(self.V):
            for j in range(self.V):
                if i != j and random.random() < edge_density:
                    if not any(e[0] == i and e[1] == j for e in self.edges):
                        weight = random.randint(1, 100)
                        self.add_edge(i, j, weight)
    
    def add_edge(self, u: int, v: int, w: float):
        
        self.edges.append((u, v, w))
        self.graph.add_edge(u, v, weight=w)
    
    def bellman_ford(self, src: int) -> Tuple[Optional[Dict[int, float]], Optional[Dict[int, int]], bool, List[Tuple[int, int]]]:
        
        distances = {i: float('inf') for i in range(self.V)}
        distances[src] = 0
        predecessors = {i: None for i in range(self.V)}
        
        # Relax edges |V| - 1 times
        for _ in range(self.V - 1):
            for u, v, w in self.edges:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    predecessors[v] = u
        
        # Check for negative cycles
        for u, v, w in self.edges:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                return None, None, True, []
        
        # Collect all edges that are part of shortest paths
        shortest_path_edges = []
        for v in range(self.V):
            if predecessors[v] is not None:
                shortest_path_edges.append((predecessors[v], v))
        
        return distances, predecessors, False, shortest_path_edges

    def visualize(self, src: int, shortest_path_edges: List[Tuple[int, int]], distances: Dict[int, float]):
        
        plt.figure(figsize=(12, 8))
        
        # Create layout for the graph
        pos = nx.spring_layout(self.graph, k=1, iterations=50)
        
        # Draw the base graph
        nx.draw_networkx_nodes(self.graph, pos, node_color='lightblue', 
                             node_size=500)
        
        # Highlight source node
        nx.draw_networkx_nodes(self.graph, pos, nodelist=[src],
                             node_color='lightgreen', node_size=500)
        
        # Draw edges
        edge_colors = []
        edge_widths = []
        for u, v in self.graph.edges():
            if (u, v) in shortest_path_edges:
                edge_colors.append('red')
                edge_widths.append(2.0)
            else:
                edge_colors.append('black')
                edge_widths.append(1.0)
        
        nx.draw_networkx_edges(self.graph, pos, edge_color=edge_colors, 
                             width=edge_widths, arrows=True)
        
        # Add edge labels
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels)
        
        # Add node labels with distances
        node_labels = {node: f'v{node}\nd={distances[node]:.1f}' 
                      for node in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, node_labels)
        
        plt.title("Shortest Paths from Source (Red edges show shortest paths)")
        plt.axis('off')
        plt.show()

def run_bellman_ford(frame, vertices, source=0):
    try:
        # Create a graph and generate a random graph
        g = Graph(vertices)
        g.generate_random_graph(edge_density=0.3)
        
        # Run Bellman-Ford from the specified source
        distances, predecessors, has_negative_cycle, shortest_path_edges = g.bellman_ford(source)
        
        if has_negative_cycle:
            messagebox.showwarning("Warning", "Graph contains a negative cycle!")
            return
        
        # Visualize the graph with shortest paths
        g.visualize(source, shortest_path_edges, distances)
        
        # Prepare result text for display
        result_text = f"Bellman-Ford Shortest Paths from vertex {source}\n\n"
        for target in range(g.V):
            if target != source:
                path = []
                current = target
                while current is not None:
                    path.append(current)
                    current = predecessors[current]
                path.reverse()
                result_text += f"To vertex {target}: Distance = {distances[target]}, Path = {' -> '.join(map(str, path))}\n"
        
        # Display the result in the GUI
        display_graph_result(frame, None, result_text)  # No figure to display, just text
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Error in Bellman-Ford algorithm: {str(e)}")

# Example usage
def main():
    # Create a graph with 5 vertices
    g = Graph(5)
    
    # Add edges (source, destination, weight)
    g.add_edge(0, 1, 4)
    g.add_edge(0, 2, 2)
    g.add_edge(1, 2, 3)
    g.add_edge(1, 3, 2)
    g.add_edge(1, 4, 3)
    g.add_edge(2, 1, 1)
    g.add_edge(2, 3, 4)
    g.add_edge(2, 4, 5)
    g.add_edge(4, 3, -5)
    
    # Find shortest paths from vertex 0
    source = 0
    distances, predecessors, has_negative_cycle, shortest_path_edges = g.bellman_ford(source)
    
    if has_negative_cycle:
        print("Graph contains negative weight cycle")
    else:
        print("\nShortest distances from source vertex", source)
        for vertex in range(g.V):
            print(f"Vertex {vertex}: {distances[vertex]}")
            
        print("\nShortest paths from source vertex", source)
        for vertex in range(g.V):
            print(f"\nPath to vertex {vertex}:", end=" ")
            g.print_path(predecessors, source, vertex)

if __name__ == "__main__":
    main() 