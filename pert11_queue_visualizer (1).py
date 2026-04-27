"""
Queue — 5 Kasus Implementasi
Visualisasi Interaktif · Struktur Data & Algoritma
Versi Python (tkinter)
"""

import tkinter as tk
from tkinter import ttk, font
import random
import time
import threading
from collections import deque

# ═══════════════════════════════════════════════════
#  WARNA TEMA (dark mode)
# ═══════════════════════════════════════════════════
BG       = "#0a0e1a"
PANEL    = "#111827"
BORDER   = "#1e2d45"
ACCENT1  = "#00d4ff"  # cyan
ACCENT2  = "#7c3aed"  # purple
ACCENT3  = "#10b981"  # green
ACCENT4  = "#f59e0b"  # amber
ACCENT5  = "#ef4444"  # red
TEXT     = "#e2e8f0"
MUTED    = "#64748b"
NODE_BG  = "#1e293b"
NODE_BD  = "#334155"

TAB_COLORS  = ["", ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5]
TAB_LABELS  = [
    "", "🖨️ Kasus 1: Antrian Printer", "🥔 Kasus 2: Hot Potato",
    "🏥 Kasus 3: Priority Queue RS", "🔍 Kasus 4: BFS Graf",
    "✈️ Kasus 5: Loket Bandara"
]

DOC_COLORS = {
    'laporan.pdf': ACCENT1, 'tugas.docx': ACCENT2,
    'foto.jpg': ACCENT3, 'presentasi.pptx': ACCENT4,
    'spreadsheet.xlsx': ACCENT5, 'skripsi.pdf': '#ec4899',
}
PLAYER_COLORS = [ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5,
                 '#ec4899', '#06b6d4', '#84cc16']
PLAYERS = ['Andi','Budi','Citra','Dedi','Eka','Fara','Gita','Hana']

PRIO_COLORS = ['#ff4444','#f59e0b','#3b82f6','#22c55e']
PRIO_LABELS = ['🔴 KRITIS','🟡 DARURAT','🔵 MENENGAH','🟢 RINGAN']

GRAPH4 = {
    'A': ['B','C'], 'B': ['A','D','E'], 'C': ['A','F'],
    'D': ['B'],     'E': ['B','G'],     'F': ['C','G'], 'G': ['E','F']
}
NODE_POS = {
    'A':(0.50,0.08), 'B':(0.20,0.35), 'C':(0.80,0.35),
    'D':(0.05,0.70), 'E':(0.38,0.70), 'F':(0.65,0.70), 'G':(0.52,0.92)
}
EDGES4 = [('A','B'),('A','C'),('B','D'),('B','E'),('C','F'),('E','G'),('F','G')]


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def blend(hex_color, alpha=0.15):
    r, g, b = hex_to_rgb(hex_color)
    br, bg_, bb = hex_to_rgb(BG)
    nr = int(br + (r - br) * alpha)
    ng = int(bg_ + (g - bg_) * alpha)
    nb = int(bb + (b - bb) * alpha)
    return f"#{nr:02x}{ng:02x}{nb:02x}"


# ═══════════════════════════════════════════════════
#  HELPER WIDGETS
# ═══════════════════════════════════════════════════
def styled_btn(parent, text, color, command, fg=None):
    fg_col = fg or ("#000" if color in (ACCENT1, ACCENT3, ACCENT4) else "#fff")
    b = tk.Button(
        parent, text=text, command=command,
        bg=color, fg=fg_col, relief="flat",
        font=("Helvetica", 10, "bold"),
        padx=10, pady=5, cursor="hand2",
        activebackground=color, activeforeground=fg_col, bd=0
    )
    def on_enter(e): b.config(bg=_lighten(color))
    def on_leave(e): b.config(bg=color)
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)
    return b

def _lighten(hex_c):
    try:
        r,g,b = hex_to_rgb(hex_c)
        r = min(255, r + 30); g = min(255, g + 30); b = min(255, b + 30)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_c

def make_stat_row(parent, labels_ids):
    """labels_ids: list of (label_text, var_id_str)"""
    f = tk.Frame(parent, bg=PANEL)
    f.pack(fill="x", padx=0, pady=(0,8))
    vars_ = {}
    for label, vid in labels_ids:
        chip = tk.Frame(f, bg=NODE_BG, bd=0, highlightbackground=BORDER,
                        highlightthickness=1)
        chip.pack(side="left", padx=(0,6))
        tk.Label(chip, text=label, bg=NODE_BG, fg=MUTED,
                 font=("Helvetica",9)).pack(side="left", padx=(8,2), pady=4)
        v = tk.StringVar(value="0")
        l = tk.Label(chip, textvariable=v, bg=NODE_BG, fg=TEXT,
                     font=("Courier",10,"bold"))
        l.pack(side="left", padx=(0,8), pady=4)
        vars_[vid] = (v, l)
    return vars_

def log_msg(log_widget, msg, color=ACCENT1):
    log_widget.config(state="normal")
    log_widget.insert("1.0", msg + "\n")
    log_widget.config(state="disabled")
    # trim
    lines = int(log_widget.index("end-1c").split('.')[0])
    if lines > 30:
        log_widget.config(state="normal")
        log_widget.delete(f"{30}.0", "end")
        log_widget.config(state="disabled")
    # color first line
    log_widget.config(state="normal")
    log_widget.tag_add("first", "1.0", "2.0")
    log_widget.tag_config("first", foreground=color)
    log_widget.config(state="disabled")

def make_log(parent):
    f = tk.Frame(parent, bg="#060b14", bd=0, highlightbackground=BORDER,
                 highlightthickness=1)
    f.pack(fill="x", pady=(0,8))
    t = tk.Text(f, bg="#060b14", fg=ACCENT1, height=5,
                font=("Courier",9), bd=0, state="disabled",
                insertbackground=TEXT, wrap="word",
                highlightthickness=0)
    sb = tk.Scrollbar(f, command=t.yview, bg=PANEL, troughcolor=PANEL)
    t.config(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    t.pack(fill="both", expand=True, padx=8, pady=6)
    log_msg(t, "// Siap.", ACCENT1)
    return t

def make_arena(parent, title):
    outer = tk.Frame(parent, bg=PANEL, bd=0, highlightbackground=BORDER,
                     highlightthickness=1)
    outer.pack(fill="x", pady=(0,8))
    tk.Label(outer, text=title, bg=PANEL, fg=MUTED,
             font=("Helvetica",8,"bold")).pack(anchor="w", padx=12, pady=(10,4))
    inner = tk.Frame(outer, bg=PANEL)
    inner.pack(fill="x", padx=12, pady=(0,10))
    return inner

def make_code_block(parent, code_text):
    f = tk.Frame(parent, bg="#060b14", bd=0, highlightbackground=BORDER,
                 highlightthickness=1)
    f.pack(fill="x", pady=(0,8))
    t = tk.Text(f, bg="#060b14", fg="#a3c4dc", height=len(code_text.strip().split('\n'))+1,
                font=("Courier",9), bd=0, state="normal",
                highlightthickness=0, wrap="none")
    t.insert("1.0", code_text.strip())
    t.config(state="disabled")
    t.pack(fill="x", padx=12, pady=8)


# ═══════════════════════════════════════════════════
#  MAIN APPLICATION
# ═══════════════════════════════════════════════════
class QueueVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Queue — 5 Kasus Implementasi")
        self.configure(bg=BG)
        self.geometry("1020x780")
        self.minsize(800, 600)

        self._build_header()
        self._build_tabs()
        self._build_content_area()
        self._build_cases()
        self._switch_case(1)

    # ── HEADER ──────────────────────────────────────
    def _build_header(self):
        h = tk.Frame(self, bg="#0d1526", pady=16)
        h.pack(fill="x")
        tk.Label(h, text="Queue — 5 Kasus Implementasi", bg="#0d1526",
                 fg=ACCENT1, font=("Helvetica",20,"bold")).pack()
        tk.Label(h, text="VISUALISASI INTERAKTIF · STRUKTUR DATA & ALGORITMA",
                 bg="#0d1526", fg=MUTED, font=("Helvetica",9)).pack()
        sep = tk.Frame(self, bg=BORDER, height=1)
        sep.pack(fill="x")

    # ── TABS ────────────────────────────────────────
    def _build_tabs(self):
        tab_bar = tk.Frame(self, bg=PANEL, pady=10)
        tab_bar.pack(fill="x")
        self._tab_btns = {}
        for i in range(1, 6):
            col = TAB_COLORS[i]
            b = tk.Button(
                tab_bar, text=TAB_LABELS[i],
                command=lambda n=i: self._switch_case(n),
                bg=PANEL, fg=MUTED, relief="flat",
                font=("Helvetica", 9, "bold"), padx=12, pady=6,
                cursor="hand2", activebackground=col, bd=1,
                highlightbackground=BORDER, highlightthickness=1
            )
            b.pack(side="left", padx=4)
            self._tab_btns[i] = (b, col)
        sep = tk.Frame(self, bg=BORDER, height=1)
        sep.pack(fill="x")

    def _switch_case(self, n):
        self._active_case = n
        for i, (b, col) in self._tab_btns.items():
            if i == n:
                fg = "#000" if col in (ACCENT1, ACCENT3, ACCENT4) else "#fff"
                b.config(bg=col, fg=fg)
            else:
                b.config(bg=PANEL, fg=MUTED)
        for i, frame in self._cases.items():
            frame.pack_forget()
        self._cases[n].pack(fill="both", expand=True)

    # ── SCROLLABLE CONTENT ──────────────────────────
    def _build_content_area(self):
        self._canvas = tk.Canvas(self, bg=BG, bd=0, highlightthickness=0)
        self._vsb = tk.Scrollbar(self, orient="vertical",
                                 command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._vsb.set)
        self._vsb.pack(side="right", fill="y")
        self._canvas.pack(fill="both", expand=True)

        self._scroll_frame = tk.Frame(self._canvas, bg=BG)
        self._canvas_win = self._canvas.create_window(
            (0, 0), window=self._scroll_frame, anchor="nw")

        self._scroll_frame.bind("<Configure>", self._on_frame_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_frame_configure(self, e):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, e):
        self._canvas.itemconfig(self._canvas_win, width=e.width)

    def _on_mousewheel(self, e):
        self._canvas.yview_scroll(int(-1*(e.delta/120)), "units")

    # ── BUILD ALL CASES ─────────────────────────────
    def _build_cases(self):
        self._cases = {}
        for i in range(1, 6):
            f = tk.Frame(self._scroll_frame, bg=BG, padx=20, pady=14)
            self._cases[i] = f
        self._build_case1()
        self._build_case2()
        self._build_case3()
        self._build_case4()
        self._build_case5()

    # ─────────────────────────────────────────────────
    #  KASUS 1: PRINTER QUEUE
    # ─────────────────────────────────────────────────
    def _build_case1(self):
        parent = self._cases[1]
        self._p1_queue = deque()
        self._p1_printed = 0
        self._p1_auto_running = False

        # Header
        hf = tk.Frame(parent, bg=BG)
        hf.pack(fill="x", pady=(0,10))
        tk.Label(hf, text="KASUS 1", bg=blend(ACCENT1), fg=ACCENT1,
                 font=("Helvetica",8,"bold"), padx=8, pady=3).pack(side="left", padx=(0,10))
        tf = tk.Frame(hf, bg=BG)
        tf.pack(side="left")
        tk.Label(tf, text="Antrian Printer Bersama", bg=BG, fg=TEXT,
                 font=("Helvetica",14,"bold")).pack(anchor="w")
        tk.Label(tf, text="Dokumen dicetak sesuai urutan kedatangan — FIFO murni",
                 bg=BG, fg=MUTED, font=("Helvetica",9)).pack(anchor="w")

        # Stats
        self._p1_vars = make_stat_row(parent, [
            ("Ukuran Queue:", "size"),
            ("Total Dicetak:", "printed"),
            ("Status Printer:", "status"),
        ])
        self._p1_vars["status"][0].set("IDLE")
        self._p1_vars["status"][1].config(fg=ACCENT3)

        # Arena
        arena = make_arena(parent, "📋 Antrian Dokumen")
        lf = tk.Frame(arena, bg=PANEL)
        lf.pack(fill="x")
        tk.Label(lf, text="← DEPAN (dequeue)", bg=PANEL, fg=ACCENT3,
                 font=("Courier",8)).pack(side="left")
        tk.Label(lf, text="BELAKANG (enqueue) →", bg=PANEL, fg=ACCENT1,
                 font=("Courier",8)).pack(side="right")
        self._p1_track = tk.Frame(arena, bg=PANEL, height=80)
        self._p1_track.pack(fill="x", pady=6)
        self._p1_empty = tk.Label(arena, text="Queue kosong — tambahkan dokumen!",
                                  bg=PANEL, fg=MUTED, font=("Helvetica",9))
        self._p1_empty.pack()

        # Controls
        cf = tk.Frame(parent, bg=BG)
        cf.pack(fill="x", pady=(0,8))
        self._p1_doc_var = tk.StringVar(value='laporan.pdf')
        docs = list(DOC_COLORS.keys())
        om = tk.OptionMenu(cf, self._p1_doc_var, *docs)
        om.config(bg=NODE_BG, fg=TEXT, highlightbackground=BORDER,
                  activebackground=NODE_BG, relief="flat", font=("Helvetica",9))
        om["menu"].config(bg=NODE_BG, fg=TEXT)
        om.pack(side="left", padx=(0,6))
        styled_btn(cf, "➕ Enqueue (Kirim)", ACCENT1, self._p1_enqueue).pack(side="left", padx=(0,6))
        self._p1_deq_btn = styled_btn(cf, "🖨️ Dequeue (Cetak)", ACCENT5, self._p1_dequeue, "#fff")
        self._p1_deq_btn.pack(side="left", padx=(0,6))
        styled_btn(cf, "▶ Auto Cetak", ACCENT4, self._p1_auto, "#000").pack(side="left", padx=(0,6))
        styled_btn(cf, "↺ Reset", NODE_BG, self._p1_reset, TEXT).pack(side="left")

        self._p1_log = make_log(parent)
        log_msg(self._p1_log, "// Sistem antrian printer siap. Kirim dokumen!", ACCENT1)

        make_code_block(parent, """# Simulasi Antrian Printer
printer_queue = Queue()
printer_queue.enqueue("laporan.pdf")   # → rear
printer_queue.enqueue("tugas.docx")    # → rear
printer_queue.enqueue("foto.jpg")      # → rear
while not printer_queue.isEmpty():
    doc = printer_queue.dequeue()      # ← front
    print(f"Mencetak: {doc}")""")

        # Init
        for d in ['laporan.pdf', 'tugas.docx', 'foto.jpg']:
            self._p1_queue.append(d)
        self._p1_render()

    def _p1_render(self):
        for w in self._p1_track.winfo_children():
            w.destroy()
        if not self._p1_queue:
            self._p1_empty.pack()
        else:
            self._p1_empty.pack_forget()
        for i, doc in enumerate(self._p1_queue):
            col = DOC_COLORS.get(doc, '#94a3b8')
            bg_ = blend(col, 0.13)
            box = tk.Frame(self._p1_track, bg=bg_, bd=2,
                           highlightbackground=col, highlightthickness=2,
                           width=64, height=52)
            box.pack(side="left", padx=2)
            box.pack_propagate(False)
            short = (doc[:6]+'..') if len(doc) > 8 else doc
            tk.Label(box, text=short, bg=bg_, fg=col,
                     font=("Courier",8,"bold"), wraplength=58).pack(expand=True)
            idx_text = f"[{i}]" + (" ←front" if i == 0 else "")
            tk.Label(self._p1_track, text=idx_text, bg=PANEL, fg=MUTED,
                     font=("Courier",7)).pack(side="left")
            if i < len(self._p1_queue) - 1:
                tk.Label(self._p1_track, text="→", bg=PANEL, fg=MUTED,
                         font=("Helvetica",12)).pack(side="left", padx=2)
        self._p1_vars["size"][0].set(str(len(self._p1_queue)))
        self._p1_vars["printed"][0].set(str(self._p1_printed))
        self._p1_deq_btn.config(state="normal" if self._p1_queue else "disabled")

    def _p1_enqueue(self):
        doc = self._p1_doc_var.get()
        self._p1_queue.append(doc)
        log_msg(self._p1_log, f'✉ enqueue("{doc}") → rear idx {len(self._p1_queue)-1}', ACCENT1)
        self._p1_render()

    def _p1_dequeue(self):
        if not self._p1_queue:
            log_msg(self._p1_log, "⚠ Queue kosong!", ACCENT5)
            return
        doc = self._p1_queue.popleft()
        self._p1_printed += 1
        self._p1_vars["status"][0].set(f"🖨 {doc}")
        self._p1_vars["status"][1].config(fg=ACCENT4)
        log_msg(self._p1_log, f'🖨 Mencetak: "{doc}" ← dequeue dari front', ACCENT3)
        self.after(900, lambda: (
            self._p1_vars["status"][0].set("IDLE"),
            self._p1_vars["status"][1].config(fg=ACCENT3)
        ))
        self._p1_render()

    def _p1_auto(self):
        if self._p1_auto_running or not self._p1_queue:
            return
        self._p1_auto_running = True
        def step():
            if self._p1_queue:
                self._p1_dequeue()
                self.after(950, step)
            else:
                self._p1_auto_running = False
        step()

    def _p1_reset(self):
        self._p1_queue.clear()
        self._p1_printed = 0
        self._p1_vars["status"][0].set("IDLE")
        self._p1_vars["status"][1].config(fg=ACCENT3)
        self._p1_log.config(state="normal")
        self._p1_log.delete("1.0", "end")
        self._p1_log.config(state="disabled")
        log_msg(self._p1_log, "// Reset. Siap menerima dokumen.", ACCENT1)
        self._p1_render()

    # ─────────────────────────────────────────────────
    #  KASUS 2: HOT POTATO
    # ─────────────────────────────────────────────────
    def _build_case2(self):
        parent = self._cases[2]
        self._p2_queue = deque()
        self._p2_running = False

        hf = tk.Frame(parent, bg=BG)
        hf.pack(fill="x", pady=(0,10))
        tk.Label(hf, text="KASUS 2", bg=blend(ACCENT2, 0.2), fg=ACCENT2,
                 font=("Helvetica",8,"bold"), padx=8, pady=3).pack(side="left", padx=(0,10))
        tf = tk.Frame(hf, bg=BG)
        tf.pack(side="left")
        tk.Label(tf, text="Permainan Hot Potato", bg=BG, fg=TEXT,
                 font=("Helvetica",14,"bold")).pack(anchor="w")
        tk.Label(tf, text="Simulasi melingkar — dequeue lalu enqueue kembali",
                 bg=BG, fg=MUTED, font=("Helvetica",9)).pack(anchor="w")

        self._p2_vars = make_stat_row(parent, [
            ("Pemain tersisa:", "remaining"),
            ("Putaran oper (N):", "n_display"),
            ("Pemenang:", "winner"),
        ])
        self._p2_vars["winner"][1].config(fg=ACCENT3)

        arena = make_arena(parent, "🥔 Lingkaran Pemain")
        self._p2_circle = tk.Frame(arena, bg=PANEL, height=80)
        self._p2_circle.pack(fill="x")

        cf = tk.Frame(parent, bg=BG)
        cf.pack(fill="x", pady=(0,8))
        tk.Label(cf, text="N oper:", bg=BG, fg=MUTED, font=("Helvetica",9)).pack(side="left", padx=(0,4))
        self._p2_n_var = tk.IntVar(value=3)
        ns = tk.Spinbox(cf, from_=1, to=20, textvariable=self._p2_n_var, width=5,
                        bg=NODE_BG, fg=TEXT, buttonbackground=NODE_BG,
                        insertbackground=TEXT, relief="flat", font=("Courier",10),
                        command=lambda: self._p2_vars["n_display"][0].set(str(self._p2_n_var.get())))
        ns.pack(side="left", padx=(0,8))
        styled_btn(cf, "🔄 Setup Pemain", ACCENT2, self._p2_setup, "#fff").pack(side="left", padx=(0,6))
        self._p2_step_btn = styled_btn(cf, "⏩ Satu Putaran", ACCENT4, self._p2_step, "#000")
        self._p2_step_btn.pack(side="left", padx=(0,6))
        self._p2_auto_btn = styled_btn(cf, "▶ Auto Play", ACCENT3, self._p2_auto)
        self._p2_auto_btn.pack(side="left", padx=(0,6))
        styled_btn(cf, "↺ Reset", NODE_BG, self._p2_reset, TEXT).pack(side="left")
        self._p2_step_btn.config(state="disabled")
        self._p2_auto_btn.config(state="disabled")

        self._p2_log = make_log(parent)
        log_msg(self._p2_log, '// Klik "Setup Pemain" untuk mulai!', ACCENT1)

        make_code_block(parent, """def hot_potato(names, num):
    q = Queue()
    for name in names: q.enqueue(name)
    while len(q) > 1:
        for _ in range(num):
            q.enqueue(q.dequeue())  # oper melingkar
        q.dequeue()  # ← tersingkir!
    return q.dequeue()  # pemenang!""")

    def _p2_render(self):
        for w in self._p2_circle.winfo_children():
            w.destroy()
        for i, name in enumerate(self._p2_queue):
            is_holder = (i == 0)
            col = PLAYER_COLORS[PLAYERS.index(name) % len(PLAYER_COLORS)] if name in PLAYERS else ACCENT1
            bg_ = col if is_holder else blend(col, 0.2)
            fg_ = "#000" if is_holder else col
            lbl = tk.Label(self._p2_circle,
                           text=("🥔 " if is_holder else "") + name,
                           bg=bg_, fg=fg_,
                           font=("Helvetica",9,"bold"),
                           padx=10, pady=5, bd=2,
                           relief="flat",
                           highlightbackground=col, highlightthickness=2)
            lbl.pack(side="left", padx=3, pady=6)
        self._p2_vars["remaining"][0].set(str(len(self._p2_queue)))

    def _p2_setup(self):
        self._p2_queue = deque(PLAYERS)
        self._p2_vars["winner"][0].set("—")
        self._p2_step_btn.config(state="normal")
        self._p2_auto_btn.config(state="normal")
        log_msg(self._p2_log, f'🎮 Game dimulai dengan {len(self._p2_queue)} pemain', ACCENT1)
        self._p2_render()

    def _p2_step(self):
        if len(self._p2_queue) <= 1:
            return
        N = self._p2_n_var.get()
        for _ in range(N):
            self._p2_queue.append(self._p2_queue.popleft())
        eliminated = self._p2_queue.popleft()
        log_msg(self._p2_log, f'❌ {eliminated} tersingkir setelah {N}x oper!', ACCENT4)
        if len(self._p2_queue) == 1:
            winner = self._p2_queue[0]
            log_msg(self._p2_log, f'🏆 PEMENANG: {winner}!', ACCENT3)
            self._p2_vars["winner"][0].set(winner)
            self._p2_step_btn.config(state="disabled")
            self._p2_auto_btn.config(state="disabled")
        self._p2_render()

    def _p2_auto(self):
        if self._p2_running:
            return
        self._p2_running = True
        self._p2_auto_btn.config(state="disabled")
        def step():
            if len(self._p2_queue) > 1:
                self._p2_step()
                self.after(700, step)
            else:
                self._p2_running = False
        step()

    def _p2_reset(self):
        self._p2_queue.clear()
        self._p2_running = False
        for w in self._p2_circle.winfo_children():
            w.destroy()
        self._p2_vars["remaining"][0].set("0")
        self._p2_vars["winner"][0].set("—")
        self._p2_step_btn.config(state="disabled")
        self._p2_auto_btn.config(state="disabled")
        self._p2_log.config(state="normal")
        self._p2_log.delete("1.0","end")
        self._p2_log.config(state="disabled")
        log_msg(self._p2_log, '// Reset. Klik "Setup Pemain".', ACCENT1)

    # ─────────────────────────────────────────────────
    #  KASUS 3: PRIORITY QUEUE
    # ─────────────────────────────────────────────────
    def _build_case3(self):
        parent = self._cases[3]
        self._p3_queue = []
        self._p3_serial = 0
        self._p3_served = 0

        hf = tk.Frame(parent, bg=BG)
        hf.pack(fill="x", pady=(0,10))
        tk.Label(hf, text="KASUS 3", bg=blend(ACCENT3, 0.2), fg=ACCENT3,
                 font=("Helvetica",8,"bold"), padx=8, pady=3).pack(side="left", padx=(0,10))
        tf = tk.Frame(hf, bg=BG)
        tf.pack(side="left")
        tk.Label(tf, text="Antrian Rumah Sakit — Priority Queue", bg=BG, fg=TEXT,
                 font=("Helvetica",14,"bold")).pack(anchor="w")
        tk.Label(tf, text="Pasien darurat didahulukan · Prioritas sama → FIFO",
                 bg=BG, fg=MUTED, font=("Helvetica",9)).pack(anchor="w")

        self._p3_vars = make_stat_row(parent, [
            ("Total Pasien:", "total"),
            ("Dilayani:", "served"),
            ("Berikutnya:", "next"),
        ])
        self._p3_vars["next"][1].config(fg=ACCENT4)

        # Legend
        lf = tk.Frame(parent, bg=BG)
        lf.pack(fill="x", pady=(0,6))
        for i, (label, col) in enumerate(zip(
            ['🔴 0=KRITIS','🟡 1=DARURAT','🔵 2=MENENGAH','🟢 3=RINGAN'],
            PRIO_COLORS
        )):
            tk.Label(lf, text=label, bg=blend(col, 0.2), fg=col,
                     font=("Helvetica",8,"bold"), padx=6, pady=2,
                     bd=1, relief="flat",
                     highlightbackground=col, highlightthickness=1
                     ).pack(side="left", padx=(0,4))

        arena = make_arena(parent, "🏥 Daftar Antrian (diurutkan prioritas + FIFO)")
        self._p3_list_frame = tk.Frame(arena, bg=PANEL)
        self._p3_list_frame.pack(fill="x")
        self._p3_empty_lbl = tk.Label(arena, text="Queue kosong — tambahkan pasien!",
                                      bg=PANEL, fg=MUTED, font=("Helvetica",9))
        self._p3_empty_lbl.pack()

        cf = tk.Frame(parent, bg=BG)
        cf.pack(fill="x", pady=(0,8))
        self._p3_name_var = tk.StringVar(value="Pasien")
        tk.Entry(cf, textvariable=self._p3_name_var, width=14,
                 bg=NODE_BG, fg=TEXT, insertbackground=TEXT,
                 relief="flat", font=("Helvetica",9),
                 highlightbackground=BORDER, highlightthickness=1
                 ).pack(side="left", padx=(0,6), ipady=4)
        self._p3_prio_var = tk.IntVar(value=0)
        prio_options = ["0 - Kritis 🔴","1 - Darurat 🟡","2 - Menengah 🔵","3 - Ringan 🟢"]
        om = tk.OptionMenu(cf, self._p3_prio_var,
                           *range(4),
                           command=lambda v: None)
        # rebuild with labels
        om.destroy()
        self._p3_prio_var = tk.StringVar(value="0")
        om2 = tk.OptionMenu(cf, self._p3_prio_var, "0","1","2","3")
        om2.config(bg=NODE_BG, fg=TEXT, highlightbackground=BORDER,
                   activebackground=NODE_BG, relief="flat", font=("Helvetica",9), width=3)
        om2["menu"].config(bg=NODE_BG, fg=TEXT)
        om2.pack(side="left", padx=(0,6))
        styled_btn(cf, "➕ Enqueue Pasien", ACCENT3, self._p3_enqueue).pack(side="left", padx=(0,6))
        self._p3_deq_btn = styled_btn(cf, "✅ Layani (Dequeue)", ACCENT5, self._p3_dequeue, "#fff")
        self._p3_deq_btn.pack(side="left", padx=(0,6))
        styled_btn(cf, "📋 Load Demo", ACCENT4, self._p3_load_demo, "#000").pack(side="left", padx=(0,6))
        styled_btn(cf, "↺ Reset", NODE_BG, self._p3_reset, TEXT).pack(side="left")

        self._p3_log = make_log(parent)
        log_msg(self._p3_log, '// Tambahkan pasien dengan prioritas berbeda!', ACCENT1)

        make_code_block(parent, """pq = BPriorityQueue(4)   # 4 level (0-3)
pq.enqueue("Budi",  3)  # ringan
pq.enqueue("Ani",   0)  # kritis!
pq.enqueue("Citra", 2)  # menengah
pq.enqueue("Dedi",  0)  # kritis!
pq.enqueue("Eka",   1)  # darurat
# → Output: Ani, Dedi, Eka, Citra, Budi""")

        self._p3_load_demo()

    def _p3_sort(self):
        self._p3_queue.sort(key=lambda x: (x['prio'], x['arrive']))

    def _p3_render(self):
        for w in self._p3_list_frame.winfo_children():
            w.destroy()
        if not self._p3_queue:
            self._p3_empty_lbl.pack()
        else:
            self._p3_empty_lbl.pack_forget()
        for i, p in enumerate(self._p3_queue):
            col = PRIO_COLORS[p['prio']]
            row = tk.Frame(self._p3_list_frame, bg=blend(col, 0.07),
                           bd=1, highlightbackground=blend(col, 0.4),
                           highlightthickness=1)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=PRIO_LABELS[p['prio']], bg=blend(col, 0.07), fg=col,
                     font=("Courier",8,"bold"), width=12).pack(side="left", padx=8, pady=5)
            tk.Label(row, text=p['name'], bg=blend(col, 0.07), fg=TEXT,
                     font=("Helvetica",10,"bold")).pack(side="left")
            if i == 0:
                tk.Label(row, text="← BERIKUTNYA", bg=blend(col, 0.07), fg=ACCENT3,
                         font=("Helvetica",8,"bold")).pack(side="right", padx=8)
        self._p3_vars["total"][0].set(str(len(self._p3_queue)))
        self._p3_vars["served"][0].set(str(self._p3_served))
        nxt = self._p3_queue[0]['name'] if self._p3_queue else "—"
        self._p3_vars["next"][0].set(nxt)
        self._p3_deq_btn.config(state="normal" if self._p3_queue else "disabled")

    def _p3_enqueue(self):
        name = self._p3_name_var.get().strip() or "Pasien"
        prio = int(self._p3_prio_var.get())
        self._p3_queue.append({'name': name, 'prio': prio, 'arrive': self._p3_serial})
        self._p3_serial += 1
        self._p3_sort()
        color = ACCENT4 if prio <= 1 else ACCENT3
        log_msg(self._p3_log, f'➕ {name} masuk — Prioritas: {PRIO_LABELS[prio]}', color)
        self._p3_render()

    def _p3_dequeue(self):
        if not self._p3_queue:
            return
        p = self._p3_queue.pop(0)
        self._p3_served += 1
        log_msg(self._p3_log, f'✅ Melayani: {p["name"]} [{PRIO_LABELS[p["prio"]]}]', ACCENT3)
        self._p3_render()

    def _p3_load_demo(self):
        demo = [('Budi',3),('Ani',0),('Citra',2),('Dedi',0),('Eka',1)]
        for name, prio in demo:
            self._p3_queue.append({'name': name, 'prio': prio, 'arrive': self._p3_serial})
            self._p3_serial += 1
        self._p3_sort()
        log_msg(self._p3_log, '📋 Demo pasien dimuat: Budi(3), Ani(0), Citra(2), Dedi(0), Eka(1)', ACCENT1)
        self._p3_render()

    def _p3_reset(self):
        self._p3_queue.clear()
        self._p3_serial = 0
        self._p3_served = 0
        self._p3_log.config(state="normal")
        self._p3_log.delete("1.0","end")
        self._p3_log.config(state="disabled")
        log_msg(self._p3_log, '// Reset.', ACCENT1)
        self._p3_render()

    # ─────────────────────────────────────────────────
    #  KASUS 4: BFS
    # ─────────────────────────────────────────────────
    def _build_case4(self):
        parent = self._cases[4]
        self._bfs_queue = []
        self._bfs_visited = set()
        self._bfs_steps = []
        self._bfs_step_idx = 0
        self._bfs_node_colors = {}

        hf = tk.Frame(parent, bg=BG)
        hf.pack(fill="x", pady=(0,10))
        tk.Label(hf, text="KASUS 4", bg=blend(ACCENT4, 0.2), fg=ACCENT4,
                 font=("Helvetica",8,"bold"), padx=8, pady=3).pack(side="left", padx=(0,10))
        tf = tk.Frame(hf, bg=BG)
        tf.pack(side="left")
        tk.Label(tf, text="BFS — Breadth-First Search", bg=BG, fg=TEXT,
                 font=("Helvetica",14,"bold")).pack(anchor="w")
        tk.Label(tf, text="Penjelajahan graf level demi level menggunakan queue",
                 bg=BG, fg=MUTED, font=("Helvetica",9)).pack(anchor="w")

        self._p4_vars = make_stat_row(parent, [
            ("Node dikunjungi:", "visited"),
            ("Queue saat ini:", "queue_disp"),
            ("Level:", "level"),
        ])
        self._p4_vars["queue_disp"][0].set("[ ]")
        self._p4_vars["level"][0].set("—")

        # Graph canvas
        garena = make_arena(parent, "🔍 Graf")
        self._p4_canvas = tk.Canvas(garena, bg=PANEL, height=220,
                                    bd=0, highlightthickness=0)
        self._p4_canvas.pack(fill="x")
        self._p4_canvas.bind("<Configure>", lambda e: self._p4_draw_graph())

        # BFS Queue arena
        qarena = make_arena(parent, "📋 BFS Queue")
        lf = tk.Frame(qarena, bg=PANEL)
        lf.pack(fill="x")
        tk.Label(lf, text="← DEPAN (diproses)", bg=PANEL, fg=ACCENT3,
                 font=("Courier",8)).pack(side="left")
        tk.Label(lf, text="BELAKANG (baru masuk) →", bg=PANEL, fg=ACCENT4,
                 font=("Courier",8)).pack(side="right")
        self._p4_track = tk.Frame(qarena, bg=PANEL, height=70)
        self._p4_track.pack(fill="x", pady=4)
        self._p4_empty_lbl = tk.Label(qarena, text="Klik node di graf atau tombol BFS",
                                      bg=PANEL, fg=MUTED, font=("Helvetica",9))
        self._p4_empty_lbl.pack()

        cf = tk.Frame(parent, bg=BG)
        cf.pack(fill="x", pady=(0,8))
        tk.Label(cf, text="Mulai dari:", bg=BG, fg=MUTED, font=("Helvetica",9)).pack(side="left", padx=(0,4))
        self._p4_start_var = tk.StringVar(value="A")
        om = tk.OptionMenu(cf, self._p4_start_var, *list(GRAPH4.keys()))
        om.config(bg=NODE_BG, fg=TEXT, highlightbackground=BORDER,
                  activebackground=NODE_BG, relief="flat", font=("Courier",10), width=3)
        om["menu"].config(bg=NODE_BG, fg=TEXT)
        om.pack(side="left", padx=(0,8))
        styled_btn(cf, "▶ Mulai BFS", ACCENT4, self._p4_start_bfs, "#000").pack(side="left", padx=(0,6))
        self._p4_step_btn = styled_btn(cf, "⏩ Next Step", ACCENT1, self._p4_step)
        self._p4_step_btn.pack(side="left", padx=(0,6))
        self._p4_step_btn.config(state="disabled")
        self._p4_auto_btn = styled_btn(cf, "⚡ Auto Run", ACCENT3, self._p4_auto)
        self._p4_auto_btn.pack(side="left", padx=(0,6))
        self._p4_auto_btn.config(state="disabled")
        styled_btn(cf, "↺ Reset", NODE_BG, self._p4_reset, TEXT).pack(side="left")

        self._p4_log = make_log(parent)
        log_msg(self._p4_log, '// Pilih node awal, lalu klik "Mulai BFS"', ACCENT1)

        make_code_block(parent, """def bfs(graph, start):
    visited = set()
    queue = Queue()
    queue.enqueue(start); visited.add(start)
    while not queue.isEmpty():
        node = queue.dequeue()  # proses node
        print(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)  # level berikutnya""")

        self.after(100, self._p4_draw_graph)

    def _p4_draw_graph(self):
        c = self._p4_canvas
        c.delete("all")
        W = c.winfo_width() or 600
        H = 220
        pad = 30
        def px(node):
            rx, ry = NODE_POS[node]
            return (pad + rx*(W-2*pad), pad + ry*(H-2*pad))
        # edges
        for u, v in EDGES4:
            x1,y1 = px(u); x2,y2 = px(v)
            col = self._bfs_node_colors.get(f"edge-{u}-{v}",
                  self._bfs_node_colors.get(f"edge-{v}-{u}", BORDER))
            w = 2.0 if col != BORDER else 1.0
            c.create_line(x1,y1,x2,y2, fill=col, width=w, tags=f"edge-{u}-{v}")
        # nodes
        for n in GRAPH4:
            x,y = px(n)
            fill_c = self._bfs_node_colors.get(f"node-fill-{n}", NODE_BG)
            stroke_c = self._bfs_node_colors.get(f"node-stroke-{n}", NODE_BD)
            r = 16
            c.create_oval(x-r,y-r,x+r,y+r, fill=fill_c, outline=stroke_c, width=2,
                          tags=f"gnode-{n}")
            c.create_text(x,y, text=n, fill="#fff", font=("Courier",11,"bold"),
                          tags=f"gnode-{n}")
            c.tag_bind(f"gnode-{n}", "<Button-1>",
                       lambda e, node=n: self._p4_start_var.set(node))

    def _p4_render_bfs_queue(self):
        for w in self._p4_track.winfo_children():
            w.destroy()
        if not self._bfs_queue:
            self._p4_empty_lbl.pack()
        else:
            self._p4_empty_lbl.pack_forget()
        for i, n in enumerate(self._bfs_queue):
            box = tk.Frame(self._p4_track, bg=blend(ACCENT4, 0.13),
                           bd=2, highlightbackground=ACCENT4,
                           highlightthickness=2, width=48, height=48)
            box.pack(side="left", padx=2)
            box.pack_propagate(False)
            tk.Label(box, text=n, bg=blend(ACCENT4, 0.13), fg=ACCENT4,
                     font=("Courier",11,"bold")).pack(expand=True)
            tk.Label(self._p4_track, text=f"[{i}]", bg=PANEL, fg=MUTED,
                     font=("Courier",7)).pack(side="left")
            if i < len(self._bfs_queue) - 1:
                tk.Label(self._p4_track, text="→", bg=PANEL, fg=MUTED,
                         font=("Helvetica",12)).pack(side="left", padx=2)
        self._p4_vars["queue_disp"][0].set(f"[ {', '.join(self._bfs_queue)} ]")
        self._p4_vars["visited"][0].set(str(len(self._bfs_visited)))

    def _p4_start_bfs(self):
        self._p4_reset()
        start = self._p4_start_var.get()
        self._bfs_queue = [start]
        self._bfs_visited = {start}
        self._bfs_node_colors[f"node-fill-{start}"] = blend(ACCENT4, 0.55)
        self._bfs_node_colors[f"node-stroke-{start}"] = ACCENT4
        # precompute
        self._bfs_steps = []
        q = deque([start]); vis = {start}
        while q:
            node = q.popleft()
            self._bfs_steps.append(('process', node, None))
            for nb in GRAPH4[node]:
                if nb not in vis:
                    vis.add(nb); q.append(nb)
                    self._bfs_steps.append(('enqueue', nb, node))
        self._bfs_step_idx = 0
        self._p4_step_btn.config(state="normal")
        self._p4_auto_btn.config(state="normal")
        log_msg(self._p4_log, f'▶ BFS mulai dari node "{start}"', ACCENT1)
        self._p4_render_bfs_queue()
        self._p4_draw_graph()

    def _p4_step(self):
        if self._bfs_step_idx >= len(self._bfs_steps):
            log_msg(self._p4_log, '✅ BFS selesai! Semua node dikunjungi.', ACCENT3)
            return
        step = self._bfs_steps[self._bfs_step_idx]
        self._bfs_step_idx += 1
        typ, node, from_node = step
        if typ == 'process':
            if self._bfs_queue:
                self._bfs_queue.pop(0)
            self._bfs_node_colors[f"node-fill-{node}"] = blend(ACCENT3, 0.45)
            self._bfs_node_colors[f"node-stroke-{node}"] = ACCENT3
            log_msg(self._p4_log, f'📍 Proses node "{node}" ← dequeue', ACCENT3)
            self._p4_vars["level"][0].set(node)
        else:
            self._bfs_queue.append(node)
            self._bfs_visited.add(node)
            self._bfs_node_colors[f"node-fill-{node}"] = blend(ACCENT4, 0.30)
            self._bfs_node_colors[f"node-stroke-{node}"] = ACCENT4
            for key in [f"edge-{from_node}-{node}", f"edge-{node}-{from_node}"]:
                self._bfs_node_colors[key] = ACCENT4
            log_msg(self._p4_log, f'➕ enqueue("{node}") — tetangga dari "{from_node}"', ACCENT1)
        self._p4_render_bfs_queue()
        self._p4_draw_graph()

    def _p4_auto(self):
        self._p4_auto_btn.config(state="disabled")
        def step():
            if self._bfs_step_idx < len(self._bfs_steps):
                self._p4_step()
                self.after(600, step)
            else:
                log_msg(self._p4_log, '✅ BFS selesai!', ACCENT3)
        step()

    def _p4_reset(self):
        self._bfs_queue = []
        self._bfs_visited = set()
        self._bfs_steps = []
        self._bfs_step_idx = 0
        self._bfs_node_colors = {}
        self._p4_step_btn.config(state="disabled")
        self._p4_auto_btn.config(state="disabled")
        for w in self._p4_track.winfo_children():
            w.destroy()
        self._p4_empty_lbl.pack()
        self._p4_vars["visited"][0].set("0")
        self._p4_vars["queue_disp"][0].set("[ ]")
        self._p4_vars["level"][0].set("—")
        self._p4_log.config(state="normal")
        self._p4_log.delete("1.0","end")
        self._p4_log.config(state="disabled")
        log_msg(self._p4_log, '// Pilih node awal, klik "Mulai BFS"', ACCENT1)
        self._p4_draw_graph()

    # ─────────────────────────────────────────────────
    #  KASUS 5: AIRPORT SIMULATION
    # ─────────────────────────────────────────────────
    def _build_case5(self):
        parent = self._cases[5]
        self._p5_queue = deque()
        self._p5_agents = []
        self._p5_tick = 0
        self._p5_total_wait = 0
        self._p5_served = 0
        self._p5_pass_id = 0
        self._p5_running = False
        self._p5_after_id = None
        self._p5_timeline_bars = []

        hf = tk.Frame(parent, bg=BG)
        hf.pack(fill="x", pady=(0,10))
        tk.Label(hf, text="KASUS 5", bg=blend(ACCENT5, 0.2), fg=ACCENT5,
                 font=("Helvetica",8,"bold"), padx=8, pady=3).pack(side="left", padx=(0,10))
        tf = tk.Frame(hf, bg=BG)
        tf.pack(side="left")
        tk.Label(tf, text="Simulasi Loket Tiket Bandara", bg=BG, fg=TEXT,
                 font=("Helvetica",14,"bold")).pack(anchor="w")
        tk.Label(tf, text="Discrete event simulation · rata-rata waktu tunggu penumpang",
                 bg=BG, fg=MUTED, font=("Helvetica",9)).pack(anchor="w")

        self._p5_vars = make_stat_row(parent, [
            ("Menit simulasi:", "tick"),
            ("Terlayani:", "served"),
            ("Avg Tunggu:", "avgwait"),
            ("In Queue:", "qsize"),
        ])
        self._p5_vars["avgwait"][1].config(fg=ACCENT4)
        self._p5_vars["avgwait"][0].set("0.00 mnt")

        # Sim grid
        sg = tk.Frame(parent, bg=BG)
        sg.pack(fill="x", pady=(0,8))
        # Left: Queue
        qp = tk.Frame(sg, bg="#060b14", bd=0,
                      highlightbackground=BORDER, highlightthickness=1)
        qp.pack(side="left", fill="both", expand=True, padx=(0,8))
        tk.Label(qp, text="ANTRIAN PENUMPANG", bg="#060b14", fg=MUTED,
                 font=("Helvetica",7,"bold")).pack(anchor="w", padx=8, pady=(8,4))
        self._p5_queue_frame = tk.Frame(qp, bg="#060b14")
        self._p5_queue_frame.pack(fill="x", padx=8)
        self._p5_qempty = tk.Label(qp, text="Kosong", bg="#060b14", fg=MUTED,
                                   font=("Helvetica",9))
        self._p5_qempty.pack(padx=8, pady=(0,8))
        # Right: Agents
        ap = tk.Frame(sg, bg="#060b14", bd=0,
                      highlightbackground=BORDER, highlightthickness=1)
        ap.pack(side="left", fill="both", expand=True)
        tk.Label(ap, text="AGEN TIKET", bg="#060b14", fg=MUTED,
                 font=("Helvetica",7,"bold")).pack(anchor="w", padx=8, pady=(8,4))
        self._p5_agents_frame = tk.Frame(ap, bg="#060b14")
        self._p5_agents_frame.pack(fill="x", padx=8, pady=(0,8))

        # Timeline
        tarena = make_arena(parent, "📊 Timeline Kedatangan")
        self._p5_timeline = tk.Canvas(tarena, bg=PANEL, height=40,
                                      bd=0, highlightthickness=0)
        self._p5_timeline.pack(fill="x")

        # Controls
        cf = tk.Frame(parent, bg=BG)
        cf.pack(fill="x", pady=(0,8))
        tk.Label(cf, text="Agen:", bg=BG, fg=MUTED, font=("Helvetica",9)).pack(side="left", padx=(0,3))
        self._p5_nagents = tk.IntVar(value=2)
        tk.Spinbox(cf, from_=1, to=5, textvariable=self._p5_nagents, width=4,
                   bg=NODE_BG, fg=TEXT, buttonbackground=NODE_BG,
                   relief="flat", font=("Courier",10)).pack(side="left", padx=(0,8))
        tk.Label(cf, text="Interval tiba:", bg=BG, fg=MUTED, font=("Helvetica",9)).pack(side="left", padx=(0,3))
        self._p5_interval = tk.IntVar(value=4)
        tk.Spinbox(cf, from_=1, to=15, textvariable=self._p5_interval, width=4,
                   bg=NODE_BG, fg=TEXT, buttonbackground=NODE_BG,
                   relief="flat", font=("Courier",10)).pack(side="left", padx=(0,8))
        tk.Label(cf, text="Layanan (mnt):", bg=BG, fg=MUTED, font=("Helvetica",9)).pack(side="left", padx=(0,3))
        self._p5_service = tk.IntVar(value=6)
        tk.Spinbox(cf, from_=1, to=20, textvariable=self._p5_service, width=4,
                   bg=NODE_BG, fg=TEXT, buttonbackground=NODE_BG,
                   relief="flat", font=("Courier",10)).pack(side="left", padx=(0,8))
        styled_btn(cf, "⚙ Setup", ACCENT5, self._p5_setup, "#fff").pack(side="left", padx=(0,6))
        self._p5_run_btn = styled_btn(cf, "▶ Jalankan", ACCENT1, self._p5_toggle)
        self._p5_run_btn.pack(side="left", padx=(0,6))
        self._p5_run_btn.config(state="disabled")
        styled_btn(cf, "↺ Reset", NODE_BG, self._p5_reset, TEXT).pack(side="left", padx=(0,8))

        # Speed
        sf = tk.Frame(cf, bg=BG)
        sf.pack(side="left")
        tk.Label(sf, text="Kecepatan:", bg=BG, fg=MUTED, font=("Helvetica",9)).pack(side="left", padx=(0,4))
        self._p5_speed = tk.IntVar(value=600)
        tk.Scale(sf, from_=100, to=1000, orient="horizontal",
                 variable=self._p5_speed, bg=BG, fg=MUTED,
                 highlightthickness=0, troughcolor=NODE_BG,
                 activebackground=ACCENT1, length=100, showvalue=False,
                 sliderlength=15).pack(side="left")

        self._p5_log = make_log(parent)
        log_msg(self._p5_log, '// Atur parameter, klik Setup lalu Jalankan!', ACCENT1)

        make_code_block(parent, """for curTime in range(numMinutes + 1):
    handleArrival(curTime)      # R1: tiba? → enqueue
    handleBeginService(curTime) # R2: agen free? → dequeue
    handleEndService(curTime)   # R3: selesai? → agen free
# avg_wait = totalWait / numServed""")

    def _p5_render_agents(self):
        for w in self._p5_agents_frame.winfo_children():
            w.destroy()
        for a in self._p5_agents:
            row = tk.Frame(self._p5_agents_frame, bg="#060b14")
            row.pack(fill="x", pady=2)
            dot = tk.Canvas(row, width=10, height=10, bg="#060b14",
                            highlightthickness=0)
            dot.create_oval(1,1,9,9, fill=ACCENT3 if a['busy'] else "#334155")
            dot.pack(side="left", padx=(0,6))
            text = f"Agen {a['id']}: " + (f"🧳 {a['passenger']}" if a['busy'] else "⏳ Menunggu")
            tk.Label(row, text=text, bg="#060b14", fg=TEXT,
                     font=("Courier",9)).pack(side="left")

    def _p5_render_queue(self):
        for w in self._p5_queue_frame.winfo_children():
            w.destroy()
        q_list = list(self._p5_queue)
        if not q_list:
            self._p5_qempty.pack()
        else:
            self._p5_qempty.pack_forget()
            for i, p in enumerate(q_list[:10]):
                col = ACCENT4 if i == 0 else MUTED
                tk.Label(self._p5_queue_frame,
                         text=f"[{i}] {p['name']} (tiba:{p['arrive_at']})",
                         bg="#060b14", fg=col, font=("Courier",8)
                         ).pack(anchor="w")
            if len(q_list) > 10:
                tk.Label(self._p5_queue_frame,
                         text=f"+{len(q_list)-10} lainnya...",
                         bg="#060b14", fg=MUTED, font=("Courier",8)
                         ).pack(anchor="w")
        self._p5_vars["qsize"][0].set(str(len(self._p5_queue)))

    def _p5_setup(self):
        self._p5_reset()
        n_agents = self._p5_nagents.get()
        self._p5_agents = [
            {'id': i+1, 'busy': False, 'passenger': None, 'finish_at': 0}
            for i in range(n_agents)
        ]
        self._p5_render_agents()
        self._p5_run_btn.config(state="normal")
        log_msg(self._p5_log,
                f'⚙ Setup: {n_agents} agen, interval ~{self._p5_interval.get()} mnt, '
                f'layanan ~{self._p5_service.get()} mnt', ACCENT1)

    def _p5_tick_fn(self):
        if not self._p5_running:
            return
        self._p5_tick += 1
        t = self._p5_tick
        self._p5_vars["tick"][0].set(str(t))

        # R1: arrival
        if random.random() < 1 / self._p5_interval.get():
            self._p5_pass_id += 1
            pid = self._p5_pass_id
            pax = {'id': pid, 'name': f'P{pid:03d}', 'arrive_at': t, 'wait_start': t}
            self._p5_queue.append(pax)
            # timeline bar
            bar_h = int(8 + random.random() * 12)
            W = self._p5_timeline.winfo_width() or 400
            x = (len(self._p5_timeline_bars) * 8) % (W - 10)
            y0 = 38 - bar_h
            rid = self._p5_timeline.create_rectangle(x, y0, x+6, 38,
                                                      fill=ACCENT1, outline="")
            self._p5_timeline_bars.append(rid)
            log_msg(self._p5_log,
                    f'[t={t}] ✈ {pax["name"]} tiba → enqueue (antrian:{len(self._p5_queue)})',
                    ACCENT1)

        # R3: end service
        for a in self._p5_agents:
            if a['busy'] and t >= a['finish_at']:
                self._p5_served += 1
                log_msg(self._p5_log, f'[t={t}] ✅ Agen {a["id"]} selesai: {a["passenger"]}', ACCENT3)
                a['busy'] = False; a['passenger'] = None; a['finish_at'] = 0

        # R2: begin service
        for a in self._p5_agents:
            if not a['busy'] and self._p5_queue:
                pax = self._p5_queue.popleft()
                waited = t - pax['wait_start']
                self._p5_total_wait += waited
                a['busy'] = True; a['passenger'] = pax['name']
                a['finish_at'] = t + self._p5_service.get() + random.randint(-1, 1)
                log_msg(self._p5_log,
                        f'[t={t}] 🛂 Agen {a["id"]} melayani {pax["name"]} (tunggu:{waited} mnt)',
                        ACCENT4)

        self._p5_render_agents()
        self._p5_render_queue()
        self._p5_vars["served"][0].set(str(self._p5_served))
        avg = f'{self._p5_total_wait/self._p5_served:.2f} mnt' if self._p5_served > 0 else '0.00 mnt'
        self._p5_vars["avgwait"][0].set(avg)

        if t >= 120:
            self._p5_stop()
            log_msg(self._p5_log, '[t=120] ⏹ Simulasi selesai (120 menit)', ACCENT3)
            return

        spd = max(50, 1100 - self._p5_speed.get())
        self._p5_after_id = self.after(spd, self._p5_tick_fn)

    def _p5_toggle(self):
        if self._p5_running:
            self._p5_stop()
        else:
            self._p5_start()

    def _p5_start(self):
        self._p5_running = True
        self._p5_run_btn.config(text="⏸ Pause")
        self._p5_tick_fn()

    def _p5_stop(self):
        self._p5_running = False
        self._p5_run_btn.config(text="▶ Jalankan")
        if self._p5_after_id:
            self.after_cancel(self._p5_after_id)

    def _p5_reset(self):
        self._p5_stop()
        self._p5_queue.clear()
        self._p5_agents = []
        self._p5_tick = 0
        self._p5_total_wait = 0
        self._p5_served = 0
        self._p5_pass_id = 0
        self._p5_timeline_bars = []
        self._p5_vars["tick"][0].set("0")
        self._p5_vars["served"][0].set("0")
        self._p5_vars["avgwait"][0].set("0.00 mnt")
        self._p5_vars["qsize"][0].set("0")
        for w in self._p5_agents_frame.winfo_children():
            w.destroy()
        for w in self._p5_queue_frame.winfo_children():
            w.destroy()
        self._p5_qempty.pack()
        self._p5_timeline.delete("all")
        self._p5_run_btn.config(state="disabled", text="▶ Jalankan")
        self._p5_log.config(state="normal")
        self._p5_log.delete("1.0","end")
        self._p5_log.config(state="disabled")
        log_msg(self._p5_log, '// Reset. Klik Setup untuk memulai ulang.', ACCENT1)


# ═══════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════
if __name__ == "__main__":
    app = QueueVisualizer()
    app.mainloop()
