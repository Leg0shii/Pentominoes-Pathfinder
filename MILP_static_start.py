import gurobipy as gp
from gurobipy import GRB


# Approach #3 (for learning MILP purposes)
# MILP for finding longest possible path with set start and end position
# pretty fast but constraints are not correct yet (loops are still possible)
def find_longest_path(m, n, start, end):
    model = gp.Model("longest_path")
    x = model.addVars(m, n, vtype=GRB.BINARY, name="x")

    def neighbors(i, j):
        return [(x, y) for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)] if 0 <= x < m and 0 <= y < n]

    # Start and end constraints (have to be at static positions)
    model.addConstr(x[start[0], start[1]] == 1, "StartPosition")
    model.addConstr(x[end[0], end[1]] == 1, "EndPosition")

    # Start and end neighbor constraints
    model.addConstr(gp.quicksum(x[i, j] for i, j in neighbors(start[0], start[1])) == 1, "StartNeighbor")
    model.addConstr(gp.quicksum(x[i, j] for i, j in neighbors(end[0], end[1])) == 1, "EndNeighbor")

    # Path neighbor constraints using indicator constraints
    for i in range(m):
        for j in range(n):
            if (i, j) != start and (i, j) != end:
                path_neighbors = neighbors(i, j)
                # applied only on x[i, j] == 1, other instances ignored
                model.addGenConstrIndicator(x[i, j], True, gp.quicksum(x[k, l] for k, l in path_neighbors) == 2,
                                            name=f"ExactPathNeighbors_{i}_{j}")

    # Maximize the number of path cells
    model.setObjective(gp.quicksum(x[i, j] for i in range(m) for j in range(n)), GRB.MAXIMIZE)
    model.optimize()

    if model.status == GRB.OPTIMAL:
        return [[1 if x[i, j].x > 0.5 else 0 for j in range(n)] for i in range(m)]
    else:
        return None


m, n, start, end = 6, 6, (0, 0), (5, 5)
solution = find_longest_path(m, n, start, end)

if solution:
    total_length = sum(map(sum, solution))
    print(f"Length: {total_length}")
    print("\n".join(map(str, solution)))
else:
    print("No solution found")
