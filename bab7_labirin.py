"""
Maze Generator & Solver — Struktur Data Bab 7: Stack
Versi GUI dengan Tkinter
=====================================================
- Generate labirin random pakai Recursive Backtracking
- Solve labirin pakai Stack-based DFS (Depth-First Search)
- Visualisasi animasi real-time dengan warna
- Panel Stack live update
"""

import random
import tkinter as tk
from tkinter import ttk
from collections import deque


# ─────────────────────────────────────────────
#  STACK ADT (implementasi manual, sesuai Bab 7)
# ─────────────────────────────────────────────
class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop dari stack kosong")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek dari stack kosong")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

    def to_list(self):
        return list(self._data)


# ─────────────────────────────────────────────
#  MAZE LOGIC
# ─────────────────────────────────────────────
WALL     = 0
PATH     = 1
VISITED  = 2
STACKED  = 3
SOLUTION = 4
START    = 5
END      = 6

COLORS = {
    WALL:     "#1e1e1e",
    PATH:     "#f5f0e8",
    VISITED:  "#378ADD",
    STACKED:  "#EF9F27",
    SOLUTION: "#639922",
    START:    "#1D9E75",
    END:      "#D85A30",
}


def generate_maze(rows, cols):
    grid = [[WALL] * cols for _ in range(rows)]

    def carve(r, c):
        grid[r][c] = PATH
        dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows - 1 and 1 <= nc < cols - 1 and grid[nr][nc] == WALL:
                grid[r + dr // 2][c + dc // 2] = PATH
                carve(nr, nc)

    carve(1, 1)
    grid[1][1] = START
    grid[rows - 2][cols - 2] = END
    return grid


def dfs_steps(grid, rows, cols):
    """
    Generator: yield satu langkah DFS per-iterasi.
    Setiap yield berisi (grid_snapshot, stack_list, visited_count, status).
    """
    stack = Stack()
    visited = set()
    parent = {}

    start = (1, 1)
    end = (rows - 2, cols - 2)

    stack.push(start)
    visited.add(start)
    parent[start] = None

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while not stack.is_empty():
        current = stack.peek()
        r, c = current

        if current == end:
            # Rekonstruksi jalur solusi
            path = []
            node = end
            while node:
                path.append(node)
                node = parent[node]
            path.reverse()
            for pr, pc in path:
                if grid[pr][pc] not in (START, END):
                    grid[pr][pc] = SOLUTION
            yield grid, stack.to_list(), len(visited), "solved", path
            return

        moved = False
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            nb = (nr, nc)
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] not in (WALL,)
                    and nb not in visited):
                if grid[nr][nc] not in (START, END):
                    grid[nr][nc] = STACKED
                stack.push(nb)
                visited.add(nb)
                parent[nb] = current
                moved = True

        if not moved:
            stack.pop()
        else:
            if grid[r][c] not in (START, END):
                grid[r][c] = VISITED

        yield grid, stack.to_list(), len(visited), "searching", None

    yield grid, [], len(visited), "no_path", None


# ─────────────────────────────────────────────
#  GUI APPLICATION
# ─────────────────────────────────────────────
class MazeApp:
    SIZE_OPTIONS = {"Kecil (11×11)": 11, "Sedang (15×15)": 15, "Besar (21×21)": 21}
    SPEED_OPTIONS = {"Lambat": 120, "Sedang": 40, "Cepat": 12, "Turbo": 2}

    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver — Struktur Data Bab 7: Stack DFS")
        self.root.configure(bg="#111111")
        self.root.resizable(True, True)

        self.grid = None
        self.rows = 15
        self.cols = 15
        self.cell = 30
        self.anim_id = None
        self.generator = None
        self.solving = False
        self.step_count = 0

        self._build_ui()
        self._new_maze()

    # ── UI Layout ────────────────────────────
    def _build_ui(self):
        # ── Top bar ──
        top = tk.Frame(self.root, bg="#111111", pady=8)
        top.pack(fill=tk.X, padx=12)

        tk.Label(top, text="Maze Solver", font=("Courier New", 15, "bold"),
                 fg="#EF9F27", bg="#111111").pack(side=tk.LEFT)
        tk.Label(top, text=" — Stack DFS  |  Bab 7 Struktur Data",
                 font=("Courier New", 11), fg="#888", bg="#111111").pack(side=tk.LEFT)

        # ── Controls ──
        ctrl = tk.Frame(self.root, bg="#1a1a1a", pady=6, padx=10)
        ctrl.pack(fill=tk.X, padx=12, pady=(0, 6))

        # Ukuran
        tk.Label(ctrl, text="Ukuran:", fg="#aaa", bg="#1a1a1a",
                 font=("Courier New", 10)).pack(side=tk.LEFT, padx=(0, 4))
        self.size_var = tk.StringVar(value="Sedang (15×15)")
        size_cb = ttk.Combobox(ctrl, textvariable=self.size_var,
                               values=list(self.SIZE_OPTIONS.keys()),
                               width=14, state="readonly")
        size_cb.pack(side=tk.LEFT, padx=(0, 12))
        size_cb.bind("<<ComboboxSelected>>", lambda e: self._new_maze())

        # Kecepatan
        tk.Label(ctrl, text="Kecepatan:", fg="#aaa", bg="#1a1a1a",
                 font=("Courier New", 10)).pack(side=tk.LEFT, padx=(0, 4))
        self.speed_var = tk.StringVar(value="Sedang")
        ttk.Combobox(ctrl, textvariable=self.speed_var,
                     values=list(self.SPEED_OPTIONS.keys()),
                     width=10, state="readonly").pack(side=tk.LEFT, padx=(0, 16))

        # Buttons
        btn_style = dict(font=("Courier New", 10, "bold"), relief="flat",
                         cursor="hand2", padx=12, pady=4)
        tk.Button(ctrl, text="⟳  Labirin Baru", bg="#EF9F27", fg="#1a1a1a",
                  command=self._new_maze, **btn_style).pack(side=tk.LEFT, padx=4)
        tk.Button(ctrl, text="▶  Cari Jalan (DFS)", bg="#1D9E75", fg="white",
                  command=self._start_solve, **btn_style).pack(side=tk.LEFT, padx=4)
        tk.Button(ctrl, text="↺  Reset", bg="#378ADD", fg="white",
                  command=self._reset, **btn_style).pack(side=tk.LEFT, padx=4)

        # ── Main area ──
        main = tk.Frame(self.root, bg="#111111")
        main.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)

        # Canvas frame
        canvas_frame = tk.Frame(main, bg="#111111")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="#111111",
                                highlightthickness=1, highlightbackground="#333")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Right panel
        right = tk.Frame(main, bg="#1a1a1a", width=200,
                         relief="flat", bd=0)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right.pack_propagate(False)

        # Status
        tk.Label(right, text="STATUS", fg="#EF9F27", bg="#1a1a1a",
                 font=("Courier New", 9, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 2))
        self.status_var = tk.StringVar(value="Siap")
        tk.Label(right, textvariable=self.status_var, fg="#ddd", bg="#1a1a1a",
                 font=("Courier New", 10), wraplength=180,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=10)

        # Stats
        tk.Frame(right, bg="#333", height=1).pack(fill=tk.X, padx=10, pady=8)
        stats = tk.Frame(right, bg="#1a1a1a")
        stats.pack(fill=tk.X, padx=10)

        self._stat_labels = {}
        for key, label in [("steps", "Langkah"), ("visited", "Dikunjungi"),
                            ("stack_size", "Stack Size"), ("path_len", "Panjang Jalur")]:
            row = tk.Frame(stats, bg="#1a1a1a")
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=label + ":", fg="#888", bg="#1a1a1a",
                     font=("Courier New", 9)).pack(side=tk.LEFT)
            var = tk.StringVar(value="—")
            tk.Label(row, textvariable=var, fg="#EF9F27", bg="#1a1a1a",
                     font=("Courier New", 10, "bold")).pack(side=tk.RIGHT)
            self._stat_labels[key] = var

        # Stack visualizer
        tk.Frame(right, bg="#333", height=1).pack(fill=tk.X, padx=10, pady=8)
        tk.Label(right, text="STACK  (TOP → BAWAH)", fg="#EF9F27", bg="#1a1a1a",
                 font=("Courier New", 9, "bold")).pack(anchor=tk.W, padx=10, pady=(0, 4))

        stack_scroll_frame = tk.Frame(right, bg="#1a1a1a")
        stack_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        scrollbar = tk.Scrollbar(stack_scroll_frame, bg="#222")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.stack_listbox = tk.Listbox(
            stack_scroll_frame,
            yscrollcommand=scrollbar.set,
            bg="#111", fg="#9FE1CB",
            font=("Courier New", 10),
            selectbackground="#1D9E75",
            relief="flat", bd=0,
            activestyle="none"
        )
        self.stack_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.stack_listbox.yview)

        # Legend
        leg_frame = tk.Frame(self.root, bg="#111111", pady=6)
        leg_frame.pack(fill=tk.X, padx=12)
        legends = [
            ("#1D9E75", "Start"),
            ("#D85A30", "End"),
            ("#378ADD", "Dieksplorasi"),
            ("#EF9F27", "Di Stack"),
            ("#639922", "Jalur Solusi"),
            ("#1e1e1e", "Dinding"),
        ]
        for color, label in legends:
            box = tk.Frame(leg_frame, bg=color, width=14, height=14)
            box.pack(side=tk.LEFT, padx=(0, 4))
            tk.Label(leg_frame, text=label, fg="#aaa", bg="#111111",
                     font=("Courier New", 9)).pack(side=tk.LEFT, padx=(0, 12))

    # ── Maze Actions ─────────────────────────
    def _new_maze(self):
        if self.anim_id:
            self.root.after_cancel(self.anim_id)
            self.anim_id = None
        self.solving = False
        self.step_count = 0

        n = self.SIZE_OPTIONS[self.size_var.get()]
        self.rows = self.cols = n
        self.grid = generate_maze(self.rows, self.cols)
        self.generator = None

        self._update_cell_size()
        self._draw_maze()
        self._update_stack_panel([], 0)
        self.status_var.set("Labirin baru dibuat.\nKlik ▶ untuk solve.")
        for k in self._stat_labels:
            self._stat_labels[k].set("—")

    def _update_cell_size(self):
        self.root.update_idletasks()
        w = self.canvas.winfo_width() or 480
        h = self.canvas.winfo_height() or 480
        self.cell = max(8, min(w // self.cols, h // self.rows))

    def _start_solve(self):
        if self.solving:
            return
        if self.generator is None:
            self._reset_grid_colors()
            import copy
            self._solve_grid = copy.deepcopy(self.grid)
            self.generator = dfs_steps(self._solve_grid, self.rows, self.cols)
        self.solving = True
        self.status_var.set("Mencari jalur...")
        self._animate()

    def _reset(self):
        if self.anim_id:
            self.root.after_cancel(self.anim_id)
            self.anim_id = None
        self.solving = False
        self.generator = None
        self.step_count = 0
        self._reset_grid_colors()
        self._draw_maze()
        self._update_stack_panel([], 0)
        self.status_var.set("Reset. Klik ▶ untuk coba lagi.")
        for k in self._stat_labels:
            self._stat_labels[k].set("—")

    def _reset_grid_colors(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] in (VISITED, STACKED, SOLUTION):
                    self.grid[r][c] = PATH

    # ── Animation Loop ────────────────────────
    def _animate(self):
        if not self.solving or self.generator is None:
            return

        speed = self.SPEED_OPTIONS[self.speed_var.get()]
        # batch beberapa step sekaligus di kecepatan tinggi
        batch = max(1, 60 // speed)

        status = "searching"
        for _ in range(batch):
            try:
                grid, stack_list, visited_count, status, path = next(self.generator)
                self.step_count += 1
            except StopIteration:
                self.solving = False
                self._draw_maze()
                break

        self._draw_maze()
        self._stat_labels["steps"].set(str(self.step_count))
        self._stat_labels["visited"].set(str(visited_count))
        self._stat_labels["stack_size"].set(str(len(stack_list)))
        self._update_stack_panel(stack_list, visited_count)

        if status == "solved":
            self.solving = False
            path_len = sum(
                1 for r in range(self.rows) for c in range(self.cols)
                if self._solve_grid[r][c] == SOLUTION
            ) + 2  # +2 untuk Start & End
            self._stat_labels["path_len"].set(str(path_len))
            self.status_var.set(f"✓ Jalur ditemukan!\n{path_len} sel, {self.step_count} langkah.")
            self._update_stack_panel([], visited_count)
        elif status == "no_path":
            self.solving = False
            self.status_var.set("✗ Tidak ada jalur!")
            self._update_stack_panel([], visited_count)
        else:
            self.status_var.set(
                f"Mencari jalur...\nStack: {len(stack_list)}  |  Visited: {visited_count}"
            )
            self.anim_id = self.root.after(speed, self._animate)

    # ── Drawing ───────────────────────────────
    def _draw_maze(self):
        self._update_cell_size()
        cell = self.cell
        self.canvas.delete("all")

        src = self._solve_grid if (self.generator is not None) else self.grid

        for r in range(self.rows):
            for c in range(self.cols):
                v = src[r][c]
                color = COLORS.get(v, COLORS[PATH])
                x0, y0 = c * cell, r * cell
                x1, y1 = x0 + cell, y0 + cell
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

                # Label S dan E
                if v == START:
                    self.canvas.create_text(
                        x0 + cell // 2, y0 + cell // 2, text="S",
                        font=("Courier New", max(7, cell // 2), "bold"), fill="white"
                    )
                elif v == END:
                    self.canvas.create_text(
                        x0 + cell // 2, y0 + cell // 2, text="E",
                        font=("Courier New", max(7, cell // 2), "bold"), fill="white"
                    )

    def _update_stack_panel(self, stack_list, visited):
        self.stack_listbox.delete(0, tk.END)
        if not stack_list:
            self.stack_listbox.insert(tk.END, "  (kosong)")
            return
        # Tampilkan dari TOP ke bawah
        for i, (r, c) in enumerate(reversed(stack_list)):
            prefix = "▶ " if i == 0 else "  "
            self.stack_listbox.insert(tk.END, f"{prefix}({r}, {c})")
        # Highlight TOP
        if self.stack_listbox.size() > 0:
            self.stack_listbox.itemconfig(0, fg="#EF9F27", selectforeground="#EF9F27")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("860x620")
    root.minsize(600, 480)

    # Style Combobox agar sesuai tema gelap
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox",
                    fieldbackground="#2a2a2a",
                    background="#2a2a2a",
                    foreground="#ddd",
                    selectbackground="#EF9F27",
                    selectforeground="#111")

    app = MazeApp(root)
    root.mainloop()
