# 문제: https://codetree.ai/training-field/frequent-problems/problems/royal-knight-duel/description?page=1&pageSize=20
import copy

# 상 우 하 좌: yx
directions = [(-1,0), (0,1), (1,0),(0,-1)]

l,n,q = map(int, input().split())

board = []
for _ in range(l):
    board.append(list(map(int, input().split())))

# r, c => 초기 위치
# h, w, => 크기
# k => 체력
## 추가 original 체력
knights = []
for _ in range(n):
    tmp = list(map(int, input().split()))
    tmp[0] -= 1
    tmp[1] -= 1
    tmp.append(tmp[4])
    knights.append(tmp)

def isKnightArea(knight, y,x):
    for i in range(knight[2]):
        for j in range(knight[3]):
            ky = knight[0]+i
            kx = knight[1]+j
            if (ky == y and x == kx):
                return True

    return False

def findCloseKnights(knightNum, directionNum):
    knight = knights[knightNum]
    direction = directions[directionNum]

    ys = []
    xs = []
    if (directionNum == 0): # 상
        ys = [knight[0]+direction[0] for _ in range(knight[3])]
        xs = [knight[1]+i for i in range(knight[3])]
    elif (directionNum == 1): # 우
        ys = [knight[0] + i for i in range(knight[2])]
        xs = [knight[1] + knight[3] + direction[1] - 1 for _ in range(knight[2])]
    elif (directionNum == 2): # 하
        ys = [knight[0] + knight[2] + direction[0] -1 for _ in range(knight[3])]
        xs = [knight[1] + i for i in range(knight[3])]
    elif (directionNum == 3): # 좌
        ys = [knight[0]+i for i in range(knight[2])]
        xs = [knight[1]+direction[1] for _ in range(knight[2])]

    closeKnightNums = []
    for i in range(n):
        if (i != knightNum):
            for j in range(len(ys)):
                if (isKnightArea(knights[i], ys[j], xs[j]) and knights[i][4] > 0):
                    closeKnightNums.append(i)

    return closeKnightNums


def executeMove(knightNum, directionNum, depth):
    global knights
    knight = knights[knightNum]
    direction = directions[directionNum]

    if (knight[4] <= 0):
        return True

    copyKnights = []
    if (depth == 0):
        copyKnights = copy.deepcopy(knights)


    closeKnightNums = findCloseKnights(knightNum, directionNum)

    canMove = True
    for closeKnightNum in closeKnightNums:
        if(not executeMove(closeKnightNum, directionNum, depth+1)):
            canMove = False
            break

    if (not canMove):
        if (depth == 0):
            knights = copyKnights
        return False

    knight[0] += direction[0]
    knight[1] += direction[1]
    for i in range(knight[2]):
        for j in range(knight[3]):
            ky = knight[0] + i
            kx = knight[1] + j


            if (ky < 0 or ky >= l or kx < 0 or kx >= l or board[ky][kx] == 2):
                if (depth == 0):
                    knights = copyKnights
                return False
            if (board[ky][kx] == 1 and depth != 0):
                knight[4] -= 1

    return True

# i q
for _ in range(q):
    operation = list(map(int, input().split()))
    executeMove(operation[0]-1, operation[1], 0)

sum = 0
for knight in knights:
    if (knight[4] > 0):
        sum += knight[5]-knight[4]
print(sum)