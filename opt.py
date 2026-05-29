import pulp
import streamlit as st
from graphviz import Digraph

# --- LOGIC: The Branch and Bound Solver ---
class BBNode:
    def __init__(self, items, capacity, constraints=None, parent_id=None, node_id=0):
        self.items = items  # List of (name, value, cost)
        self.capacity = capacity
        self.constraints = constraints or {}
        self.id = str(node_id)
        self.parent_id = parent_id
        self.status = ""
        self.lp_value = 0
        self.vars = {}

    def solve(self):
        # Create a Linear Program
        prob = pulp.LpProblem(f"Node_{self.id}", pulp.LpMaximize)
        
        # Variables: Continuous [0, 1] for relaxation
        vars = {i: pulp.LpVariable(f"x_{i}", 0, 1) for i in range(len(self.items))}
        
        # Objective: Maximize 'Yumminess'
        prob += pulp.lpSum([vars[i] * self.items[i][1] for i in range(len(self.items))])
        
        # Constraint: Budget/Capacity
        prob += pulp.lpSum([vars[i] * self.items[i][2] for i in range(len(self.items))]) <= self.capacity
        
        # Apply branching constraints (the 'Branch' part)
        for i, val in self.constraints.items():
            prob += (vars[i] == val)

        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        
        if pulp.LpStatus[prob.status] == 'Infeasible':
            self.status = "Infeasible"
            return None
        
        self.lp_value = pulp.value(prob.objective)
        self.vars = {i: pulp.value(vars[i]) for i in range(len(self.items))}
        return self.lp_value

# --- UI: Streamlit Interface ---
st.title("🍕 Pizza Optimizer: Branch & Bound Visualizer")

# Input Data
pizza_data = [
    ("Pepperoni", 10, 15), # (Name, Value/Yum, Cost)
    ("Mushroom", 8, 10),
    ("Extra Cheese", 5, 7)
]
budget = st.sidebar.slider("Budget", 5, 50, 20)

# Implementation of the Tree logic would go here...
# (You can use a recursive loop to build a 'dot' graph for visualization)
