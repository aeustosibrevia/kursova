import numpy as np
####################
m = 4
n = [20, 80, 10, 10]

c = [
    1, 0.3, 0.3, 0.3,
    0.3, 1, 0.7, 0.7,
    0.3, 0.7, 1, 0.7,
    0.3, 0.7, 0.7, 1
]

r = [
    0, 0.2, 0.2, 0.2,
    0.2, 0, 0.1, 0.1,
    0.2, 0.1, 0, 0.1,
    0.2, 0.1, 0.1, 0
]

t = 0.5
d = 0.8

matrix_c = np.array(c).reshape(m, m)
matrix_r = np.array(r).reshape(m, m)

####################
def risk_of_set(S):
     total = 0
     S = list(S)
     for i in range(len(S)):
          for j in range(len(S)):
               if i != j:
                    total += matrix_r[S[i], S[j]]
     return total/2
def F(S): # тут можна взагалі додати перевірку на q < 2, але у нас завжди доходить до цього етапу при q >= 2
     S = list(S)
     q = len(S)
     multiplication = 1
     indicator = 2/(q*(q-1))
     for i in range(q):
          for j in range(q):
               if i < j:
                    multiplication *= matrix_c[S[i], S[j]]
     return multiplication ** indicator

def total_agreement(i, S):
     S = list(S)
     total = 0
     for j in S:
          if i != j:
               total += matrix_c[i, j]
     return total

N = sum(n)
print(N)
for i in range(m):
     if n[i] >= (N * 0.5 + 1):
          print("K* = ", {i})
          print("H* = ", {i})
          print("F* = ", 1)
          raise Exception("Коаліція складається з однієї партії")

row_sums = []
for i in range(m):
     total = 0
     for j in range(m):
          if i != j:
               total += matrix_c[i, j]
     row_sums.append(total)
i0 = row_sums.index(max(row_sums))
K = {i0}
print(i0)
print(K)

while sum(n[i] for i in K) < N * 0.5 + 1:
     J = set()
     for j in range(m):
          if j not in K and risk_of_set(K | {j}) <= d:
               J.add(j)

     if not J:
          raise Exception("Помилка: неможливо побудувати допустиму коаліцію")

     j_star = None
     best_val = -1
     for j in J:
          current_F = F(K | {j})
          if current_F > best_val:
               best_val = current_F
               j_star = j
     K.add(j_star)

koal = sum(n[i] for i in K)

print(koal)

best_val = 0
h0 = None
for i in K:
     current_res = total_agreement(i, K)
     # print("Total: ", current_res)
     if current_res > best_val:
          best_val = current_res
          h0 = i
H = {h0}

print(H)
while True:
     sum_H = 0
     for i in H:
          sum_H += n[i]

     cond1 = sum_H < koal * 0.5 + 1

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

     JH = set()

     for i in K:
          if i not in H:
               JH.add(i)

     if not JH:
          raise Exception("Помилка: неможливо побудувати допустиме ядро")

     j_star = None
     best_val = -1

     JH = list(JH)
     for j in JH:
          score = 0

          for i in JH:
               if matrix_c[i, j] >= t:
                    score += matrix_c[i, j]

          if score > best_val:
               best_val = score
               j_star = j

     H.add(j_star)

K_out = {i + 1 for i in K}
H_out = {i + 1 for i in H}

print("K* =", K_out)
print("H* =", H_out)
print("F* =", F(K))


