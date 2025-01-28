import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from display_utils import display_graph_result, display_matrix_result

def run_north_west_corner(frame, vertices, supply=None, demand=None):
    try:
        if supply is None or demand is None:
            # Generate random supply and demand if not provided
            supply = np.random.randint(10, 50, size=vertices)
            demand = np.random.randint(10, 50, size=vertices)
            # Adjust to make balanced
            diff = sum(supply) - sum(demand)
            if diff > 0:
                demand[-1] += diff
            elif diff < 0:
                supply[-1] -= diff
        
        # Generate random costs
        costs = np.random.randint(1, 20, size=(len(supply), len(demand)))
        
        # Implement North-West Corner method
        supply_left = supply.copy()
        demand_left = demand.copy()
        solution = np.zeros((len(supply), len(demand)))
        
        i, j = 0, 0
        while i < len(supply) and j < len(demand):
            quantity = min(supply_left[i], demand_left[j])
            solution[i, j] = quantity
            supply_left[i] -= quantity
            demand_left[j] -= quantity
            
            if supply_left[i] == 0:
                i += 1
            if demand_left[j] == 0:
                j += 1
        
        # Calculate total cost
        total_cost = np.sum(solution * costs)
        
        # Create visualization
        plt.clf()
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Plot solution matrix
        im = ax.imshow(solution, cmap='YlOrRd')
        
        # Add text annotations
        for i in range(len(supply)):
            for j in range(len(demand)):
                text = ax.text(j, i, f'{solution[i, j]:.0f}\n({costs[i, j]})',
                             ha='center', va='center')
        
        ax.set_title('North-West Corner Solution\n(Allocation\nCost)')
        plt.colorbar(im)
        
        # Prepare result text
        result_text = "North-West Corner Method Solution\n\n"
        result_text += f"Total Cost: {total_cost}\n\n"
        result_text += "Supply: " + ", ".join(map(str, supply)) + "\n"
        result_text += "Demand: " + ", ".join(map(str, demand)) + "\n"
        
        # Display the result
        display_matrix_result(frame, solution, supply, demand, result_text)
        display_graph_result(frame, fig, result_text)
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Error in North-West Corner method: {str(e)}") 