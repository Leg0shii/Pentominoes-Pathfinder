import gurobipy as gp
from gurobipy import GRB

# Fixing approach #3 (loops)
# allowing start end end position to be set dynamically
def find_longest_path(m, n):
    model = gp.Model("longest_path")

    # Path variables
    x = model.addVars(m, n, vtype=GRB.BINARY, name="x")  # Path cells
    s = model.addVars(m, n, vtype=GRB.BINARY, name="s")  # Start cell
    e = model.addVars(m, n, vtype=GRB.BINARY, name="e")  # End cell
    u = model.addVars(m, n, vtype=GRB.INTEGER, lb=0, ub=m * n, name="u")  # Ordering variables for subtour elimination

    def neighbors(i, j):
        return [(x, y) for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)] if 0 <= x < m and 0 <= y < n]

    # Constraint: Exactly one start and one end cell
    model.addConstr(gp.quicksum(s[i, j] for i in range(m) for j in range(n)) == 1, "OneStart")
    model.addConstr(gp.quicksum(e[i, j] for i in range(m) for j in range(n)) == 1, "OneEnd")

    for i in range(m):
        for j in range(n):
            start_neighbors = neighbors(i, j)
            model.addGenConstrIndicator(s[i, j], True, gp.quicksum(e[k, l] for k, l in start_neighbors), GRB.EQUAL, 0, f"StartEndNotAdjacent_{i}_{j}")
            model.addConstr(s[i, j] + e[i, j] <= 1, f"StartEndNotSame_{i}_{j}")

    # Neighbor constraints for path, start, end cells
    for i in range(m):
        for j in range(n):
            path_neighbors = neighbors(i, j)
            model.addGenConstrIndicator(s[i, j], True, gp.quicksum(x[k, l] for k, l in path_neighbors), GRB.EQUAL, 1, f"StartNeighbor_{i}_{j}")
            model.addGenConstrIndicator(e[i, j], True, gp.quicksum(x[k, l] for k, l in path_neighbors), GRB.EQUAL, 1, f"EndNeighbor_{i}_{j}")
            model.addGenConstrIndicator(x[i, j], True, gp.quicksum(x[k, l] + s[k, l] + e[k, l] for k, l in path_neighbors), GRB.EQUAL, 2, f"ExactPathNeighbors_{i}_{j}")

        # Subtour elimination constraints using ordering variables
        for i in range(m):
            for j in range(n):
                path_neighbors = neighbors(i, j)
                model.addGenConstrIndicator(x[i, j], True, u[i, j], GRB.GREATER_EQUAL, 1, f"ActiveU_{i}_{j}")
                model.addGenConstrIndicator(x[i, j], True, (gp.quicksum(u[ni, nj] for ni, nj in path_neighbors) / 2), GRB.EQUAL, 2, f"AvgNeighborConstr_{i}_{j}")

    # Objective: Maximize the number of path cells
    model.setObjective(gp.quicksum(x[i, j] for i in range(m) for j in range(n)), GRB.MAXIMIZE)
    model.optimize()

    # Handle infeasibility
    if model.status == GRB.INFEASIBLE:
        print("Model is infeasible; computing IIS")
        model.computeIIS()
        model.write("infeasible_model.ilp")

    if model.status == GRB.OPTIMAL:
        get_cell_value = lambda i, j: 5 if s[i, j].X > 0.5 else 3 if e[i, j].X > 0.5 else 1 if x[i, j].X > 0.5 else 0
        solution = [[get_cell_value(i, j) for j in range(n)] for i in range(m)]
        return solution
    else:
        return None


# Example usage
m, n = 8, 8

solution = find_longest_path(m, n)
if solution:
    total_sum = sum(sum(inner_list) for inner_list in solution)
    print(total_sum - 6)
    for row in solution:
        print(row)
else:
    print("No solution found")
