import AG

entradas = [[80, 1, 100, 100, "BLXab", 1], [80, 5, 100, 100, "BLXab", 1],
            [80, 10, 100, 100, "BLXab", 1], [100, 1, 100, 100, "BLXab", 1],
            [100, 5, 100, 100, "BLXab", 1], [100, 10, 100, 100, "BLXab", 1]]

for i in entradas:
    fitness, media = AG.AG_real(i[0], i[1], i[2], i[3], i[4], i[5])