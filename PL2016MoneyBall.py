# Simple Dynamic Team Selection Optimization Program using Linear Programming
# Author: Vladyslav Bordia, Patrick McKeever, Abby Gopal
# Date: November 28th, 2024

# Import necessary libraries
import pandas as pd
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpStatus, PULP_CBC_CMD

def load_dataset():
    """
    Load the dataset from a CSV file.
    Assumes the CSV file is named 'PlayerDataSet.csv' and is in the same directory as this script.
    Returns a pandas DataFrame.
    """
    try:
        data = pd.read_csv('PlayerDataSet.csv')
        return data
    except FileNotFoundError:
        print("Error: The file 'PlayerDataSet.csv' was not found.")
        exit()

def main():
    # Load the dataset
    data = load_dataset()

    # Exclude non-numeric columns except 'name'
    non_numeric_cols = ['id', 'dob', 'name', 'nationality']
    headers = [col for col in data.columns if col not in non_numeric_cols]

    # Ensure only numeric columns are included
    numeric_headers = data[headers].select_dtypes(include=[float, int]).columns.tolist()

    # Prompt the user to choose a metric to maximize
    print("\nAvailable performance metrics to maximize:")
    print(", ".join(numeric_headers))
    while True:
        maximize_metric = input("Enter the performance metric you want to maximize: ").strip()
        if maximize_metric in numeric_headers:
            break
        else:
            print(f"Invalid metric '{maximize_metric}'. Please choose from the available metrics.")

    # Prompt the user to specify constraints on other metrics
    print("\nYou can specify constraints on other metrics.")
    print("Enter constraints in the format: '<metric> <operator> <value>', one per line.")
    print("Valid operators are '<=', '>=', '=='. Type 'done' when finished.")
    constraints = []
    while True:
        constraint_input = input("Enter a constraint or 'done' to finish: ").strip()
        if constraint_input.lower() == 'done':
            break
        try:
            metric, operator, value = constraint_input.split()
            if metric not in numeric_headers:
                print(f"Invalid metric '{metric}'. Please choose from the available metrics.")
                continue
            if operator not in ['<=', '>=', '==']:
                print(f"Invalid operator '{operator}'. Valid operators are '<=', '>=', '=='.")
                continue
            value = float(value)
            constraints.append((metric, operator, value))
        except ValueError:
            print("Invalid constraint format. Please use the format: '<metric> <operator> <value>'.")

    # Ensure necessary columns are present
    required_columns = ['name', maximize_metric] + [c[0] for c in constraints]
    required_columns = list(set(required_columns))  # Remove duplicates
    for col in required_columns:
        if col not in data.columns:
            print(f"Error: Column '{col}' is missing from the dataset.")
            exit()

    # Drop rows with missing values in the required columns
    data = data.dropna(subset=required_columns)

    # Reset index after dropping rows
    data = data.reset_index(drop=True)

    # Define the number of players to select
    total_players = 11

    # Create a list of player indices
    player_indices = data.index.tolist()

    # Create decision variables
    # x_i represents the fraction of player i selected (between 0 and 1)
    x = LpVariable.dicts('x', player_indices, lowBound=0, upBound=1)

    # Initialize the LP problem
    prob = LpProblem("Dynamic_Team_Selection_Problem", LpMaximize)

    # Define the objective function: Maximize the selected performance metric
    prob += lpSum([x[i] * data.loc[i, maximize_metric] for i in player_indices]), f"Total_{maximize_metric}"

    # Add constraint: Total number of players selected equals total_players
    prob += lpSum([x[i] for i in player_indices]) == total_players, "Total_Players"

    # Add user-defined constraints
    for idx, (metric, operator, value) in enumerate(constraints):
        if operator == '<=':
            prob += lpSum([x[i] * data.loc[i, metric] for i in player_indices]) <= value, f"Constraint_{idx}_{metric}"
        elif operator == '>=':
            prob += lpSum([x[i] * data.loc[i, metric] for i in player_indices]) >= value, f"Constraint_{idx}_{metric}"
        elif operator == '==':
            prob += lpSum([x[i] * data.loc[i, metric] for i in player_indices]) == value, f"Constraint_{idx}_{metric}"

    # Solve the problem using the default solver (CBC)
    prob.solve(PULP_CBC_CMD(msg=False))

    # Check the status of the solution
    if prob.status != 1:
        print("No optimal solution found.")
        exit()

    # Retrieve the decision variable values and store them with player data
    player_selection = []
    for i in player_indices:
        xi = x[i].varValue  # Get the value of the decision variable x_i
        if xi is not None:
            player_selection.append({
                'index': i,
                'name': data.loc[i, 'name'],
                maximize_metric: data.loc[i, maximize_metric],
                'selection_value': xi
            })

    # Sort players by selection value in descending order
    player_selection.sort(key=lambda k: k['selection_value'], reverse=True)

    # Select the top players based on selection values
    selected_players = player_selection[:total_players]

    # Output the selected players
    print("\nSelected Players:")
    for player in selected_players:
        print(f"Name: {player['name']}, {maximize_metric.capitalize()}: {player[maximize_metric]}, Selection Value: {player['selection_value']:.2f}")

if __name__ == "__main__":
    main()
