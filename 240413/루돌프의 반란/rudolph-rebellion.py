# n: 게임판의 크기 (3 <= N <= 50)
# m: 게임의 턴 수 (1<= M <= 1000)
# p: 산타의 수 (1<= p <= 30)
# c: 루돌프의 흼 (1 <= c <= N)
# d: 산타의 힘 (1 <= d <= N)
santaY = [0 for _ in range(31)]
santaX = [0 for _ in range(31)]
outSantas = [False for _ in range(31)]
santaScores = [0 for _ in range(31)]
sturnedSantas = [0 for _ in range(31)]
directions = [(0, -1), (1, 0), (0, 1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]  ## 좌하우상
n, m, p, c, d = map(int, input().split())

# 루돌프의 초기 위치
rudolfPoint = list(map(int, input().split()))

for _ in range(p):
    idx, sr, sc = map(int, input().split())
    santaY[idx] = sr
    santaX[idx] = sc


def isSantasAllOut():
    for i in range(1, p + 1):
        if (not outSantas[i]):
            return False
    return True


def getDistance(y1, x1, y2, x2):
    return (y1 - y2) ** 2 + (x1 - x2) ** 2


def getCloseSantaNum():
    closeSantaLst = []
    for i in range(1, p + 1):
        if (outSantas[i]):
            continue
        closeSantaLst.append(
            (i, getDistance(rudolfPoint[0], rudolfPoint[1], santaY[i], santaX[i]), santaY[i], santaX[i]))

    return sorted(closeSantaLst, key=lambda x: (x[1], -x[2], -x[3]))[0][0]


def isInDifferentSanta(santaNum):
    for i in range(1, p + 1):
        if (santaNum != i and santaY[santaNum] == santaY[i] and santaX[santaNum] == santaX[i]):
            return i
    return -1


def interactionSanta(santaNum, dir):
    if (santaY[santaNum] < 1 or santaY[santaNum] > n or santaX[santaNum] < 1 or santaX[santaNum] > n):
        outSantas[santaNum] = True
        return
    isInSantaNum = isInDifferentSanta(santaNum)
    if (isInSantaNum != -1):
        santaY[isInSantaNum] += dir[0]
        santaX[isInSantaNum] += dir[1]
        interactionSanta(isInSantaNum, dir)


def crashSanta(closeSantaNum, dir):
    santaY[closeSantaNum] += dir[0] * c
    santaX[closeSantaNum] += dir[1] * c

    interactionSanta(closeSantaNum, dir)


def getOppositeDirection(dirNum):
    if (dirNum == 0):
        return 2
    if (dirNum == 1):
        return 3
    if (dirNum == 2):
        return 0
    if (dirNum == 3):
        return 1


def crashRudolf(santaNum, dir):
    santaY[santaNum] += dir[0] * d
    santaX[santaNum] += dir[1] * d

    interactionSanta(santaNum, dir)


def moveRudolf():
    closeSantaNum = getCloseSantaNum()

    minY = rudolfPoint[0] + directions[0][0]
    minX = rudolfPoint[1] + directions[0][1]
    minDis = getDistance(minY, minX, santaY[closeSantaNum], santaX[closeSantaNum])
    dir = directions[0]
    for i in range(1, 8):
        tmpY = rudolfPoint[0] + directions[i][0]
        tmpX = rudolfPoint[1] + directions[i][1]
        tmpDis = getDistance(tmpY, tmpX, santaY[closeSantaNum], santaX[closeSantaNum])

        if (minDis >= tmpDis):
            minY = tmpY
            minX = tmpX
            minDis = tmpDis
            dir = directions[i]

    rudolfPoint[0] = minY
    rudolfPoint[1] = minX

    if (minDis == 0):
        santaScores[closeSantaNum] += c
        sturnedSantas[closeSantaNum] = 2
        crashSanta(closeSantaNum, dir)


def isSanta(y, x):
    for i in range(1, p + 1):
        if (santaY[i] == y and santaX[i] == x):
            return True
    return False


def moveSantas():
    for i in range(1, p + 1):
        if outSantas[i] or sturnedSantas[i] > 0:
            continue

        minY = n + 1
        minX = n + 1
        minDis = n*2 ** 2
        dir = -1
        can_move = False

        for j in range(4):
            tmpY = santaY[i] + directions[j][0]
            tmpX = santaX[i] + directions[j][1]
            tmpDis = getDistance(rudolfPoint[0], rudolfPoint[1], tmpY, tmpX)

            if (isSanta(tmpY, tmpX) or tmpY < 1 or tmpY > n or tmpX < 1 or tmpX > n):
                continue
            if (minDis >= tmpDis):
                minY = tmpY
                minX = tmpX
                minDis = tmpDis
                dir = j
                can_move = True

        if (can_move and minDis < getDistance(rudolfPoint[0],rudolfPoint[1], santaY[i], santaX[i])):
            santaY[i] = minY
            santaX[i] = minX

            if (minDis == 0):
                santaScores[i] += d
                sturnedSantas[i] = 2
                crashRudolf(i, directions[getOppositeDirection(dir)])


for _ in range(m):
    for i in range(1, p + 1):
        sturnedSantas[i] -= 1
        if sturnedSantas[i] < 0:
            sturnedSantas[i] = 0

    moveRudolf()
    if (isSantasAllOut()):
        break
    moveSantas()
    if (isSantasAllOut()):
        break

    for i in range(1, p + 1):
        if (not outSantas[i]):
            santaScores[i] += 1

for i in range(1, p + 1):
    print(santaScores[i], end=" ")