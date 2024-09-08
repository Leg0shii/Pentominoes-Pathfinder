import tkinter as tk
import time
from heapq import heappop, heappush
from tkinter import simpledialog


# Approach #2
# tries to generate the longest possible path following certain rules
# it is slow, very slow
class ClickableBoard:
    def __init__(self, root, rows, cols):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.status_label = None
        self.buttons = []
        self.previous_green = None
        self.saved_configs = []

        self.create_board()

    def create_board(self):
        # Clear existing buttons if they exist
        for widget in self.root.grid_slaves():
            widget.grid_forget()

        self.buttons = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                button = tk.Button(self.root, width=4, height=2, bg="lightgray")
                button.grid(row=i, column=j, sticky="ew")
                button.bind("<Button-1>", lambda event, r=i, c=j: self.on_left_click(r, c))
                button.bind("<Button-3>", lambda event, r=i, c=j: self.on_right_click(r, c))
                row.append(button)
            self.buttons.append(row)

        # Adjust the button size by setting width and height explicitly
        reset_button = tk.Button(self.root, text="Reset", command=self.reset_board, width=15, height=1)
        reset_button.grid(row=self.rows, column=0, columnspan=self.cols)

        count_button = tk.Button(self.root, text="Count Green Cells", command=self.count_green_cells, width=15, height=1)
        count_button.grid(row=self.rows + 1, column=0, columnspan=self.cols)

        save_button = tk.Button(self.root, text="Save Configuration", command=self.save_configuration, width=15, height=1)
        save_button.grid(row=self.rows + 2, column=0, columnspan=self.cols)

        load_button = tk.Button(self.root, text="Load Configuration", command=self.load_configuration, width=15, height=1)
        load_button.grid(row=self.rows + 3, column=0, columnspan=self.cols)

        path_button = tk.Button(self.root, text="Find Longest Path", command=self.find_longest_path, width=15, height=1)
        path_button.grid(row=self.rows + 4, column=0, columnspan=self.cols)

        update_button = tk.Button(self.root, text="Update Dimensions", command=self.update_dimensions, width=15, height=1)
        update_button.grid(row=self.rows + 7, column=0, columnspan=self.cols)

        self.dimension_entry = tk.Entry(self.root)
        self.dimension_entry.grid(row=self.rows + 6, column=0, columnspan=self.cols)
        self.dimension_entry.insert(0, f"{self.rows},{self.cols}")

        update_button = tk.Button(self.root, text="Update Dimensions", command=self.update_dimensions)
        update_button.grid(row=self.rows + 7, column=0, columnspan=self.cols)

        self.status_label = tk.Label(self.root, text="...", anchor="w")
        self.status_label.grid(row=self.rows + 8, column=0, columnspan=self.cols, sticky="ew")

    def update_dimensions(self):
        dimensions = self.dimension_entry.get().split(',')
        if len(dimensions) != 2:
            self.update_status("Invalid format. Use rows,cols format.")
            return

        try:
            new_rows = int(dimensions[0])
            new_cols = int(dimensions[1])
            if new_rows > 0 and new_cols > 0:
                self.rows = new_rows
                self.cols = new_cols
                self.create_board()  # Recreate the board with new dimensions
                self.update_status(f"Board updated to {new_rows} rows and {new_cols} columns.")
            else:
                self.update_status("Rows and columns must be positive numbers.")
        except ValueError:
            self.update_status("Invalid input. Rows and columns must be integers.")

    def on_left_click(self, row, col):
        current_color = self.buttons[row][col].cget("bg")
        if current_color == "lightgray":
            self.buttons[row][col].config(bg="green")
            if self.previous_green:
                self.color_neighbors_red(*self.previous_green)
            self.previous_green = (row, col)
        else:
            self.buttons[row][col].config(bg="lightgray")
            self.previous_green = None

    def on_right_click(self, row, col):
        current_color = self.buttons[row][col].cget("bg")
        if current_color == "lightgray":
            self.buttons[row][col].config(bg="red")
        else:
            self.buttons[row][col].config(bg="lightgray")

    def color_neighbors_red(self, row, col):
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for r, c in neighbors:
            if 0 <= r < self.rows and 0 <= c < self.cols:
                if self.buttons[r][c].cget("bg") == "lightgray":
                    self.buttons[r][c].config(bg="red")

    def reset_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].config(bg="lightgray")
        self.previous_green = None

    def count_green_cells(self):
        green_count = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.buttons[i][j].cget("bg") == "green":
                    green_count += 1
        self.update_status(f"There are {green_count} green cells on the board.")

    def save_configuration(self):
        config = []
        for i in range(self.rows):
            row_config = ""
            for j in range(self.cols):
                cell_color = self.buttons[i][j].cget("bg")
                if cell_color == "green":
                    row_config += "G"
                elif cell_color == "red":
                    row_config += "R"
                else:
                    row_config += "L"
            config.append(row_config)
        self.saved_configs.append(config)
        self.update_status("Configuration saved successfully!")

    def load_configuration(self):
        if not self.saved_configs:
            self.update_status("No configurations saved.")
            return

        config_index = simpledialog.askinteger("Load Configuration",
                                               f"Enter configuration number (1 to {len(self.saved_configs)}):")

        if config_index is None or not (1 <= config_index <= len(self.saved_configs)):
            self.update_status("Invalid configuration number.")
            return

        config = self.saved_configs[config_index - 1]
        for i in range(self.rows):
            for j in range(self.cols):
                color_char = config[i][j]
                if color_char == "G":
                    self.buttons[i][j].config(bg="green")
                elif color_char == "R":
                    self.buttons[i][j].config(bg="red")
                else:
                    self.buttons[i][j].config(bg="lightgray")

        self.update_status(f"Configuration {config_index} loaded successfully!")

    def find_longest_path(self):
        longest_path = []
        visited = [[False] * self.cols for _ in range(self.rows)]

        # Precompute heuristic values (distance from the center)
        center_r, center_c = self.rows // 2, self.cols // 2
        heuristic_map = [[-(abs(r - center_r) + abs(c - center_c)) for c in range(self.cols)] for r in range(self.rows)]

        def is_valid(r, c):
            if r < 0 or r >= self.rows or c < 0 or c >= self.cols or visited[r][c]:
                return False

            # Limit to 1 visited neighbor to ensure path growth
            neighbor_count = 0
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and visited[nr][nc]:
                    neighbor_count += 1
                    if neighbor_count > 1:
                        return False
            return True

        def greedy_dfs(r, c, path):
            nonlocal longest_path

            if not is_valid(r, c):
                return

            visited[r][c] = True
            path.append((r, c))

            if len(path) > len(longest_path):
                longest_path = path[:]

            # Explore neighbors using priority queue
            queue = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if is_valid(nr, nc):
                    heappush(queue, (heuristic_map[nr][nc], nr, nc))

            while queue:
                _, nr, nc = heappop(queue)
                greedy_dfs(nr, nc, path)

            visited[r][c] = False
            path.pop()

        start_time = time.time()

        for i in range(self.rows):
            for j in range(self.cols):
                greedy_dfs(i, j, [])

        end_time = time.time()
        elapsed_time = end_time - start_time

        for r, c in longest_path:
            self.buttons[r][c].config(bg="green")

        self.save_path_configuration(longest_path)
        self.update_status(
            f"The longest path length is {len(longest_path)}. Calculation time: {elapsed_time:.2f} seconds")

    def save_path_configuration(self, path):
        config = []
        for i in range(self.rows):
            row_config = ""
            for j in range(self.cols):
                if (i, j) in path:
                    row_config += "P"
                elif self.buttons[i][j].cget("bg") == "green":
                    row_config += "G"
                elif self.buttons[i][j].cget("bg") == "red":
                    row_config += "R"
                else:
                    row_config += "L"
            config.append(row_config)
        self.saved_configs.append(config)
        self.update_status("Longest path configuration saved successfully!")

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()


def create_board():
    root = tk.Tk()
    root.title("Customizable Clickable Board")

    ClickableBoard(root, 5, 5)
    root.mainloop()


create_board()
