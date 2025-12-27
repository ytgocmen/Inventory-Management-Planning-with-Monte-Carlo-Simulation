import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class InventorySimulation:
    def __init__(self, s, Q, L, lambda_demand, h, p, K, initial_stock, days):
        """
        Initializes the simulation with parameters defined in the report (Section 2.2).
        
        Parameters:
        -----------
        s : int
            Reorder Point. An order is placed if Inventory Position <= s.
        Q : int
            Order Quantity. The fixed amount ordered.
        L : int
            Lead Time (days). Time delay between placing an order and receiving it.
        lambda_demand : float
            Average daily demand (Poisson distribution parameter).
        h : float
            Holding cost per unit per day.
        p : float
            Shortage (penalty) cost per unit per day (for backlog).
        K : float
            Fixed ordering cost per order.
        initial_stock : int
            Starting inventory level.
        days : int
            Duration of the simulation in days.
        """
        self.s = s
        self.Q = Q
        self.L = L
        self.lambda_demand = lambda_demand
        self.h = h
        self.p = p
        self.K = K
        self.initial_stock = initial_stock
        self.days = days
        
        # DataFrame to store daily results
        self.results = None

    def run(self):
        """
        Executes the simulation steps as defined in Section 3.1:
        1. Process Delivery
        2. Serve Backlog
        3. Generate & Meet Demand
        4. Reorder Decision ((s, Q) Policy)
        5. Calculate Costs
        """
        
        # Initialization [cite: 166]
        I = self.initial_stock # On-Hand Inventory
        B = 0  # Backlog (Accumulated unmet demand)
        P = 0  # Pipeline (On-Order Quantity)
        
        # List to track incoming orders: (Delivery Day, Quantity)
        incoming_orders = [] 
        
        records = []
        
        total_holding_cost = 0
        total_shortage_cost = 0
        total_order_cost = 0
        stockout_days = 0
        
        for t in range(1, self.days + 1):
            # --- Step 1: Delivery Control [cite: 150] ---
            # Check if any order is scheduled to arrive today
            arrived_qty = sum(qty for day, qty in incoming_orders if day == t)
            if arrived_qty > 0:
                I += arrived_qty
                P -= arrived_qty
                # Remove arrived orders from the list
                incoming_orders = [order for order in incoming_orders if order[0] != t]
            
            # --- Step 2: Backlog Service [cite: 151] ---
            # If we have stock and a backlog, fulfill the backlog first
            if I > 0 and B > 0:
                fulfilled_backlog = min(I, B)
                I -= fulfilled_backlog
                B -= fulfilled_backlog
            
            # --- Step 3: Generate Demand [cite: 139] ---
            # Using Poisson distribution to model random daily demand
            D_t = np.random.poisson(self.lambda_demand)
            
            # --- Step 4: Meet Daily Demand [cite: 153-155] ---
            fulfilled_demand = 0
            if I >= D_t:
                I -= D_t
                fulfilled_demand = D_t
            else:
                # Stockout situation
                fulfilled_demand = I
                shortage = D_t - I
                I = 0
                B += shortage # Add unmet demand to backlog
                stockout_days += 1
            
            # --- Step 5: Reorder Decision ((s, Q) Policy) [cite: 156] ---
            # Calculate Inventory Position = On-Hand + Pipeline - Backlog
            inventory_position = I + P - B
            order_placed = False
            
            # Place order if Position <= s AND no order is currently in the pipeline
            # (Note: Assuming single open order constraint for simplicity as per Section 3.3)
            if inventory_position <= self.s and P == 0:
                order_placed = True
                P += self.Q
                delivery_day = t + self.L
                incoming_orders.append((delivery_day, self.Q))
                total_order_cost += self.K
                
            # --- Step 6: Cost Calculation [cite: 159] ---
            daily_holding_cost = I * self.h
            daily_shortage_cost = B * self.p
            
            total_holding_cost += daily_holding_cost
            total_shortage_cost += daily_shortage_cost
            
            # Record daily metrics
            records.append({
                'Day': t,
                'Inventory': I,
                'Backlog': B,
                'Demand': D_t,
                'Order_Placed': 1 if order_placed else 0,
                'Daily_Cost': daily_holding_cost + daily_shortage_cost + (self.K if order_placed else 0)
            })
            
        self.results = pd.DataFrame(records)
        return self.results

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Parameters based on the "Base Scenario" in the report [cite: 161]
    # s=20, Q=50, L=5, Poisson(5), h=1, p=10, K=50
    sim = InventorySimulation(
        s=20, 
        Q=50, 
        L=5, 
        lambda_demand=5, 
        h=1, 
        p=10, 
        K=50, 
        initial_stock=50, 
        days=365
    )
    
    df_results = sim.run()

    # --- VISUALIZATION ---
    # Set the style for a professional look
    sns.set_style("whitegrid")
    plt.figure(figsize=(14, 6))

    # Plot Inventory Levels
    plt.plot(df_results['Day'], df_results['Inventory'], label='On-Hand Inventory', color='#1f77b4', linewidth=1.5)
    
    # Plot Reorder Point
    plt.axhline(y=20, color='r', linestyle='--', label='Reorder Point (s=20)', alpha=0.7)
    
    # Highlight Backlog/Stockouts
    plt.fill_between(df_results['Day'], 0, -df_results['Backlog'], color='orange', alpha=0.3, label='Backlog (Negative Stock)')

    plt.title('Monte Carlo Simulation: Inventory Levels & Backlog (365 Days)', fontsize=14, fontweight='bold')
    plt.xlabel('Simulation Day', fontsize=12)
    plt.ylabel('Units', fontsize=12)
    plt.legend(loc='upper right')
    plt.tight_layout()

    # Save the plot for the portfolio
    plt.savefig('inventory_simulation_output.png', dpi=300)
    plt.show()

    # --- KPI REPORTING ---
    total_cost = df_results['Daily_Cost'].sum()
    stockout_days = df_results[df_results['Backlog'] > 0].shape[0]
    service_level = 1 - (stockout_days / 365)

    print(f"--- SIMULATION RESULTS ---")
    print(f"Total Annual Cost : €{total_cost:,.2f}")
    print(f"Service Level     : {service_level*100:.2f}%")
    print(f"Stockout Days     : {stockout_days} days")
    print(f"Max Backlog       : {df_results['Backlog'].max()} units")