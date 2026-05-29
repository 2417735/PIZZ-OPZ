import pulp
import streamlit as st

# 1. Define the Data
toppings = [
    {"name": "Nduja", "cost": 0.50, "satisfaction": 4.8},
    {"name": "Salame", "cost": 2.00, "satisfaction": 8.3},
    {"name": "Parma ham", "cost": 3.00, "satisfaction": 7.2},
    {"name": "Fried eggplant", "cost": 2.00, "satisfaction": 5.2},
    {"name": "Buffalo mozzarella", "cost": 2.00, "satisfaction": 5.0},
    {"name": "Ricotta", "cost": 1.00, "satisfaction": 4.2},
    {"name": "Pancetta", "cost": 2.00, "satisfaction": 4.2},
    {"name": "Zucchini", "cost": 1.00, "satisfaction": 3.5},
    {"name": "Burrata", "cost": 3.00, "satisfaction": 4.7},
    {"name": "Gorgonzola", "cost": 1.50, "satisfaction": 3.1},
]

budget = 7.00

def solve_pizza(is_binary=False):
    # Create the problem
    prob = pulp.LpProblem("Pizza_Optimizer", pulp.LpMaximize)
    
    # Decision Variables
    # Requirement 2 uses cat='Binary'
    # Requirement 3 uses cat='Continuous' with lowBound=0, upBound=1
    cat = pulp.LpBinary if is_binary else pulp.LpContinuous
    choices = pulp.LpVariable.dicts("Topping", range(len(toppings)), 0, 1, cat=cat)
    
    # Objective Function: Maximize Satisfaction
    prob += pulp.lpSum([choices[i] * toppings[i]["satisfaction"] for i in range(len(toppings))])
    
    # Constraint: Cost <= $7.00
    prob += pulp.lpSum([choices[i] * toppings[i]["cost"] for i in range(len(toppings))]) <= budget
    
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    return prob, choices

# --- Execution ---
st.title("Pizza Optimizer B&B Engine")

# Requirement 3: Continuous Solution
st.subheader("Requirement 3: Continuous (Decimal) Relaxation")
prob_cont, choices_cont = solve_pizza(is_binary=False)
st.write(f"Best Satisfaction (Continuous): {pulp.value(prob_cont.objective):.2f}")

# Requirement 2: Binary Solution
st.subheader("Requirement 2: Binary (0/1) Solution")
prob_bin, choices_bin = solve_pizza(is_binary=True)
st.write(f"Best Satisfaction (Binary): {pulp.value(prob_bin.objective):.2f}")

# Display items chosen
for i in range(len(toppings)):
    if pulp.value(choices_bin[i]) > 0:
        st.write(f"✅ {toppings[i]['name']} (Cost: ${toppings[i]['cost']})")
