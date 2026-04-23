import numpy as np

def run_branch_and_bound(m, n, c, r, t, d):

    matrix_c = np.array(c).reshape(m, m)
    matrix_r = np.array(r).reshape(m, m)

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
        total = 0
        for j in S:
            if i != j:
                total += matrix_c[i, j]
        return total

    N = sum(n)

    row_sums = []
    for i in range(m):
        total = 0
        for j in range(m):
            if i != j:
                total += matrix_c[i, j]
        row_sums.append(total)

    i0 = row_sums.index(max(row_sums))

    K_star = {i0}
    H_star = {i0}
    F_star = 0

    def upper_bound(K):
        if not K:
            return 1

        max_c = 1
        for i in range(m):
            for j in range(m):
                if i != j:
                    if matrix_c[i, j] > max_c:
                        max_c = matrix_c[i, j]

        return F(K) * (max_c ** (m - len(K)))

    def build_core(K):
        best = None
        best_val = -1
        for i in K:
            val = total_agreement(i, K)
            if val > best_val:
                best_val = val
                best = i

        H = {best}

        while True:
            sum_H = 0
            for i in H:
                sum_H += n[i]

            cond1 = sum_H < sum(n[i] for i in K) * 0.5 + 1

            cond2 = False
            for j in K:
                if j not in H:
                    all_bad = True
                    for h in H:
                        if matrix_c[h, j] >= t:
                            all_bad = False
                            break
                    if all_bad:
                        cond2 = True
                        break

            if not (cond1 or cond2):
                break

            candidates = []
            for i in K:
                if i not in H:
                    candidates.append(i)

            if not candidates:
                break

            h_star = None
            best_val = -1

            for j in candidates:
                score = 0
                for h in H:
                    score += matrix_c[h, j]

                if score > best_val:
                    best_val = score
                    h_star = j

            H.add(h_star)

        return H

    solution_found = False
    def branch_and_bound(K_current, idx):
        nonlocal K_star, H_star, F_star, solution_found

        if sum(n[i] for i in K_current) >= 0.5 * N + 1:
            if risk_of_set(K_current) <= d:
                F_current = F(K_current)

                if (not solution_found) or (F_current > F_star):
                    H_current = build_core(K_current)

                    K_star = set(K_current)
                    H_star = set(H_current)
                    F_star = F_current
                    solution_found = True

        for j in range(idx, m):
            if j in K_current:
                continue

            new_K = K_current | {j}

            if risk_of_set(new_K) > d:
                continue
            if upper_bound(new_K) <= F_star:
                continue

            branch_and_bound(new_K, j + 1)

    branch_and_bound({i0}, 0)

    if not solution_found:
        return None, None, None

    K_out = {i + 1 for i in K_star}
    H_out = {i + 1 for i in H_star}

    return K_out, H_out, F_star