grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

for y, linha in enumerate(grid):
    for x, coluna in enumerate(linha):
        print(coluna)
