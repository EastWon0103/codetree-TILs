from collections import deque

n, m, k = map(int, input().split())

board = [[0]*(m+1) for _ in range(n+1)]
shooting_log = [[0]*(m+1) for _ in range(n+1)]
hit_log = [[0]*(m+1) for _ in range(n+1)]

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] #우하좌상

for i in range(1,n+1):
    lst = list(map(int,input().split()))
    for j in range(1,m+1):
        board[i][j] = lst[j-1]

def find_attacker():
    weak_turret = None

    for i in range(1, n+1):
        for j in range(1, m+1):
            if board[i][j] == 0:
                continue
            if weak_turret is None:
                weak_turret = (i, j, board[i][j])
            elif weak_turret[2] > board[i][j]:
                weak_turret = (i, j, board[i][j])
            elif weak_turret[2] < board[i][j]:
                continue

            # 공격력이 같으면
            if shooting_log[weak_turret[0]][weak_turret[1]] < shooting_log[i][j]: # 최근에 공격한 것
                weak_turret = (i, j, board[i][j])
            elif shooting_log[weak_turret[0]][weak_turret[1]] > shooting_log[i][j]:
                continue

            # 둘 다 최근에 공격했다면
            if weak_turret[0]+weak_turret[1] > i+j: # 행열 합이 더 큰 거
                weak_turret = (i, j, board[i][j])
            elif weak_turret[0]+weak_turret[1] == i+j and weak_turret[1] < j: # 행열 합이 같으면 열이 더 큰 거
                weak_turret = (i, j, board[i][j])

    return (weak_turret[0], weak_turret[1], weak_turret[2]+n+m)

def find_attack_target(attacker):
    strong_turret = None

    for i in range(1, n+1):
        for j in range(1, m+1):
            if attacker[0] == i and attacker[1] == j: # 공격자가 공격 대상과 같다면
                continue
            if strong_turret is None:
                strong_turret = (i, j, board[i][j])

            # 공격력이 높은 것을 뽑기
            if strong_turret[2] < board[i][j]:
                strong_turret = (i, j, board[i][j])
            elif strong_turret[2] > board[i][j]:
                continue

            # 만약 공격력이 같다면
            if shooting_log[strong_turret[0]][strong_turret[1]] > shooting_log[i][j]: # 공격한지 가장 오래된 포탑
                strong_turret = (i, j, board[i][j])
            elif shooting_log[strong_turret[0]][strong_turret[1]] < shooting_log[i][j]:
                continue

            # 공격 시간도 같다면
            if strong_turret[0]+strong_turret[1] > i+j:
                strong_turret = (i, j, board[i][j])
            elif strong_turret[0]+strong_turret[1] == i+j and strong_turret[1] > j:
                strong_turret = (i, j, board[i][j])

    return strong_turret

def setY(y):
    if y > n:
        return 1
    if y == 0:
        return n
    return y

def setX(x):
    if x > m:
        return 1
    if x == 0:
        return n
    return x

def get_opposite_dir(dirNum):
    if dirNum == 0:
        return 2
    if dirNum == 1:
        return 3
    if dirNum == 2:
        return 0
    if dirNum == 3:
        return 1

def razor_attack(attacker, target, t):
    visited = [[[False]]*(m+1) for _ in range(n+1)] # 들어왔는지, 1:y, 2:x 3: fromDir 번호

    que = deque()
    visited[attacker[0]][attacker[1]] = (True, attacker[0], attacker[1], -1, 0)
    que.append((attacker[0], attacker[1], 0)) # y,x,distance

    while que:
        point = que.popleft()

        for i in range(4):
            y = setY(point[0]+directions[i][0])
            x = setX(point[1]+directions[i][1])
            dis = point[2]+1

            if visited[y][x][0]:
                continue

            if board[y][x] ==0:
                continue

            visited[y][x] = (True, y, x, i, dis)
            if y == target[0] and x == target[1]:
                que.clear()
                break

            que.append((y, x, dis))

    if not visited[target[0]][target[1]][0]:
        return False


    y = visited[target[0]][target[1]][1]
    x = visited[target[0]][target[1]][2]
    dirNum = visited[target[0]][target[1]][3]
    for i in range(visited[target[0]][target[1]][4]):
        if i == 0:
            board[y][x] -= attacker[2]
        else:
            board[y][x] -= int(attacker[2]/2)

        if board[y][x] < 0:
            board[y][x] = 0
        hit_log[y][x] = t
        y += directions[get_opposite_dir(dirNum)][0]
        x += directions[get_opposite_dir(dirNum)][1]
        dirNum = visited[y][x][3]

    return True

def normal_attack(attacker, target, t):
    normal_dir = [(1,1),(-1,-1),(-1,1), (1,-1), (0, 1), (1, 0), (0, -1), (-1, 0)]

    board[target[0]][target[1]] -= attacker[2]
    hit_log[target[0]][target[1]] = t
    if board[target[0]][target[1]] < 0:
        board[target[0]][target[1]] = 0

    for dir in normal_dir:
        y = setY(target[0]+dir[0])
        x = setX(target[1]+dir[1])

        if (y,x) == attacker[:2] or board[y][x] == 0:
            continue

        board[y][x] -= int(attacker[2]/2)
        hit_log[y][x] = t
        if board[y][x] < 0:
            board[y][x] = 0

def printResult():
    for i in range(1, n+1):
        for j in range(1, m+1):
            print(board[i][j], end=" ")
        print()

def heal_turret(attacker, t):
    for i in range(1,n+1):
        for j in range(1,m+1):
            if board[i][j] != 0 and hit_log[i][j] < t and (i,j) != attacker[:2]:
                board[i][j] += 1

for t in range(1, k+1):
    attacker = find_attacker() # 약한 포탑이 공격자 y,x,공격력
    board[attacker[0]][attacker[1]] = attacker[2] # 싱크 맞추기

    target = find_attack_target(attacker) # 공격자를 제외한 공격력이 가장 쎈 포탑이 타겟 y,x,공격력
    razor_attack_success = razor_attack(attacker, target, t)

    if not razor_attack_success:
        normal_attack(attacker, target, t)

    shooting_log[attacker[0]][attacker[1]] = t
    heal_turret(attacker, t)


max_turret = 0
for i in range(1,n+1):
    for j in range(1,m+1):
        max_turret = max(max_turret, board[i][j])
print(max_turret)