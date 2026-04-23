import random

def generate_data():
    print("\n--- Генерація випадкових даних ---")

    m = int(input("m (кількість фракцій): "))

    n_min, n_max = 10, 100

    change = input(f"Змінити діапазон n_i? (за замовчуванням [{n_min}, {n_max}]) y/n: ")

    if change.lower() == 'y':
        n_min = int(input("n_min: "))
        n_max = int(input("n_max: "))

    n = [random.randint(n_min, n_max) for _ in range(m)]

    matrix_c = []
    for i in range(m):
        for j in range(m):
            if i == j:
                matrix_c.append(1.0)
            else:
                matrix_c.append(round(random.uniform(0, 1), 2))

    matrix_r = []
    for i in range(m):
        for j in range(m):
            if i == j:
                matrix_r.append(0.0)
            else:
                matrix_r.append(round(random.uniform(0, 1), 2))

    t = round(random.uniform(0, 1), 2)
    d = round(random.uniform(0, 1), 2)

    print("\n--- Згенерована задача ---")
    print("m =", m)
    print("n =", n)

    print("\nMatrix C:")
    for i in range(m):
        print(matrix_c[i*m:(i+1)*m])

    print("\nMatrix R:")
    for i in range(m):
        print(matrix_r[i*m:(i+1)*m])

    print("\nt =", t)
    print("d =", d)

    return m, n, matrix_c, matrix_r, t, d