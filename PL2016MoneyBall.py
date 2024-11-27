#!/usr/bin/env python3
import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, PULP_CBC_CMD
import sys

# Static dataset file path
DATASET_FILE = "PlayerDataSet.csv"

def load_dataset():
    """
    Load the dataset from the CSV file.
    """
    try:
        data = pd.read_csv(DATASET_FILE)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{DATASET_FILE}' was not found.")
        sys.exit()

def get_objective_criteria(headers):
    """
    Get user input for objective function criteria.
    """
    print("\nAvailable criteria (you can select multiple):")
    print(", ".join(headers))
    print("Enter criteria in the format: '<header>=<weight>', separated by commas (e.g., goals=5,fouls=-3):")
    while True:
        criteria_input = input("Enter criteria: ")
        try:
            criteria = {}
            for item in criteria_input.split(","):
                key, value = item.split("=")
                key = key.strip()
                value = float(value.strip())
                if key not in headers:
                    raise ValueError(f"Invalid header: '{key}'")
                criteria[key] = value
            if not criteria:
                raise ValueError("No criteria provided.")
            return criteria
        except Exception as e:
            print(f"Input error: {e}. Please try again.")

def get_constraints(headers):
    """
    Get user input for constraints.
    """
    print("\nAvailable constraints (you can specify multiple):")
    print(", ".join(headers))
    print("Enter constraints in the format: '<header>=<value>', '<header><=value>', '<header>>=value', separated by commas (e.g., fouls<=10,goals>=5):")
    constraints = []
    while True:
        constraints_input = input("Enter constraints: ")
        try:
            for constraint in constraints_input.split(","):
                constraint = constraint.strip()
                if "<=" in constraint:
                    header, value = constraint.split("<=")
                    ctype = "max"
                elif ">=" in constraint:
                    header, value = constraint.split(">=")
                    ctype = "min"
                elif "=" in constraint:
                    header, value = constraint.split("=")
                    ctype = "equal"
                else:
                    raise ValueError(f"Invalid constraint format: '{constraint}'")
                header = header.strip()
                value = float(value.strip())
                if header not in headers:
                    raise ValueError(f"Invalid header: '{header}'")
                constraints.append({"type": ctype, "header": header, "value": value})
            if not constraints:
                raise ValueError("No constraints provided.")
            return constraints
        except Exception as e:
            print(f"Input error: {e}. Please try again.")

def solve_optimization(data, criteria, constraints):
    """
    Build and solve the optimization problem.
    """
    # Define decision variables
    n = len(data)
    x = LpVariable.dicts("Select", range(n), cat="Binary")

    # Define the problem
    model = LpProblem("Dynamic_Team_Selection", LpMaximize)

    # Add objective function
    model += lpSum(
        criteria[header] * data.loc[i, header] * x[i]
        for i in range(n) for header in criteria
    ), "Total_Score"

    # Add constraints with unique names
    for idx, constraint in enumerate(constraints):
        header = constraint["header"]
        value = constraint["value"]
        if constraint["type"] == "max":
            model += lpSum(data.loc[i, header] * x[i] for i in range(n)) <= value, f"Max_{header}_{idx}"
        elif constraint["type"] == "min":
            model += lpSum(data.loc[i, header] * x[i] for i in range(n)) >= value, f"Min_{header}_{idx}"
        elif constraint["type"] == "equal":
            model += lpSum(data.loc[i, header] * x[i] for i in range(n)) == value, f"Equal_{header}_{idx}"

    # Solve the problem with solver output suppressed
    solver = PULP_CBC_CMD(msg=False)  # Suppress solver messages
    status = model.solve(solver)

    # Check if a feasible solution was found
    if LpStatus[status] != 'Optimal':
        print("No optimal solution found. Please adjust your criteria and constraints.")
        sys.exit()

    # Get selected players and calculate their individual scores
    selected_players = []
    for i in range(n):
        if x[i].varValue == 1:
            player_name = data.loc[i, "name"]
            # Calculate individual score
            individual_score = sum(criteria[header] * data.loc[i, header] for header in criteria)
            selected_players.append((player_name, individual_score))

    # Sort players based on their individual scores in descending order
    selected_players.sort(key=lambda x: x[1], reverse=True)

    return selected_players

def main():
    # Load dataset
    data = load_dataset()

    # Exclude non-numeric columns
    non_numeric_cols = ['id', 'dob', 'name', 'nationality']
    headers = [col for col in data.columns if col not in non_numeric_cols]

    # Ensure only numeric columns are included
    numeric_headers = data[headers].select_dtypes(include=[float, int]).columns.tolist()

    # Get user inputs
    criteria = get_objective_criteria(numeric_headers)
    constraints = get_constraints(numeric_headers)

    # Combine criteria and constraint headers
    relevant_columns = list(set(list(criteria.keys()) + [constraint['header'] for constraint in constraints]))

    # Check for NaN values and handle them by dropping players with missing data
    initial_player_count = len(data)
    data = data.dropna(subset=relevant_columns).reset_index(drop=True)
    final_player_count = len(data)

    if final_player_count < initial_player_count:
        print(f"\n{initial_player_count - final_player_count} players were excluded due to missing data in selected criteria and constraints.")
        if final_player_count == 0:
            print("No players left after excluding those with missing data. Please adjust your criteria and constraints.")
            sys.exit()

    # Solve the problem
    selected_players = solve_optimization(data, criteria, constraints)

    # Output results
    print("\nSelected Players (ordered by individual scores):")
    for player, score in selected_players:
        print(f"{player}: {score}")

if __name__ == "__main__":
    main()
