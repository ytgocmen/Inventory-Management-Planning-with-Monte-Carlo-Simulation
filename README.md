# Inventory Optimization Engine using Monte Carlo Simulation

## Project Overview
This project addresses the challenge of managing inventory under uncertain demand and supply conditions. By simulating a warehouse environment, the model balances holding costs, ordering costs, and the risk of stockouts to determine the optimal inventory policy.

Unlike static calculations, this project uses **Monte Carlo Simulation** to visualize risk and variability, helping decision-makers answer: *"How much safety stock is needed for a 98% Service Level?"*.

## The Logic: (s, Q) Policy
The simulation implements a continuous review **(s, Q) policy**:
- **Reorder Point (s):** An order is triggered when Inventory Position ≤ s.
- **Order Quantity (Q):** A fixed quantity Q is ordered.
- **Lead Time (L):** Modeled as a variable time delay between order and delivery.

## Tech Stack & Methodology
- **Language:** Python (NumPy, Pandas)
- **Simulation Type:** Discrete-time (Daily Step) Stochastic Simulation.
- **Key Algorithms:**
  - **Demand Modeling:** Poisson Distribution (to mimic random daily customer orders).
  - **Backlog Management:** Logic to handle unmet demand as backlog rather than lost sales.
  - **Metric Tracking:** Daily tracking of Inventory (I), Backlog (B), and Pipeline Orders (P).

## Key Results & Insights
The simulation provides probabilistic outputs for Strategic and Tactical planning:
1.  **Service Level Analysis:** Quantifies the probability of stockouts (e.g., 95% vs 99% targets).
2.  **Cost Optimization:** Identifies the "sweet spot" between holding excessive stock and paying stockout penalties.
3.  **Risk Assessment:** Visualizes "tail risks" (extreme scenarios) that average-based formulas miss.

## How to Run
1. Clone the repo.
2. Run `inventory_simulation.py` to execute the simulation loop.
3. Adjust parameters `s` (reorder point) and `Q` (quantity) in the config section to test different scenarios.
