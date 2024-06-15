#считываем входные данные
n, m = map(int, input().split())

A = [[] for _ in range(m + 1)]

for i in range(n):
    lst = list(map(float, input().split()))
    for j in range(len(lst)):
        if j == m:
            A[0].append(lst[j])
        else:
            A[j + 1].append(lst[j])
            
B = [[] for _ in range(m)]

def multiplyer(row1, row2):
    res = 0
    for i in range(len(row1)):
        res += row1[i]*row2[i]
    return res

#создаем новую матрицу
for i in range(m):
    for j in range(m):
        B[i].append(multiplyer(A[j + 1], A[i + 1]))
    B[i].append(multiplyer(A[0], A[i + 1]))
    
a, b = len(B), len(B[0]) - 1

e = 1e-6

n = a #строки
m = b + 1 #длина строки

#вычисляем ранг матрицы
r1 = 0
for i in range(n):
    tmp = B[i][:(m - 1)]
    if any(abs(ele) > e for ele in tmp):
        r1 += 1

step = 0
for i in range(n - 1):
    step = step or i
    while step < m:
        pivot = B[i][step]
        pivot_row = i
        for j in range(i + 1, n):
            if abs(B[j][step]) > abs(pivot):
                pivot = B[j][step]
                pivot_row = j
        
        #меняем строки, если нужно        
        if pivot_row != i:
            B[i], B[pivot_row] = B[pivot_row], B[i]
            
        #зануляем нижние строки, если pivot не ноль
        if abs(pivot) > e:
            for j in range(i + 1, n):
                factor = B[j][step] / pivot
                for x in range(step, m):
                    B[j][x] -= B[i][x] * factor
            step += 1
            break
        step += 1
    
#вычисляем ранг матрицы после прямого прохода
r2 = 0
zeroes = []
flag = 0

for i in range(n):
    tmp = B[i][:(m - 1)]
    if any(abs(ele) > e for ele in tmp):
        r2 += 1
    else:
        zeroes.append(i)

if len(zeroes):
    for row in zeroes:
        if abs(B[row][-1]) > e:
            print('NO')
            break
    else:
        if (r2 < m - 1):
            print('INF')
        else:
            flag = 1
            
elif r1 == r2 and r1 < (m - 1):
    print('INF')
    
else:
    flag = 1
    
if flag == 1:
    #print('YES')
    start = step if step < m - 1 else m - 2
    #обратный ход матрицы
    for x in range(n - 1, 0, -1):
        if abs(B[x][start]) < e:
            continue
        for i in range(x - 1, -1, -1):
            factor = B[i][start] / B[x][start] 
            for j in range(m - 1, start - 1, -1):
                B[i][j] -= B[x][j] * factor
        start -= 1

    #вывод результатов
    res = []
    for i in range(n - len(zeroes)):
        res.append( B[i][-1] / B[i][i] )
    print(*res)
