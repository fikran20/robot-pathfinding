import streamlit as st
import numpy as np

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Jalur Terpendek Robot", layout="centered")

# --- DATASET (10 Grid 10x10) ---
datasets = [
    [[0,0,0,0,1,0,0,0,0,0], [0,1,1,0,1,0,1,1,1,0], [0,0,0,0,0,0,0,0,1,0], [1,1,1,1,1,1,1,0,1,0], [0,0,0,0,1,0,0,0,0,0], [0,1,1,0,1,0,1,1,1,1], [0,0,0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1,1,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0]],
    # ... (Dataset lainnya disingkat untuk efisiensi, Anda bisa mengisi matriks 10x10 di sini)
]
# Untuk simulasi, kita buat generator dataset acak sederhana jika index > 0
for i in range(9):
    datasets.append(np.random.choice([0, 1], size=(10, 10), p=[0.7, 0.3]).tolist())
    datasets[-1][0][0] = 0 # Pastikan start aman
    datasets[-1][9][9] = 0 # Pastikan finish aman

# --- LOGIKA BACKTRACKING ---
def solve_path(grid):
    rows, cols = 10, 10
    shortest_path = []
    
    def is_safe(r, c, visited):
        return 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0 and not visited[r][c]

    def backtrack(r, c, visited, current_path):
        nonlocal shortest_path
        if (r, c) == (9, 9):
            if not shortest_path or len(current_path) < len(shortest_path):
                shortest_path = list(current_path)
            return
        
        if shortest_path and len(current_path) >= len(shortest_path):
            return

        for nr, nc in [(r+1, c), (r, c+1), (r-1, c), (r, c-1)]:
            if is_safe(nr, nc, visited):
                visited[nr][nc] = True
                current_path.append((nr, nc))
                backtrack(nr, nc, visited, current_path)
                current_path.pop()
                visited[nr][nc] = False

    visited = [[False]*cols for _ in range(rows)]
    visited[0][0] = True
    backtrack(0, 0, visited, [(0,0)])
    return shortest_path

# --- INTERFACE STREAMLIT ---
st.title("🤖 Robot Pathfinding")
st.sidebar.header("Kontrol")
data_idx = st.sidebar.selectbox("Pilih Dataset", range(1, 11)) - 1
grid = datasets[data_idx]

if st.sidebar.button("Cari Jalur Terpendek"):
    path = solve_path(grid)
    if path:
        st.success(f"Jalur ditemukan! Panjang: {len(path)-1} langkah")
    else:
        st.error("Jalur buntu!")
else:
    path = []

# --- VISUALISASI GRID ---
def draw_grid(grid, path):
    display_grid = np.array(grid, dtype=object)
    for r in range(10):
        cols_ui = st.columns(10)
        for c in range(10):
            color = "⬜" # Jalan
            if grid[r][c] == 1: color = "⬛" # Tembok
            if (r, c) == (0, 0): color = "🟩X" # Start
            if (r, c) == (9, 9): color = "🟥Y" # Finish
            if (r, c) in path and (r,c) != (0,0) and (r,c) != (9,9): color = "🟨" # Jalur
            cols_ui[c].write(color)

draw_grid(grid, path)