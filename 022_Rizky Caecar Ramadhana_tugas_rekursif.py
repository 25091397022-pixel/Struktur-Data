# ============================================================
#  TUGAS REKURSI - Tiga Soal Klasik
#  1. N-Queens Problem
#  2. Knight's Tour (Tur Kuda)
#  3. Knapsack Problem
# ============================================================


# ============================================================
#  SOAL 1 : N-QUEENS PROBLEM
# ============================================================

class NQueensBoard:
    """
    Representasi papan n×n untuk masalah N-Queens.
    Menyimpan posisi ratu menggunakan array 1-D (seperti yang
    dijelaskan di buku: indeks ke-col menyimpan baris ratu).
    """

    def __init__(self, n):
        self._size = n
        # -1 berarti kolom belum terisi ratu
        self._queens = [-1] * n
        self._num_queens = 0

    def size(self):
        return self._size

    def numQueens(self):
        return self._num_queens

    def unguarded(self, row, col):
        """Kembalikan True jika posisi (row, col) tidak diserang ratu manapun."""
        for c in range(col):
            r = self._queens[c]
            # Cek baris yang sama atau diagonal
            if r == row or abs(r - row) == abs(c - col):
                return False
        return True

    def placeQueen(self, row, col):
        self._queens[col] = row
        self._num_queens += 1

    def removeQueen(self, row, col):
        self._queens[col] = -1
        self._num_queens -= 1

    def reset(self):
        self._queens = [-1] * self._size
        self._num_queens = 0

    def draw(self):
        """Cetak papan dengan Q = ratu, . = kosong."""
        n = self._size
        print("+" + "---+" * n)
        for r in range(n):
            row_str = "|"
            for c in range(n):
                if self._queens[c] == r:
                    row_str += " Q |"
                else:
                    row_str += " . |"
            print(row_str)
            print("+" + "---+" * n)


def solveNQueens(board, col):
    """
    Fungsi rekursif untuk menyelesaikan N-Queens.
    Mengembalikan True jika solusi ditemukan, False jika tidak.
    """
    # Base case: semua ratu telah ditempatkan
    if board.numQueens() == board.size():
        return True

    for row in range(board.size()):
        if board.unguarded(row, col):
            board.placeQueen(row, col)
            if solveNQueens(board, col + 1):
                return True
            board.removeQueen(row, col)

    # Tidak ada posisi valid di kolom ini → backtrack
    return False


def run_nqueens():
    print("=" * 55)
    print("          SOAL 1 : N-QUEENS PROBLEM")
    print("=" * 55)
    try:
        n = int(input("Masukkan ukuran papan (n): "))
        if n < 1:
            print("Ukuran papan harus >= 1.")
            return
    except ValueError:
        print("Input tidak valid.")
        return

    board = NQueensBoard(n)
    print(f"\nMencari solusi untuk {n}-Queens ...\n")

    if solveNQueens(board, 0):
        print(f"Solusi ditemukan! Posisi ratu (per kolom): {board._queens}\n")
        board.draw()
    else:
        print("Tidak ada solusi untuk papan berukuran tersebut.")


# ============================================================
#  SOAL 2 : KNIGHT'S TOUR (TUR KUDA)
# ============================================================

# 8 kemungkinan gerakan kuda dalam catur
KNIGHT_MOVES = [
    (-2, -1), (-2, +1),
    (-1, -2), (-1, +2),
    (+1, -2), (+1, +2),
    (+2, -1), (+2, +1),
]


def solveKnightsTour(board, row, col, move_num, n):
    """
    Fungsi rekursif backtracking untuk Tur Kuda.
    board  : papan n×n (nilai = urutan langkah, 0 = belum dikunjungi)
    row,col: posisi kuda saat ini
    move_num: nomor langkah saat ini (1 = pertama)
    Mengembalikan True jika tur berhasil diselesaikan.
    """
    # Base case: semua petak telah dikunjungi
    if move_num > n * n:
        return True

    for dr, dc in KNIGHT_MOVES:
        next_row = row + dr
        next_col = col + dc
        if 0 <= next_row < n and 0 <= next_col < n and board[next_row][next_col] == 0:
            board[next_row][next_col] = move_num
            if solveKnightsTour(board, next_row, next_col, move_num + 1, n):
                return True
            # Backtrack
            board[next_row][next_col] = 0

    return False


def print_knights_board(board, n):
    """Cetak urutan langkah kuda di papan."""
    cell_w = len(str(n * n)) + 2
    sep = "+" + ("-" * cell_w + "+") * n
    print(sep)
    for r in range(n):
        row_str = "|"
        for c in range(n):
            row_str += str(board[r][c]).center(cell_w) + "|"
        print(row_str)
        print(sep)


def run_knights_tour():
    print("\n" + "=" * 55)
    print("       SOAL 2 : KNIGHT'S TOUR (TUR KUDA)")
    print("=" * 55)
    try:
        n   = int(input("Ukuran papan (n, disarankan 5-8): "))
        sr  = int(input(f"Baris awal kuda (0 – {n-1}): "))
        sc  = int(input(f"Kolom awal kuda (0 – {n-1}): "))
    except ValueError:
        print("Input tidak valid.")
        return

    if not (0 <= sr < n and 0 <= sc < n):
        print("Posisi awal di luar papan.")
        return

    # Inisialisasi papan; tandai posisi awal dengan langkah ke-1
    board = [[0] * n for _ in range(n)]
    board[sr][sc] = 1

    print(f"\nMencari Tur Kuda {n}×{n} mulai dari ({sr}, {sc}) ...\n")

    if solveKnightsTour(board, sr, sc, 2, n):
        print("Solusi ditemukan! Urutan langkah kuda:\n")
        print_knights_board(board, n)
        # Tampilkan daftar langkah
        moves_list = [None] * (n * n)
        for r in range(n):
            for c in range(n):
                moves_list[board[r][c] - 1] = (r, c)
        print("\nDaftar langkah (langkah : baris, kolom):")
        for i, pos in enumerate(moves_list):
            print(f"  Langkah {i+1:3d}: baris={pos[0]}, kolom={pos[1]}")
    else:
        print("Tidak ada solusi Tur Kuda untuk konfigurasi ini.")
        print("(Coba posisi awal yang berbeda atau ukuran papan >= 5.)")


# ============================================================
#  SOAL 3 : KNAPSACK PROBLEM
# ============================================================

def knapsack(items, index, remaining, chosen):
    """
    Fungsi rekursif untuk Knapsack (0/1).
    items     : list berat barang
    index     : indeks barang yang sedang dipertimbangkan
    remaining : sisa kapasitas knapsack
    chosen    : list yang menyimpan barang-barang yang dipilih
    Mengembalikan True jika kombinasi yang mencapai tepat 'target' ditemukan,
    atau kombinasi terbaik (≤ target) jika mode best-fit diaktifkan.
    """
    # Base case 1: sisa kapasitas tepat nol → solusi sempurna
    if remaining == 0:
        return True

    # Base case 2: tidak ada barang lagi yang bisa dicoba
    if index >= len(items) or remaining < 0:
        return False

    # Coba masukkan barang ke-index
    if items[index] <= remaining:
        chosen.append(items[index])
        if knapsack(items, index + 1, remaining - items[index], chosen):
            return True
        chosen.pop()  # backtrack

    # Lewati barang ke-index
    return knapsack(items, index + 1, remaining, chosen)


def knapsack_best(items, index, remaining, chosen, best):
    """
    Versi knapsack yang mencari kombinasi dengan total berat
    semaksimal mungkin (≤ target), bukan harus tepat sama.
    best[0] menyimpan kombinasi terbaik yang ditemukan sejauh ini.
    """
    current_weight = sum(chosen)
    if current_weight > best[0][0]:
        best[0] = (current_weight, list(chosen))

    if index >= len(items) or remaining <= 0:
        return

    if items[index] <= remaining:
        chosen.append(items[index])
        knapsack_best(items, index + 1, remaining - items[index], chosen, best)
        chosen.pop()

    knapsack_best(items, index + 1, remaining, chosen, best)


def run_knapsack():
    print("\n" + "=" * 55)
    print("          SOAL 3 : KNAPSACK PROBLEM")
    print("=" * 55)
    print("Contoh default: berat target=30, barang=[2,5,6,9,12,14,20]")
    use_default = input("Gunakan contoh default? (y/n): ").strip().lower()

    if use_default == 'y':
        target = 30
        weights = [2, 5, 6, 9, 12, 14, 20]
    else:
        try:
            target = int(input("Masukkan berat target knapsack: "))
            raw = input("Masukkan berat barang (pisahkan dengan koma, contoh: 2,5,9): ")
            weights = [int(x.strip()) for x in raw.split(",")]
        except ValueError:
            print("Input tidak valid.")
            return

    print(f"\nBerat target  : {target}")
    print(f"Daftar barang : {weights}")
    print(f"Jumlah barang : {len(weights)}\n")

    # Coba cari kombinasi yang tepat sama dengan target
    chosen_exact = []
    found_exact = knapsack(weights, 0, target, chosen_exact)

    if found_exact:
        print(f"✓ Solusi TEPAT ditemukan!")
        print(f"  Barang yang dipilih : {chosen_exact}")
        print(f"  Total berat         : {sum(chosen_exact)}")
    else:
        print("✗ Tidak ada kombinasi yang beratnya TEPAT sama dengan target.")
        print("  Mencari kombinasi terbaik (berat ≤ target) ...\n")
        best = [(0, [])]
        knapsack_best(weights, 0, target, [], best)
        best_weight, best_items = best[0]
        if best_items:
            print(f"  Kombinasi terbaik   : {best_items}")
            print(f"  Total berat terbaik : {best_weight}  (sisa: {target - best_weight})")
        else:
            print("  Tidak ada barang yang bisa dimasukkan.")


# ============================================================
#  MAIN – jalankan semua soal
# ============================================================

def main():
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        TUGAS REKURSI – TIGA SOAL KLASIK             ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    run_nqueens()
    run_knights_tour()
    run_knapsack()

    print("\n" + "=" * 55)
    print("         Semua tugas selesai dikerjakan!")
    print("=" * 55)


if __name__ == "__main__":
    main()
