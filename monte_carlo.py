import random
import time

def simulate_variance():
    # --- CONFIGURATION (The "SG 553 | Tornado" Scenario) ---
    STARTING_BANKROLL = 300.00  # Your total budget
    COST_PER_TRY = 7.50         # Cost of 1 Anchor + 9 Fillers
    WIN_PAYOUT = 85.00          # Value of the Target Skin (after 15% tax)
    WIN_CHANCE = 0.10           # 10% probability
    TOTAL_ATTEMPTS = 30         # How many times we pull the lever
    # --------------------------------------------------------

    current_balance = STARTING_BANKROLL
    wins = 0
    losses = 0
    
    print(f"\n--- SIMULATION STARTED ---")
    print(f"Bankroll: ${STARTING_BANKROLL}")
    print(f"Goal: Survive {TOTAL_ATTEMPTS} attempts")
    print("-" * 50)
    
    # ASCII Chart storage
    history = [current_balance]

    for i in range(1, TOTAL_ATTEMPTS + 1):
        # The Moment of Truth (RNG)
        is_win = random.random() < WIN_CHANCE
        
        # Deduct cost immediately (You pay to play)
        current_balance -= COST_PER_TRY
        
        if is_win:
            wins += 1
            current_balance += WIN_PAYOUT
            result = "WIN!  [++++++++++++]"
            color_code = "\033[92m" # Green Text
        else:
            losses += 1
            result = "LOSS  [-]"
            color_code = "\033[91m" # Red Text
            
        reset_color = "\033[0m"
        
        # Visualizing the "Heartbeat"
        # We print the result and the new bank balance
        print(f"Try #{i:02d} | {color_code}{result}{reset_color} | Balance: ${current_balance:.2f}")
        
        history.append(current_balance)
        time.sleep(0.05) # Tiny pause for dramatic effect

    # --- FINAL STATS ---
    net_profit = current_balance - STARTING_BANKROLL
    roi = (net_profit / STARTING_BANKROLL) * 100
    
    print("-" * 50)
    print(f"--- RESULTS SUMMARY ---")
    print(f"Wins: {wins} | Losses: {losses}")
    print(f"Win Rate: {(wins/TOTAL_ATTEMPTS)*100:.1f}% (Expected: 10.0%)")
    print(f"Final Balance: ${current_balance:.2f}")
    
    if net_profit > 0:
        print(f"Total Profit: \033[92m+${net_profit:.2f}\033[0m")
    else:
        print(f"Total Profit: \033[91m${net_profit:.2f}\033[0m")
        
    print(f"Return on Investment (ROI): {roi:.1f}%")
    
    # The "Risk of Ruin" Check
    if min(history) < COST_PER_TRY:
        print("\n\033[93mWARNING: At one point, you went broke and couldn't afford the next try!\033[0m")
    elif min(history) < (STARTING_BANKROLL * 0.5):
         print("\nNOTE: You experienced a significant drawdown (lost >50% of bankroll).")

if __name__ == "__main__":
    simulate_variance()