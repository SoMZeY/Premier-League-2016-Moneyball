# Premier League 2016 Moneyball Optimization

## Overview

The **Premier League 2016 Moneyball Optimization** program is a Python script designed to help you select an optimal team of football (soccer) players based on customizable performance criteria and constraints. Utilizing linear programming techniques, it allows you to maximize your team's overall performance according to the specific attributes you value most.

## Features

- **Dynamic Metric Selection**: Choose the performance metric you want to maximize (e.g., goals scored, assists, tackles).
- **Custom Constraints**: Define constraints on other metrics (e.g., maximum fouls, minimum clean sheets) to tailor the team selection to your strategy.
- **Data Cleaning**: Automatically excludes players with missing data in relevant criteria and constraints to ensure accurate optimization.
- **Optimized Team Selection**: Employs binary integer programming to select the team that maximizes your specified objective while satisfying all constraints.
- **Clear and Readable Code**: The program is well-documented with comments for easy understanding and modification.

## How to Download and Run

### Prerequisites

- **Python 3.x**: Ensure you have Python 3 installed on your system.
- **Required Python Packages**:
  - `pandas`
  - `pulp`

Install the required packages using pip:

```bash
pip install pandas pulp
