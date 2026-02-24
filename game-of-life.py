import pygame
import numpy as np

# Konfigurasi Dasar
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 10
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 10

# Warna
COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE = (170, 170, 170)
COLOR_ALIVE = (255, 255, 255)

def draw_grid(screen, grid):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = COLOR_ALIVE if grid[row, col] == 1 else COLOR_BG
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))

def update_grid(grid):
    new_grid = grid.copy()
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            # Menghitung tetangga yang hidup (8 arah)
            # Menggunakan modulo agar grid bersifat "wrap-around" (donat)
            neighbors = np.sum(grid[row-1:row+2, col-1:col+2]) - grid[row, col]

            # Aturan Conway
            if grid[row, col] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[row, col] = 0
            else:
                if neighbors == 3:
                    new_grid[row, col] = 1
    return new_grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Inisialisasi grid secara acak
    grid = np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH), p=[0.8, 0.2])
    
    running = True
    playing = False

    while running:
        clock.tick(FPS)
        screen.fill(COLOR_GRID)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Tekan SPACE untuk pause/play
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                # Tekan R untuk reset acak
                if event.key == pygame.K_r:
                    grid = np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH), p=[0.8, 0.2])

        if playing:
            grid = update_grid(grid)

        draw_grid(screen, grid)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
