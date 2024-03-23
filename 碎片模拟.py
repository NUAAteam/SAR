import asyncio
import math
import random
import matplotlib.pyplot as plt

async def calculate_values(m, n, dm, dn, k, theta):
    R_distance2 = [[0.0 for _ in range(n)] for _ in range(m)]
    p_array = [[0.0 for _ in range(n)] for _ in range(m)]
    X_array = [[0.0 for _ in range(n)] for _ in range(m)]

    for i in range(m):
        for j in range(n):
            R_distance2[i][j] = (dm*(i-(m-1)/2))**2+ (dn*(j-(n-1)/2))**2
            p_array[i][j] = math.exp(-R_distance2[i][j]/k/theta)
            X_array[i][j] = 1-int(random.random()+1-p_array[i][j])

    Picture_x = [[0.0 for _ in range(n)] for _ in range(m)]
    Picture_y = [[0.0 for _ in range(n)] for _ in range(m)]

    tasks = []
    loop = asyncio.get_event_loop()

    for i in range(m):
        for j in range(n):
            if X_array[i][j] == 1:
                tasks.append(asyncio.ensure_future(plt.scatter(i , j , s = .5 ,color = 'b')))

    await asyncio.gather(*tasks)

async def main():
    m = 10
    n = 10
    dm = 1
    dn = 1
    k = 500
    theta = 1

    await calculate_values(m, n, dm, dn, k, theta)
    plt.show()

asyncio.run(main())