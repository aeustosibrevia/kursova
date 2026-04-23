from greedy import run_greedy
from branch_and_bound import run_branch_and_bound
from generator import generate_data


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


def main():
    print("Оберіть режим:")
    print("1 - Ввести дані вручну")
    print("2 - Згенерувати випадково")

    while True:
        choice = input("Ваш вибір: ")

        if choice == "1":
            print("\n--- Ручний ввід ---")

            while True:
                try:
                    m = int(input("m: "))
                    if m <= 0:
                        print("m має бути > 0")
                        continue
                    break
                except:
                    print("Помилка вводу")

            n = read_int_list("n: ", m)
            c = read_matrix(m, "c", "one")
            r = read_matrix(m, "r", "zero")
            t = read_float("t: ")
            d = read_float("d: ")

            break

        elif choice == "2":
            print("\n--- Генерація ---")

            import random

            while True:
                try:
                    m = int(input("m (кількість фракцій): "))
                    if m <= 0:
                        print("m має бути > 0")
                        continue
                    break
                except:
                    print("Помилка вводу")

            n_min, n_max = 10, 100
            change = input(f"Змінити діапазон n_i? (за замовчуванням [{n_min}, {n_max}]) y/n: ")

            if change.lower() == 'y':
                n_min = int(input("n_min: "))
                n_max = int(input("n_max: "))

            n = [random.randint(n_min, n_max) for _ in range(m)]

            c = []
            for i in range(m):
                for j in range(m):
                    if i == j:
                        c.append(1.0)
                    else:
                        c.append(round(random.uniform(0, 1), 2))

            r = []
            for i in range(m):
                for j in range(m):
                    if i == j:
                        r.append(0.0)
                    else:
                        r.append(round(random.uniform(0, 1), 2))

            t = round(random.uniform(0, 1), 2)
            d = round(random.uniform(0, 1), 2)

            print("\n--- Згенерована задача ---")
            print("m =", m)
            print("n =", n)

            print("\nMatrix C:")
            for i in range(m):
                print(c[i*m:(i+1)*m])

            print("\nMatrix R:")
            for i in range(m):
                print(r[i*m:(i+1)*m])

            print("\nt =", t)
            print("d =", d)

            break

        else:
            print("Невірний вибір, спробуйте ще раз")

    print("\n--- Greedy ---")
    K_greedy, H_greedy, F_greedy, err = run_greedy(m, n, c, r, t, d)

    if err:
        print(err)
    else:
        print("K* =", K_greedy)
        print("H* =", H_greedy)
        print("F* =", F_greedy)

    print("\n--- Branch and Bound ---")
    K_bb, H_bb, F_bb = run_branch_and_bound(m, n, c, r, t, d)

    if K_bb is None:
        print("Допустиму коаліцію не знайдено")
    else:
        print("K* =", K_bb)
        print("H* =", H_bb)
        print("F* =", F_bb)

if __name__ == "__main__":
    main()