import cv2
import numpy as np
import os
from collections import deque

ORIGINAL_FOLDER = r"D:\ProjectX\T1\X task 1 Windows\mazes"
CLEANED_FOLDER = r"D:\ProjectX\T1\X task 1 Windows\inverted"
SOLVED_FOLDER = r"D:\ProjectX\T1\X task 1 Windows\solved"
os.makedirs(SOLVED_FOLDER, exist_ok=True)
MOD = 1000000007
IMAGE_SIZE = 800
GRID_SIZE = 40
CELL_SIZE = IMAGE_SIZE // GRID_SIZE  # 20
def image_to_grid(img):
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            y = r * CELL_SIZE + CELL_SIZE // 2
            x = c * CELL_SIZE + CELL_SIZE // 2
            if img[y, x] > 127:
                grid[r][c] = 1
            else:
                grid[r][c] = 0
    return grid

def bfs_shortest_path(grid):
    n = GRID_SIZE
    m = GRID_SIZE
    if grid[0][0] == 0:
        return -1, None
    q = deque()
    q.append((0, 0))
    visited = [[False] * m for _ in range(n)]
    parent = [[None] * m for _ in range(n)]
    visited[0][0] = True
    directions = [(1, 0),(-1, 0),(0, 1),(0, -1)]
    while q:
        r, c = q.popleft()
        if r == n - 1 and c == m - 1:
            path = []
            cur = (r, c)
            while cur is not None:
                path.append(cur)
                cur = parent[cur[0]][cur[1]]
            path.reverse()
            return len(path), path
        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
            if (
                0 <= nr < n and
                0 <= nc < m and
                grid[nr][nc] == 1 and
                not visited[nr][nc]
            ):
                visited[nr][nc] = True
                parent[nr][nc] = (r, c)
                q.append((nr, nc))
    return -1, None

def draw_path(image, path):
    points = []
    for r, c in path:
        x = c * CELL_SIZE + CELL_SIZE // 2
        y = r * CELL_SIZE + CELL_SIZE // 2
        points.append((x, y))
    for i in range(len(points) - 1):
        cv2.line(
            image,
            points[i],
            points[i + 1],
            (0, 255, 0), 
            5
        )
    return image
product = 1
solvable_count = 0
for filename in sorted(os.listdir(CLEANED_FOLDER)):
    if not filename.lower().endswith(".png"):
        continue
    cleaned_path = os.path.join(CLEANED_FOLDER, filename)
    original_path = os.path.join(ORIGINAL_FOLDER, filename)
    cleaned_img = cv2.imread(cleaned_path, cv2.IMREAD_GRAYSCALE)
    if cleaned_img is None:
        print(f"Could not read {filename}")
        continue
    grid = image_to_grid(cleaned_img)
    length, path = bfs_shortest_path(grid)
    if length == -1:
        print(f"{filename}: UNSOLVABLE")
        continue
    solvable_count += 1
    product = (product * length) % MOD
    original_img = cv2.imread(original_path)
    if original_img is not None:
        solved_img = draw_path(original_img, path)
        output_path = os.path.join(
            SOLVED_FOLDER,
            filename
        )
        cv2.imwrite(output_path, solved_img)
    print(f"{filename}: "f"length={length}, "f"current_product={product}"
    )
print("SOLVABLE MAZES:", solvable_count)
print("FINAL PRODUCT MOD 1e9+7 =", product)