import streamlit as st
import pulp
from graphviz import Digraph

# --- DATA ---
toppings = [
    {"name": "Nduja", "cost": 0.50, "sat": 4.8},
    {"name": "Salame", "cost": 2.00, "sat": 8.3},
    {"name": "Parma ham", "cost": 3.00, "sat": 7.2},
    {"name": "Fried eggplant", "cost": 2.00, "sat": 5.2},
    {"name": "Buffalo mozzarella", "cost": 2.00, "sat": 5.0},
    {"name": "Ricotta", "cost": 1.00, "sat": 4.2},
    {"name": "Pancetta", "cost": 2.00, "sat": 4.2},
    {"name": "Zucchini", "cost": 1.00, "sat": 3.5},
    {"name": "Burrata", "cost": 3.00, "sat": 4.7},
    {"name": "Gorgonzola", "cost": 1.50, "sat": 3.1},
]
BUDGET = 7.00

# --- NAVIGATION ---
st.sidebar.title("🍕 Navigation")
mode = st.sidebar.radio("Go to:", ["1. Play the Game", "2. Understand the Logic", "3. View the Tree"])

# --- 1. PLAY THE GAME ---
if mode == "1. Play the Game":
    st.header("🎮 Beat the Algorithm")
    st.write(f"Pick toppings to maximize satisfaction without exceeding **${BUDGET}**.")
    
    col1, col2 = st.columns([1, 1])
    user_sat, user_cost = 0, 0
    
    with col1:
        st.subheader("Menu")
        for i, t in enumerate(toppings):
            if st.checkbox(f"{t['name']} (${t['cost']})", key=f"play_{i}"):
                user_sat += t['sat']
                user_cost += t['cost']

    with col2:
        st.subheader("Your Score")
        st.metric("Total Satisfaction", round(user_sat, 2))
        st.metric("Total Cost", f"${user_cost:.2f}")
        
        if user_cost > BUDGET:
            st.error("🚨 Over Budget!")
        elif user_cost > 0:
            st.success("Great Pizza!")

# --- 2. UNDERSTAND THE THINGS ---
elif mode == "2. Understand the Logic":
    st.header("🧠 How Branch & Bound Works")
    st.write("""
    Branch and Bound (B&B) is used because we cannot buy **half** of a topping. 
    It follows three main steps:
    """)
    
    st.info("**Step 1: Relaxation** - We solve the problem as if we COULD buy decimals. This gives us an 'Upper Bound'.")
    st.info("**Step 2: Branching** - We split the problem: Topping A = 0 vs Topping A = 1.")
    st.info("**Step 3: Bounding** - If a branch has a lower potential score than a solution we already found, we 'prune' it (stop looking).")

# --- 3. VIEW THE DRAW ---
elif mode == "3. View the Tree":
    st.header("🌳 The Decision Tree")
    st.write("This visualizes the 'Binary' choices (Requirement 2) vs the 'Continuous' choices (Requirement 3).")
    
    dot = Digraph()
    dot.node('A', f'Root Node\nBudget: ${BUDGET}\nMax Sat (Cont): 25.1')
    dot.node('B', 'Nduja = 1\n(Best Efficiency)')
    dot.node('C', 'Nduja = 0\n(Lower Bound)')
    dot.edge('A', 'B', label='Yes')
    dot.edge('A', 'C', label='No')
    dot.node('D', 'Salame = 1\nSat: 13.1')
    dot.node('E', 'Salame = 0\nSat: 4.8')
    dot.edge('B', 'D')
    dot.edge('B', 'E')
    
    st.graphviz_chart(dot)
    st.caption("Simplified visualization of the B&B search path.")
