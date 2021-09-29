grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

for y, linha in enumerate(grid):
    for x, _ in enumerate(linha):
        print(x, y)
