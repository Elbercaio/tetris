grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
#
# for y, linha in enumerate(grid):
#     for x, coluna in enumerate(linha):
#         print(coluna)

accepted_pos = [(j, i) for j in range(10) for i in range(20)
                if grid[i][j] == (0, 0, 0)]

print(len(accepted_pos))
