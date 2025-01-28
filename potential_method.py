import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from display_utils import display_graph_result, display_matrix_result

def run_potential_method(frame, vertices, supply=None, demand=None):
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
        
        def get_initial_solution():
            """Get initial feasible solution using North-West Corner method"""
            solution = np.zeros((len(supply), len(demand)))
            supply_left = supply.copy()
            demand_left = demand.copy()
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
                    
            return solution

        def calculate_potentials(solution, costs):
            """Calculate row (u) and column (v) potentials"""
            m, n = solution.shape
            u = np.zeros(m)  # Row potentials
            v = np.zeros(n)  # Column potentials
            
            # Create mask for basic variables (cells with allocation)
            basic_mask = solution > 0
            
            # Set u[0] = 0 as reference
            assigned = np.zeros(m + n)
            assigned[0] = 1
            
            # Iteratively find potentials
            while not np.all(assigned):
                for i in range(m):
                    for j in range(n):
                        if basic_mask[i, j]:
                            if assigned[i] and not assigned[m + j]:
                                v[j] = costs[i, j] - u[i]
                                assigned[m + j] = 1
                            elif not assigned[i] and assigned[m + j]:
                                u[i] = costs[i, j] - v[j]
                                assigned[i] = 1
                                
            return u, v

        def calculate_reduced_costs(u, v, costs):
            """Calculate reduced costs for non-basic variables"""
            return costs - (u.reshape(-1, 1) + v)

        # Get initial solution
        solution = get_initial_solution()
        iteration = 0
        max_iterations = 100
        improvement_found = True
        
        while improvement_found and iteration < max_iterations:
            # Calculate potentials
            u, v = calculate_potentials(solution, costs)
            
            # Calculate reduced costs
            reduced_costs = calculate_reduced_costs(u, v, costs)
            
            # Find entering variable (most negative reduced cost)
            non_basic_mask = solution == 0
            min_reduced_cost = np.inf
            entering_cell = None
            
            for i in range(len(supply)):
                for j in range(len(demand)):
                    if non_basic_mask[i, j] and reduced_costs[i, j] < min_reduced_cost:
                        min_reduced_cost = reduced_costs[i, j]
                        entering_cell = (i, j)
            
            # If no negative reduced costs, solution is optimal
            if min_reduced_cost >= -1e-10:  # Using small threshold for numerical stability
                improvement_found = False
                continue
            
            # Find feasible allocation for entering variable
            i, j = entering_cell
            max_allocation = min(supply[i] - np.sum(solution[i, :]),
                               demand[j] - np.sum(solution[:, j]))
            
            if max_allocation > 0:
                solution[i, j] = max_allocation
            
            iteration += 1

        # Calculate total cost
        total_cost = np.sum(solution * costs)
        
        # Calculate final potentials for display
        final_u, final_v = calculate_potentials(solution, costs)
        
        # Create visualization
        plt.clf()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot solution matrix
        im1 = ax1.imshow(solution, cmap='YlOrRd')
        ax1.set_title('Allocation Matrix')
        plt.colorbar(im1, ax=ax1)
        
        # Add allocation and cost annotations
        for i in range(len(supply)):
            for j in range(len(demand)):
                text = ax1.text(j, i, f'{solution[i, j]:.0f}\n({costs[i, j]})',
                              ha='center', va='center')
        
        # Plot reduced costs
        reduced_costs = calculate_reduced_costs(final_u, final_v, costs)
        im2 = ax2.imshow(reduced_costs, cmap='RdYlBu')
        ax2.set_title('Reduced Costs Matrix')
        plt.colorbar(im2, ax=ax2)
        
        # Add reduced costs annotations
        for i in range(len(supply)):
            for j in range(len(demand)):
                text = ax2.text(j, i, f'{reduced_costs[i, j]:.2f}',
                              ha='center', va='center')

        # Prepare result text
        result_text = "Potential Method (Méthode du Potentiel) Solution\n\n"
        result_text += f"Total Cost: {total_cost}\n"
        result_text += f"Iterations: {iteration}\n\n"
        result_text += "Supply: " + ", ".join(map(str, supply)) + "\n"
        result_text += "Demand: " + ", ".join(map(str, demand)) + "\n\n"
        result_text += "Row Potentials (u): " + ", ".join(f"{x:.2f}" for x in final_u) + "\n"
        result_text += "Column Potentials (v): " + ", ".join(f"{x:.2f}" for x in final_v) + "\n"

        # Display the result
        display_matrix_result(frame, solution, supply, demand, result_text)
        display_graph_result(frame, fig, result_text)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Error in Potential Method: {str(e)}") 