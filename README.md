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
