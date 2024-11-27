# Premier League 2016 Moneyball Optimization

## Overview

The **Premier League 2016 Moneyball Optimization** program is a Python script designed to help you select an optimal team of football (soccer) players based on customizable performance criteria and constraints. Utilizing linear programming techniques, it allows you to maximize your team's overall performance according to the specific attributes you value most.

## Features

- **Customizable Criteria**: Define the performance metrics that matter to you (e.g., goals scored, assists, tackles) and assign weights to them.
- **Flexible Constraints**: Set constraints such as minimum appearances, maximum red cards, budget limits, or any other statistical thresholds.
- **Data Cleaning**: Automatically excludes players with missing data in relevant criteria and constraints to ensure accurate optimization.
- **Optimized Team Selection**: Uses linear programming to select the team that maximizes your specified objective function while satisfying all constraints.
- **Ordered Results**: Provides an ordered list of selected players based on their individual contributions to the team's overall score.

## How to Download and Run

### Prerequisites

- **Python 3.x**: Ensure you have Python 3 installed on your system.
- **Required Python Packages**:
  - `pandas`
  - `pulp`

Install the required packages using pip:

```bash
pip install pandas pulp
```
## Mathematical Perspective

### Optimization Model

The program formulates the team selection problem as a **binary linear programming** model, where the objective is to maximize the total team score based on your specified criteria, subject to your constraints.

#### Variables

- **Decision Variables**:

  \[
  x_i = 
  \begin{cases} 
  1 & \text{if player } i \text{ is selected} \\
  0 & \text{otherwise}
  \end{cases}
  \]

#### Objective Function

The goal is to maximize the total team score:

\[
\text{Maximize } Z = \sum_{i=1}^{n} \left( \sum_{k \in K} w_k \cdot s_{ik} \right) x_i
\]

- \( Z \): Total team score
- \( n \): Total number of players
- \( K \): Set of criteria (e.g., goals, assists)
- \( w_k \): Weight assigned to criterion \( k \)
- \( s_{ik} \): Statistic of player \( i \) for criterion \( k \)
- \( x_i \): Decision variable for player \( i \)

#### Constraints

Constraints are linear inequalities or equalities that the selected players must satisfy. They can be formulated as:

- **Minimum Constraints**:

  \[
  \sum_{i=1}^{n} s_{i, \text{constraint}} \cdot x_i \geq \text{Value}
  \]

- **Maximum Constraints**:

  \[
  \sum_{i=1}^{n} s_{i, \text{constraint}} \cdot x_i \leq \text{Value}
  \]

- **Equality Constraints**:

  \[
  \sum_{i=1}^{n} s_{i, \text{constraint}} \cdot x_i = \text{Value}
  \]

#### Data Cleaning

Players with missing data in any of the selected criteria or constraints are excluded from the optimization to maintain data integrity.

### Solution Method

The program uses the **PuLP** library, a linear programming modeler in Python, and employs the **CBC (Coin-or branch and cut)** solver to find the optimal set of players.

- **Feasibility Check**: Ensures that the constraints are satisfiable with the available data.
- **Optimality**: Searches for the solution that maximizes the objective function while satisfying all constraints.

### Individual Player Scores

After solving the optimization problem, the program calculates the individual score for each selected player:

\[
\text{Individual Score}_i = \sum_{k \in K} w_k \cdot s_{ik}
\]

Players are then ordered based on these scores in descending order.
