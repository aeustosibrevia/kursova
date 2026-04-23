import numpy as np
####################
m = 4
n = [40, 30, 50, 10]
c = [1, 0.9, 0.6, 0.4,
     0.9, 1, 0.7, 0.5,
     0.6, 0.7, 1, 0.8,
     0.4, 0.5, 0.8, 1]

matrix_c = np.array(c).reshape(m, m)

r = [0, 0.1, 0.3, 0.5,
     0.1, 0, 0.2, 0.4,
     0.3, 0.2, 0, 0.2,
     0.5, 0.4, 0.2, 0]

matrix_r = np.array(r).reshape(m, m)

t = 0.6
d = 0.8

####################

def risk_of_set(S):
    S = list(S)
    total = 0
    for i in range(len(S)):
        for j in range(len(S)):
            if i != j:
                total += matrix_r[S[i], S[j]]
    return total / 2


def F(S):
    S = list(S)
    q = len(S)
    if q < 2:
        return 1

    multiplication = 1
    indicator = 2 / (q * (q - 1))

    for i in range(q):
        for j in range(i + 1, q):
            multiplication *= matrix_c[S[i], S[j]]

    return multiplication ** indicator


def total_agreement(i, S):
    return sum(matrix_c[i, j] for j in S if i != j)


####################

N = sum(n)

row_sums = [sum(matrix_c[i, j] for j in range(m) if i != j) for i in range(m)]
i0 = row_sums.index(max(row_sums))

K_star = {i0}
H_star = {i0}
F_star = 0


####################

def upper_bound(K):
    if not K:
        return 1

    max_c = 1
    for i in range(m):
        for j in range(m):
            if i != j:
                max_c = max(max_c, matrix_c[i, j])

    return F(K) * (max_c ** (m - len(K)))


def build_core(K):
    best = max(K, key=lambda i: total_agreement(i, K))
    H = {best}

    while True:
        sum_H = sum(n[i] for i in H)

        cond1 = sum_H < sum(n[i] for i in K) * 0.5 + 1

        cond2 = False
        for j in K:
            if j not in H:
                if all(matrix_c[h, j] < t for h in H):
                    cond2 = True
                    break

        if not (cond1 or cond2):
            break

        candidates = [i for i in K if i not in H]

        if not candidates:
            break

        h_star = max(
            candidates,
            key=lambda j: sum(matrix_c[h, j] for h in H)
        )

        H.add(h_star)
        for j in list(H):
            if any(matrix_c[h, j] >= t for h in H if h != j):
                continue
            else:
                worst = min(H, key=lambda x: total_agreement(x, H))
                H.remove(worst)
                break
    return H


def branch_and_bound(K_current, idx):
    global K_star, H_star, F_star
    if sum(n[i] for i in K_current) >= 0.5 * N + 1:
        if risk_of_set(K_current) <= d:
            F_current = F(K_current)

            if F_current > F_star:
                H_current = build_core(K_current)

                K_star = set(K_current)
                H_star = set(H_current)
                F_star = F_current

    for j in range(idx, m):
        if j in K_current:
            continue

        new_K = K_current | {j}

        if risk_of_set(new_K) > d:
            continue
        if upper_bound(new_K) <= F_star:
            continue

        branch_and_bound(new_K, j + 1)


####################

branch_and_bound({i0}, 0)

K_out = {i + 1 for i in K_star}
H_out = {i + 1 for i in H_star}

print("K* =", K_out)
print("H* =", H_out)
print("F* =", F_star)