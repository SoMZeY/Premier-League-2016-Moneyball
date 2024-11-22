import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import sys

# Static dataset file path
DATASET_FILE = "PlayerDataSet.csv"

# Display help for headers
def display_help():
    data = pd.read_csv(DATASET_FILE)
    headers = data.columns.tolist()
    print("Available Headers for Criteria and Constraints:")
    print(", ".join(headers))
    print("\nExamples:")
    print("Criteria: goals=5,fouls=-3,interceptions=2")
    print("Constraints: team_size=11,fouls<=10,defenders>=4")
    print("\nRun the program with './program run' to start optimization.")
    sys.exit()

# Load the dataset
def load_dataset():
    return pd.read_csv(DATASET_FILE)

# Get user input for objective function
def get_objective_criteria(headers):
    print("Available criteria (you can select multiple):")
    print(", ".join(headers))
    print("Enter criteria in the format: '<header>=<weight>', separated by commas (e.g., goals=5,fouls=-3):")
    criteria_input = input("Enter criteria: ")
    criteria = {item.split("=")[0]: float(item.split("=")[1]) for item in criteria_input.split(",")}
    return criteria

# Get user input for constraints
def get_constraints(headers):
    print("Available constraints (you can specify multiple):")
    print(", ".join(headers))
    print("Enter constraints in the format: '<header>=<value>' or '<header><=value>' separated by commas (e.g., fouls<=10,team_size=11):")
    constraints_input = input("Enter constraints: ")
    constraints = []
    for constraint in constraints_input.split(","):
        if "<=" in constraint:
            header, value = constraint.split("<=")
            constraints.append({"type": "max", "header": header.strip(), "value": float(value.strip())})
        elif ">=" in constraint:
            header, value = constraint.split(">=")
            constraints.append({"type": "min", "header": header.strip(), "value": float(value.strip())})
        elif "=" in constraint:
            header, value = constraint.split("=")
            constraints.append({"type": "equal", "header": header.strip(), "value": float(value.strip())})
    return constraints

# Build and solve the optimization problem
def solve_optimization(data, criteria, constraints):
    # Define decision variables
    n = len(data)
    x = {i: LpVariable(f"x_{i}", cat="Binary") for i in range(n)}

    # Define the problem
    model = LpProblem("Dynamic_Team_Selection", LpMaximize)

    # Add objective function
    model += lpSum(
        lpSum(criteria[header] * data.iloc[i][header] * x[i] for header in criteria) for i in range(n)
    )

    # Add constraints
    for constraint in constraints:
        if constraint["type"] == "max":
            model += lpSum(data.iloc[i][constraint["header"]] * x[i] for i in range(n)) <= constraint["value"]
        elif constraint["type"] == "min":
            model += lpSum(data.iloc[i][constraint["header"]] * x[i] for i in range(n)) >= constraint["value"]
        elif constraint["type"] == "equal":
            model += lpSum(data.iloc[i][constraint["header"]] * x[i] for i in range(n)) == constraint["value"]

    # Solve the problem
    model.solve()

    # Get selected players
    selected_players = [data.iloc[i]["name"] for i in range(n) if x[i].value() == 1]
    return selected_players

# Main function
def main():
    if len(sys.argv) < 2:
        print("Usage: ./program <command>")
        print("Commands:")
        print("  help   - Display available headers and examples")
        print("  run    - Run the optimization program")
        sys.exit()

    command = sys.argv[1].lower()
    if command == "help":
        display_help()
    elif command == "run":
        # Load dataset
        data = load_dataset()

        # Validate and clean dataset headers
        headers = data.columns.tolist()
        headers.remove("id")
        headers.remove("dob")
        headers.remove("name")
        headers.remove("nationality")  # Remove non-numeric columns for optimization

        # Get user inputs
        criteria = get_objective_criteria(headers)
        constraints = get_constraints(headers)

        # Solve the problem
        selected_players = solve_optimization(data, criteria, constraints)

        # Output results
        print("Selected Players:")
        print(selected_players)
    else:
        print("Unknown command. Use './program help' for guidance.")
        sys.exit()

# Entry point
if __name__ == "__main__":
    main()
