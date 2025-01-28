import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from display_utils import display_graph_result, display_matrix_result

def run_stepping_stone_method(frame, vertices, supply=None, demand=None):
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
        
        # Get initial solution using Least Cost method
        solution = np.zeros((len(supply), len(demand)))
        supply_left = supply.copy()
        demand_left = demand.copy()
        
        # Initialize with Least Cost method
        while np.any(supply_left > 0) and np.any(demand_left > 0):
            valid_mask = (supply_left.reshape(-1, 1) > 0) & (demand_left > 0)
            costs_masked = np.where(valid_mask, costs, np.inf)
            i, j = np.unravel_index(np.argmin(costs_masked), costs.shape)
            quantity = min(supply_left[i], demand_left[j])
            solution[i, j] = quantity
            supply_left[i] -= quantity
            demand_left[j] -= quantity

        # Implement Stepping Stone method
        max_iterations = 100
        iteration = 0
        improvement_found = True

        while improvement_found and iteration < max_iterations:
            improvement_found = False
            best_improvement = 0
            best_move = None

            # Find empty cells
            empty_cells = np.where(solution == 0)
            
            # Evaluate each empty cell
            for k in range(len(empty_cells[0])):
                i, j = empty_cells[0][k], empty_cells[1][k]
                
                # Simple evaluation of cost improvement
                row_allocated = np.sum(solution[i, :])
                col_allocated = np.sum(solution[:, j])
                
                if row_allocated < supply[i] and col_allocated < demand[j]:
                    potential_improvement = costs[i, j]
                    if potential_improvement < best_improvement:
                        best_improvement = potential_improvement
                        best_move = (i, j)

            # Apply the best move if found
            if best_move is not None:
                i, j = best_move
                max_quantity = min(supply[i] - np.sum(solution[i, :]),
                                 demand[j] - np.sum(solution[:, j]))
                solution[i, j] = max_quantity
                improvement_found = True

            iteration += 1

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
        
        ax.set_title('Stepping Stone Method Solution\n(Allocation\nCost)')
        plt.colorbar(im)

        # Prepare result text
        result_text = "Stepping Stone Method Solution\n\n"
        result_text += f"Total Cost: {total_cost}\n"
        result_text += f"Iterations: {iteration}\n\n"
        result_text += "Supply: " + ", ".join(map(str, supply)) + "\n"
        result_text += "Demand: " + ", ".join(map(str, demand)) + "\n"

        # Display the result
        display_matrix_result(frame, solution, supply, demand, result_text)
        display_graph_result(frame, fig, result_text)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Error in Stepping Stone method: {str(e)}") 