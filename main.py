from greedy import run_greedy
from branch_and_bound import run_branch_and_bound
from utils import generate_data, generate_test_data, read_int_list, read_matrix, read_float, read_from_file
import time
import matplotlib.pyplot as plt

def input_menu():
    while True:
        print("\n--- МЕНЮ ВВОДУ ---")
        print("1 - Ввести дані вручну")
        print("2 - Згенерувати випадково")
        print("3 - Зчитати з файлу")
        print("0 - Назад")

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

            return m, n, c, r, t, d

        elif choice == "2":
            print("\n--- Генерація ---")
            return generate_data()

        elif choice == "3":
            print("\n--- Зчитування з файлу ---")

            filename = input("Введіть ім'я файлу: ")
            m, n, c, r, t, d, err = read_from_file(filename)

            if err:
                print("Помилка:", err)
                continue

            print("\n--- Дані з файлу ---")
            print("m =", m)
            print("n =", n)

            print("\nMatrix C:")
            for i in range(m):
                print(c[i * m:(i + 1) * m])

            print("\nMatrix R:")
            for i in range(m):
                print(r[i * m:(i + 1) * m])

            print("\nt =", t)
            print("d =", d)

            return m, n, c, r, t, d

        elif choice == "0":
            return None

        else:
            print("Невірний вибір")

def run_experiments():
    print("\n=== ЕКСПЕРИМЕНТИ ===")

    m = int(input("m: "))
    n_min = int(input("n_min: "))
    n_max = int(input("n_max: "))
    R = int(input("Кількість запусків R: "))

    greedy_F = []
    greedy_T = []

    bb_F = []
    bb_T = []

    bb_wins = 0

    for k in range(R):

        m_, n, c, r, t, d = generate_test_data(m, n_min, n_max)

        start = time.time()
        _, _, F_g, err = run_greedy(m_, n, c, r, t, d)
        t_g = time.time() - start

        if err:
            F_g = 0

        start = time.time()
        K_b, H_b, F_b = run_branch_and_bound(m_, n, c, r, t, d)
        t_b = time.time() - start

        if K_b is None:
            F_b = 0

        if F_b > F_g:
            bb_wins += 1

        greedy_F.append(F_g)
        bb_F.append(F_b)

        greedy_T.append(t_g)
        bb_T.append(t_b)

        print(f"Test {k+1}/{R}: "
              f"Fg={F_g:.4f}, Fb={F_b:.4f}")

    def mean(arr):
        return sum(arr) / len(arr)

    def variance(arr, m):
        return sum((x - m) ** 2 for x in arr) / len(arr)

    greedy_mean = mean(greedy_F)
    bb_mean = mean(bb_F)

    greedy_var = variance(greedy_F, greedy_mean)
    bb_var = variance(bb_F, bb_mean)

    greedy_time = mean(greedy_T)
    bb_time = mean(bb_T)

    # --- НОВИЙ розрахунок δ ---
    sum_Fg = sum(greedy_F)
    sum_Fb = sum(bb_F)

    denom = max(sum_Fb, sum_Fg)

    if denom == 0:
        delta_mean = 0
    else:
        delta_mean = (sum_Fb - sum_Fg) / denom

    w = bb_wins / R

    print("\n=== GREEDY ===")
    print("F̄ =", greedy_mean)
    print("D =", greedy_var)
    print("T̄ =", greedy_time)

    print("\n=== BRANCH AND BOUND ===")
    print("F̄ =", bb_mean)
    print("D =", bb_var)
    print("T̄ =", bb_time)

    print("\n=== ПОРІВНЯННЯ ===")
    print("δ̄ =", delta_mean)
    print("w (BnB wins rate) =", w)

    tests = list(range(1, R + 1))

    plt.figure()
    plt.plot(tests, greedy_F, marker='o', label='Greedy')
    plt.plot(tests, bb_F, marker='o', label='Branch&Bound')

    plt.xlabel("Номер експерименту")
    plt.ylabel("Значення ЦФ (F)")
    plt.title("Залежність F від номера експерименту")
    plt.legend()
    plt.grid()

    plt.figure()
    plt.plot(tests, greedy_T, marker='o', label='Greedy')
    plt.plot(tests, bb_T, marker='o', label='Branch&Bound')

    plt.xlabel("Номер експерименту")
    plt.ylabel("Час виконання")
    plt.title("Залежність часу від номера експерименту")
    plt.legend()
    plt.grid()

    plt.show()

def print_problem(m, n, c, r, t, d):
    print("\n--- УМОВА ЗАДАЧІ ---")
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

def study_m():
    print("\n=== ДОСЛІДЖЕННЯ ПАРАМЕТРА m ===")

    m_min = int(input("m_min: "))
    m_max = int(input("m_max: "))

    n_min = int(input("n_min: "))
    n_max = int(input("n_max: "))

    m_full, n_full, c_full, r_full, t, d = generate_test_data(m_max, n_min, n_max)

    m_values = []
    greedy_T = []
    bb_T = []
    greedy_F = []
    bb_F = []

    for m in range(m_min, m_max + 1):

        n = n_full[:m]

        c = []
        r = []

        for i in range(m):
            for j in range(m):
                c.append(c_full[i * m_full + j])
                r.append(r_full[i * m_full + j])

        print("\n==============================")
        print(f"ЕКСПЕРИМЕНТ: m = {m}")

        print_problem(m, n, c, r, t, d)

        start = time.time()
        _, _, F_g, err = run_greedy(m, n, c, r, t, d)
        t_g = time.time() - start

        if err:
            F_g = 0

        start = time.time()
        K_b, _, F_b = run_branch_and_bound(m, n, c, r, t, d)
        t_b = time.time() - start

        if K_b is None:
            F_b = 0

        print("\n--- РЕЗУЛЬТАТИ ---")
        print(f"Greedy: F={F_g:.4f}, T={t_g:.4f}")
        print(f"BnB:    F={F_b:.4f}, T={t_b:.4f}")

        m_values.append(m)
        greedy_T.append(t_g)
        bb_T.append(t_b)
        greedy_F.append(F_g)
        bb_F.append(F_b)

    plt.figure()
    plt.plot(m_values, greedy_T, marker='o', label='Greedy')
    plt.plot(m_values, bb_T, marker='o', label='BnB')
    plt.xlabel("m")
    plt.ylabel("Час виконання")
    plt.title("Залежність часу від m")
    plt.legend()
    plt.grid()

    plt.figure()
    plt.plot(m_values, greedy_F, marker='o', label='Greedy')
    plt.plot(m_values, bb_F, marker='o', label='BnB')
    plt.xlabel("m")
    plt.ylabel("Цільова функція (F)")
    plt.title("Залежність F від m")
    plt.legend()
    plt.grid()

    plt.show()

def study_t():
    print("\n=== ДОСЛІДЖЕННЯ ПАРАМЕТРА t ===")

    m = int(input("m: "))
    n_min = int(input("n_min: "))
    n_max = int(input("n_max: "))

    t_min = float(input("t_min: "))
    t_max = float(input("t_max: "))
    steps = int(input("Кількість кроків: "))

    m, n, c, r, _, d = generate_test_data(m, n_min, n_max)

    t_values = []
    greedy_T = []
    bb_T = []
    greedy_F = []
    bb_F = []

    for i in range(steps + 1):
        t = t_min + (t_max - t_min) * i / steps

        print("\n==============================")
        print(f"ЕКСПЕРИМЕНТ: t = {t:.2f}")

        print_problem(m, n, c, r, t, d)

        start = time.time()
        _, _, F_g, err = run_greedy(m, n, c, r, t, d)
        t_g = time.time() - start

        if err:
            F_g = 0

        start = time.time()
        K_b, _, F_b = run_branch_and_bound(m, n, c, r, t, d)
        t_b = time.time() - start

        if K_b is None:
            F_b = 0

        print("\n--- РЕЗУЛЬТАТИ ---")
        print(f"Greedy: F={F_g:.4f}, T={t_g:.4f}")
        print(f"BnB:    F={F_b:.4f}, T={t_b:.4f}")

        t_values.append(t)
        greedy_T.append(t_g)
        bb_T.append(t_b)
        greedy_F.append(F_g)
        bb_F.append(F_b)

    plt.figure()
    plt.plot(t_values, greedy_T, marker='o', label='Greedy')
    plt.plot(t_values, bb_T, marker='o', label='BnB')
    plt.xlabel("t")
    plt.ylabel("Час")
    plt.title("Залежність часу від t")
    plt.legend()
    plt.grid()

    plt.figure()
    plt.plot(t_values, greedy_F, marker='o', label='Greedy')
    plt.plot(t_values, bb_F, marker='o', label='BnB')
    plt.xlabel("t")
    plt.ylabel("F")
    plt.title("Залежність F від t")
    plt.legend()
    plt.grid()

    plt.show()

def study_d():
    print("\n=== ДОСЛІДЖЕННЯ ПАРАМЕТРА d ===")

    m = int(input("m: "))
    n_min = int(input("n_min: "))
    n_max = int(input("n_max: "))

    d_min = float(input("d_min: "))
    d_max = float(input("d_max: "))
    steps = int(input("Кількість кроків: "))

    m, n, c, r, t, _ = generate_test_data(m, n_min, n_max)

    d_values = []
    greedy_T = []
    bb_T = []
    greedy_F = []
    bb_F = []

    print("\nФіксовані параметри: m, n, c, r, t")
    print("Змінюється тільки d")

    for i in range(steps + 1):
        d = d_min + (d_max - d_min) * i / steps

        print("\n==============================")
        print(f"ЕКСПЕРИМЕНТ: d = {d:.2f}")

        print_problem(m, n, c, r, t, d)

        start = time.time()
        _, _, F_g, err = run_greedy(m, n, c, r, t, d)
        t_g = time.time() - start

        if err:
            F_g = 0

        start = time.time()
        K_b, _, F_b = run_branch_and_bound(m, n, c, r, t, d)
        t_b = time.time() - start

        if K_b is None:
            F_b = 0

        print("\n--- РЕЗУЛЬТАТИ ---")
        print(f"Greedy: F={F_g:.4f}, T={t_g:.4f}")
        print(f"BnB:    F={F_b:.4f}, T={t_b:.4f}")

        d_values.append(d)
        greedy_T.append(t_g)
        bb_T.append(t_b)
        greedy_F.append(F_g)
        bb_F.append(F_b)

    plt.figure()
    plt.plot(d_values, greedy_T, marker='o', label='Greedy')
    plt.plot(d_values, bb_T, marker='o', label='BnB')
    plt.xlabel("d")
    plt.ylabel("Час виконання")
    plt.title("Залежність часу від d")
    plt.legend()
    plt.grid()

    plt.figure()
    plt.plot(d_values, greedy_F, marker='o', label='Greedy')
    plt.plot(d_values, bb_F, marker='o', label='BnB')
    plt.xlabel("d")
    plt.ylabel("Цільова функція (F)")
    plt.title("Залежність F від d")
    plt.legend()
    plt.grid()

    plt.show()

def parameter_study():
    print("\n=== ДОСЛІДЖЕННЯ ПАРАМЕТРІВ ===")
    print("1 - Дослідити m")
    print("2 - Дослідити t")
    print("3 - Дослідити d")

    choice = input("Ваш вибір: ")

    if choice == "1":
        study_m()
    elif choice == "2":
        study_t()
    elif choice == "3":
        study_d()
    else:
        print("Невірний вибір")

def output_menu():
    global stored_data, stored_result

    if stored_data is None or stored_result is None:
        print("Немає даних або результатів!")
        return

    print("\n--- ВИВЕДЕННЯ ---")
    print("1 - Вивести на екран")
    print("2 - Записати в файл")

    choice = input("Ваш вибір: ")

    m, n, c, r, t, d = stored_data
    K_g, H_g, F_g, err_g, K_b, H_b, F_b = stored_result

    def format_data():
        text = []
        text.append("=== УМОВА ===")
        text.append(f"m = {m}")
        text.append(f"n = {n}")

        text.append("\nMatrix C:")
        for i in range(m):
            text.append(str(c[i*m:(i+1)*m]))

        text.append("\nMatrix R:")
        for i in range(m):
            text.append(str(r[i*m:(i+1)*m]))

        text.append(f"\nt = {t}")
        text.append(f"d = {d}")

        text.append("\n=== РЕЗУЛЬТАТИ ===")

        text.append("\n--- Greedy ---")
        if err_g:
            text.append("Не вдалося знайти допустиме рішення")
        else:
            text.append(f"K* = {K_g}")
            text.append(f"H* = {H_g}")
            text.append(f"F* = {F_g}")

        text.append("\n--- Branch and Bound ---")
        if K_b is None:
            text.append("Не вдалося знайти допустиме рішення")
        else:
            text.append(f"K* = {K_b}")
            text.append(f"H* = {H_b}")
            text.append(f"F* = {F_b}")

        return "\n".join(text)

    if choice == "1":
        print("\n" + format_data())

    elif choice == "2":
        filename = input("Ім'я файлу: ")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(format_data())
        print("Дані записано у файл!")

    else:
        print("Невірний вибір")

stored_data = None
stored_result = None
def main():
    while True:
        print("\n=== ГОЛОВНЕ МЕНЮ ===")
        print("1 - Ввести дані")
        print("2 - Розв'язати задачу")
        print("3 - Провести експерименти")
        print("4 - Дослідження параметрів")
        print("5 - Вивести дані")
        print("0 - Вихід")

        choice = input("Ваш вибір: ")

        if choice == "1":
            data = input_menu()
            if data is not None:
                global stored_data
                stored_data = data

        elif choice == "2":
            if stored_data is None:
                print("Спочатку введіть або згенеруйте дані!")
                continue
            m, n, c, r, t, d = stored_data
            print("\nОбчислення задачі...")

            K_greedy, H_greedy, F_greedy, err_greedy = run_greedy(m, n, c, r, t, d)

            K_bb, H_bb, F_bb = run_branch_and_bound(m, n, c, r, t, d)
            global stored_result
            stored_result = (
                K_greedy, H_greedy, F_greedy, err_greedy,
                K_bb, H_bb, F_bb
            )
            print("Обчислення завершено. Перейдіть у пункт 5 для перегляду результатів.")


        elif choice == "3":
            run_experiments()

        elif choice == "4":
            parameter_study()

        elif choice == "5":
            output_menu()

        elif choice == "0":
            print("Вихід з програми...")
            break

        else:
            print("Невірний вибір. Спробуйте ще раз")

if __name__ == "__main__":
    main()