import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

class GameOfLifePro:
    def __init__(self, rows=50, cols=50, density=0.2):
        self.rows = rows
        self.cols = cols
        # Inisialisasi grid dengan pola acak langsung saat objek dibuat
        self.grid = np.random.choice([0, 1], size=(rows, cols), p=[1-density, density])

    def next_generation(self):
        """
        Menghitung generasi berikutnya menggunakan vektorisasi NumPy (tanpa explicit loop).
        """
        # Menghitung tetangga dengan menggeser grid ke 8 arah
        # Ini jauh lebih cepat daripada looping manual
        neighbors = (
            np.roll(np.roll(self.grid, 1, axis=0), 1, axis=1) +  # atas-kiri
            np.roll(self.grid, 1, axis=0) +                     # atas
            np.roll(np.roll(self.grid, 1, axis=0), -1, axis=1) + # atas-kanan
            np.roll(self.grid, 1, axis=1) +                     # kiri
            np.roll(self.grid, -1, axis=1) +                    # kanan
            np.roll(np.roll(self.grid, -1, axis=0), 1, axis=1) + # bawah-kiri
            np.roll(self.grid, -1, axis=0) +                    # bawah
            np.roll(np.roll(self.grid, -1, axis=0), -1, axis=1)  # bawah-kanan
        )

        # Menerapkan aturan Conway
        # 1. Tetangga == 3 -> Hidup (baik sel lama hidup atau mati)
        # 2. Tetangga == 2 dan Sel Lama Hidup -> Tetap Hidup
        new_grid = np.where((neighbors == 3) | ((self.grid == 1) & (neighbors == 2)), 1, 0)
        self.grid = new_grid

    def add_pattern(self, pattern, r_off, c_off):
        """Menambahkan pola kustom pada koordinat tertentu"""
        try:
            r, c = pattern.shape
            self.grid[r_off:r_off+r, c_off:c_off+c] = pattern
        except ValueError:
            print("Pola terlalu besar untuk posisi tersebut!")

    def animate(self, frames=200, interval=50):
        fig, ax = plt.subplots(figsize=(8, 8))
        # Menggunakan warna custom: Hijau neon untuk sel hidup, Hitam untuk mati
        cmap = ListedColormap(['#1a1a1a', '#39FF14'])
        img = ax.imshow(self.grid, cmap=cmap, interpolation='nearest')
        
        ax.set_axis_off()
        title = ax.set_title("Game of Life - Generasi 0")

        def update(frame):
            self.next_generation()
            img.set_array(self.grid)
            title.set_text(f"Game of Life - Generasi {frame}")
            return [img, title]

        ani = animation.FuncAnimation(fig, update, frames=frames, 
                                     interval=interval, blit=True)
        plt.show()

# --- Pola Kustom ---
GOSPER_GLIDER_GUN = np.zeros((9, 36))
gun_coords = [
    (5,1), (5,2), (6,1), (6,2), (5,11), (6,11), (7,11), (4,12), (8,12), (3,13), (9,13), 
    (3,14), (9,14), (6,15), (4,16), (8,16), (5,17), (6,17), (7,17), (6,18), (3,21), 
    (4,21), (5,21), (3,22), (4,22), (5,22), (2,23), (6,23), (1,25), (2,25), (6,25), 
    (7,25), (3,35), (4,35), (3,36), (4,36)
]
for r, c in gun_coords: GOSPER_GLIDER_GUN[r-1, c-1] = 1

# --- Eksekusi ---
if __name__ == "__main__":
    # Buat grid yang lebih besar (misal 80x80)
    game = GameOfLifePro(80, 80, density=0.1)
    
    # Tambahkan pola legendaris Gosper Glider Gun
    game.add_pattern(GOSPER_GLIDER_GUN, 10, 10)
    
    # Jalankan animasi
    game.animate(frames=500, interval=30)
