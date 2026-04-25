import random
from itertools import combinations


def _build_matrices(m, n, t, all_pairs, c_good_pairs, r_good_pairs):
    """Генерує матриці C та R і підбирає d так, щоб гарантовано існувала допустима коаліція."""

    matrix_c = [0.0] * (m * m)
    for i in range(m):
        matrix_c[i*m + i] = 1.0
    for (i, j) in all_pairs:
        if (i, j) in c_good_pairs:
            val_c = round(random.uniform(t, 1), 2)
        else:
            val_c = round(random.uniform(0, t), 2)
        matrix_c[i*m + j] = val_c
        matrix_c[j*m + i] = val_c

    # Генеруємо r без прив'язки до d — рівномірно з різними діапазонами для "хороших" пар
    r_raw = {}
    for (i, j) in all_pairs:
        if (i, j) in r_good_pairs:
            val_r = round(random.uniform(0.0, 0.4), 2)
        else:
            val_r = round(random.uniform(0.3, 1.0), 2)
        r_raw[(i, j)] = val_r

    matrix_r = [0.0] * (m * m)
    for i in range(m):
        matrix_r[i*m + i] = 0.0
    for (i, j) in all_pairs:
        v = r_raw[(i, j)]
        matrix_r[i*m + j] = v
        matrix_r[j*m + i] = v

    # Знаходимо мінімальний ризик серед усіх підмножин, що дають більшість.
    # d встановлюємо >= цього ризику + випадковий буфер.
    # Так гарантується, що хоча б одна коаліція пройде обмеження на ризик.
    N = sum(n)
    threshold = N * 0.5 + 1
    min_risk = float('inf')
    for size in range(1, m + 1):
        for combo in combinations(range(m), size):
            if sum(n[i] for i in combo) >= threshold:
                risk = sum(r_raw.get((min(i, j), max(i, j)), 0)
                           for i, j in combinations(combo, 2))
                if risk < min_risk:
                    min_risk = risk

    buffer = random.uniform(0.03, 0.4)
    d = round(min_risk + buffer, 2)

    return matrix_c, matrix_r, d


def generate_data():
    print("\n--- Генерація випадкових даних ---")

    m = int(input("m (кількість фракцій): "))

    n_min, n_max = 10, 100

    change = input(f"Змінити діапазон n_i? (за замовчуванням [{n_min}, {n_max}]) y/n: ")

    if change.lower() == 'y':
        n_min = int(input("n_min: "))
        n_max = int(input("n_max: "))

    n = [random.randint(n_min, n_max) for _ in range(m)]

    # t в помірному діапазоні — не надто велике, щоб умова ядра не була нереально жорсткою
    t = round(random.uniform(0.3, 0.6), 2)

    total_pairs = m * (m - 1) // 2
    c_good = int(total_pairs * 0.85)
    r_good = int(total_pairs * 0.6)

    all_pairs = [(i, j) for i in range(m) for j in range(i + 1, m)]
    random.shuffle(all_pairs)

    c_good_pairs = set(map(tuple, [all_pairs[k] for k in range(c_good)]))
    r_good_pairs = set(map(tuple, [all_pairs[k] for k in range(r_good)]))

    matrix_c, matrix_r, d = _build_matrices(m, n, t, all_pairs, c_good_pairs, r_good_pairs)

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


def generate_test_data(m, n_min, n_max, t_min=0, t_max=1, d_min=0, d_max=1):
    n = [random.randint(n_min, n_max) for _ in range(m)]

    # Якщо діапазон t не задано явно — звужуємо до помірного,
    # щоб умова сумісності з ядром не ставала нереально жорсткою
    if t_min == 0 and t_max == 1:
        t = round(random.uniform(0.3, 0.6), 2)
    else:
        t = round(random.uniform(t_min, t_max), 2)

    total_pairs = m * (m - 1) // 2
    c_good = int(total_pairs * 0.85)
    r_good = int(total_pairs * 0.6)

    all_pairs = [(i, j) for i in range(m) for j in range(i + 1, m)]
    random.shuffle(all_pairs)

    c_good_pairs = set(map(tuple, [all_pairs[k] for k in range(c_good)]))
    r_good_pairs = set(map(tuple, [all_pairs[k] for k in range(r_good)]))

    if d_min == 0 and d_max == 1:
        # Автоматичний вибір d: гарантуємо, що хоча б одна коаліція проходить
        matrix_c, matrix_r, d = _build_matrices(m, n, t, all_pairs, c_good_pairs, r_good_pairs)
    else:
        # Діапазон d задано явно — не перевизначаємо
        matrix_c = [0.0] * (m * m)
        for i in range(m):
            matrix_c[i*m + i] = 1.0
        for (i, j) in all_pairs:
            if (i, j) in c_good_pairs:
                val_c = round(random.uniform(t, 1), 2)
            else:
                val_c = round(random.uniform(0, t), 2)
            matrix_c[i*m + j] = val_c
            matrix_c[j*m + i] = val_c

        d = round(random.uniform(d_min, d_max), 2)

        matrix_r = [0.0] * (m * m)
        for i in range(m):
            matrix_r[i*m + i] = 0.0
        for (i, j) in all_pairs:
            if (i, j) in r_good_pairs:
                val_r = round(random.uniform(0, d), 2)
            else:
                val_r = round(random.uniform(d, 1), 2)
            matrix_r[i*m + j] = val_r
            matrix_r[j*m + i] = val_r

    return m, n, matrix_c, matrix_r, t, d


def read_int_list(prompt, expected_len):
    while True:
        try:
            data = list(map(int, input(prompt).split()))
            if len(data) != expected_len:
                print("Неправильна кількість елементів")
                continue
            return data
        except:
            print("Помилка вводу. Спробуйте ще раз")


def read_matrix(m, name, diag_type):
    print(f"\nВведіть матрицю {name} ({m} рядків по {m} чисел):")

    while True:
        data = []
        ok = True

        for i in range(m):
            try:
                row = list(map(float, input(f"Рядок {i+1}: ").split()))

                if len(row) != m:
                    print("Неправильна кількість елементів у рядку")
                    ok = False
                    break

                data.append(row)

            except:
                print("Помилка вводу")
                ok = False
                break

        if not ok:
            print("Спробуйте ввести матрицю ще раз\n")
            continue

        diag_ok = True
        for i in range(m):
            if diag_type == "zero" and data[i][i] != 0:
                print(f"У матриці {name} діагональ має бути 0")
                diag_ok = False
                break
            if diag_type == "one" and data[i][i] != 1:
                print(f"У матриці {name} діагональ має бути 1")
                diag_ok = False
                break

        if not diag_ok:
            print("Спробуйте ще раз\n")
            continue

        flat = []
        for row in data:
            for val in row:
                flat.append(val)

        return flat


def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except:
            print("Помилка вводу. Введіть число")


def read_from_file(filename):
    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        i = 0

        m = int(lines[i].split("=")[1])
        i += 1

        n = list(map(int, lines[i].split("=")[1].split()))
        i += 1

        if lines[i] != "c =":
            raise Exception("Очікується 'c ='")
        i += 1

        c = []
        for _ in range(m):
            row = list(map(float, lines[i].split()))
            if len(row) != m:
                raise Exception("Неправильний рядок у матриці C")
            c.extend(row)
            i += 1

        if lines[i] != "r =":
            raise Exception("Очікується 'r ='")
        i += 1

        r = []
        for _ in range(m):
            row = list(map(float, lines[i].split()))
            if len(row) != m:
                raise Exception("Неправильний рядок у матриці R")
            r.extend(row)
            i += 1

        t = float(lines[i].split("=")[1])
        i += 1

        d = float(lines[i].split("=")[1])

        return m, n, c, r, t, d, None

    except Exception as e:
        return None, None, None, None, None, None, str(e)