# 📦 Inventory Optimization Engine using Monte Carlo Simulation

## 🚀 Project Overview
[cite_start]This project addresses the challenge of managing inventory under uncertain demand and supply conditions[cite: 110]. By simulating a warehouse environment, the model balances holding costs, ordering costs, and stockout risks to determine the optimal inventory policy.

[cite_start]Unlike static calculations, this project uses **Monte Carlo Simulation** to visualize risk and variability, helping decision-makers answer: *"How much safety stock is needed for a 98% Service Level?"*.

## 🧠 The Logic: (s, Q) Policy
[cite_start]The simulation implements a continuous review **(s, Q) policy**:
- **Reorder Point (s):** An order is triggered when Inventory Position ≤ s.
- **Order Quantity (Q):** A fixed quantity Q is ordered.
- [cite_start]**Lead Time (L):** Modeled as a variable time delay between order and delivery[cite: 140].

## 🛠️ Tech Stack & Methodology
- **Language:** Python (NumPy, Pandas)
- [cite_start]**Simulation Type:** Discrete-time (Daily Step) Stochastic Simulation[cite: 143].
- **Key Algorithms:**
  - [cite_start]**Demand Modeling:** Poisson Distribution (to mimic random daily customer orders)[cite: 139].
  - [cite_start]**Backlog Management:** Logic to handle unmet demand as backlog rather than lost sales[cite: 151].
  - [cite_start]**Metric Tracking:** Daily tracking of Inventory (I), Backlog (B), and Pipeline Orders (P)[cite: 133].

## 📊 Key Results & Insights
[cite_start]The simulation provides probabilistic outputs for Strategic and Tactical planning[cite: 200]:
1.  [cite_start]**Service Level Analysis:** Quantifies the probability of stockouts (e.g., 95% vs 99% targets)[cite: 160].
2.  [cite_start]**Cost Optimization:** Identifies the "sweet spot" between holding excessive stock and paying stockout penalties[cite: 183].
3.  [cite_start]**Risk Assessment:** Visualizes "tail risks" (extreme scenarios) that average-based formulas miss[cite: 243].

## 📈 How to Run
1. Clone the repo.
2. Run `main.py` to execute the simulation loop.
3. Adjust parameters `s` (reorder point) and `Q` (quantity) in the config section to test different scenarios.
