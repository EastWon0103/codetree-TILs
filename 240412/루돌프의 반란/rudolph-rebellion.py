# n: 게임판의 크기 (3 <= N <= 50)
# m: 게임의 턴 수 (1<= M <= 1000)
# p: 산타의 수 (1<= p <= 30)
# c: 루돌프의 흼 (1 <= c <= N)
# d: 산타의 힘 (1 <= d <= N)
santaY = [0 for _ in range(31)]
santaX = [0 for _ in range(31)]
outSantas = [False for _ in range(31)]
scoreSantas = [0 for _ in range(31)]
sturnedSantas = [0 for _ in range(31)]
rudolfDir = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,0),(-1,1),(-1,-1)]
santaDir = [(0,-1),(1,0),(0,1),(-1,0) ] ## 좌하우상
n, m, p, c, d = map(int, input().split())

# 루돌프의 초기 위치
rudolfPoint = list(map(int, input().split()))

for _ in range(p):
    idx, sr, sc = map(int, input().split())
    santaY[idx] = sr
    santaX[idx] = sc


def isSantasAllOut():
    for i in range(1, p+1):
        if(not outSantas[i]):
            return False
    return True

def getDistance(y1,x1, y2,x2):
    return (y1-y2)*(y1-y2) + (x1-x2)*(x1-x2)

def getCloseSantaNum():
    closeSantaLst = []
    for i in range(1, p+1):
        if (outSantas[i]):
            continue
        closeSantaLst.append((i, getDistance(rudolfPoint[0], rudolfPoint[1], santaY[i], santaX[i]), santaY[i], santaX[i]))

    return sorted(closeSantaLst, key=lambda x: (x[1],-x[2], -x[3]))[0][0]


def isInDifferentSanta(santaNum):
    for i in range(1,p+1):
        if(santaNum != i and santaY[santaNum] == santaY[i] and santaX[santaNum] == santaX[i]):
            return i
    return -1


def interactionSanta(santaNum, dir):
    santaY[santaNum] += dir[0]
    santaX[santaNum] += dir[1]

    if (santaY[santaNum] < 1 or santaY[santaNum] > n or santaX[santaNum] < 1 or santaX[santaNum] > n):
        outSantas[santaNum] = True
        return
    isInSantaNum = isInDifferentSanta(santaNum)
    if (isInSantaNum != -1):
        interactionSanta(isInSantaNum, dir)

def crashSanta(closeSantaNum, dir):
    santaY[closeSantaNum] += dir[0]*c
    santaX[closeSantaNum] += dir[1]*c

    if (santaY[closeSantaNum] < 1 or santaY[closeSantaNum] > n or santaX[closeSantaNum] < 1 or santaX[closeSantaNum] > n):
        outSantas[closeSantaNum] = True
        return

    isInSantaNum = isInDifferentSanta(closeSantaNum)
    if (isInSantaNum != -1):
        interactionSanta(isInSantaNum, dir)

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
    santaY[santaNum] += dir[0]*d
    santaX[santaNum] += dir[1]*d

    if (santaY[santaNum] < 1 or santaY[santaNum] > n or santaX[santaNum] < 1 or santaX[santaNum] > n):
        outSantas[santaNum] = True
        return
    isInSantaNum = isInDifferentSanta(santaNum)
    if (isInSantaNum != -1):
        interactionSanta(isInSantaNum, dir)
def moveRudolf():
    closeSantaNum = getCloseSantaNum()

    minY = rudolfPoint[0] + rudolfDir[0][0]
    minX = rudolfPoint[1] + rudolfDir[0][1]
    minDis = getDistance(minY, minX, santaY[closeSantaNum], santaX[closeSantaNum])
    dir = rudolfDir[0]
    for i in range(1,8):
        tmpY = rudolfPoint[0] + rudolfDir[i][0]
        tmpX = rudolfPoint[1] + rudolfDir[i][1]
        tmpDis = getDistance(tmpY, tmpX, santaY[closeSantaNum], santaX[closeSantaNum])

        if(minDis > tmpDis):
            minY = tmpY
            minX = tmpX
            minDis = tmpDis
            dir = rudolfDir[i]

    rudolfPoint[0] = minY
    rudolfPoint[1] = minX

    if (minDis == 0):
        scoreSantas[closeSantaNum] += c
        sturnedSantas[closeSantaNum] += 2
        crashSanta(closeSantaNum, dir)

def isSanta(y,x):
    for i in range(1,p+1):
        if(santaY[i]==y and santaX[i]==x):
            return True

    return False

def moveSantas():
    for i in range(1,p+1):
        if (not outSantas[i] and sturnedSantas[i] == 0):
            minY = n+1
            minX = n+1
            minDis = n**2
            dir = -1

            for j in range(4):
                tmpY = santaY[i]+santaDir[j][0]
                tmpX = santaX[i]+santaDir[j][1]
                tmpDis = getDistance(rudolfPoint[0], rudolfPoint[1], tmpY, tmpX)

                if (isSanta(tmpY, tmpX) or tmpY < 1 or tmpY > n or tmpX < 1 or tmpX > n):
                    continue
                if(minDis >= tmpDis):
                    minY = tmpY
                    minX = tmpX
                    minDis = tmpDis
                    dir = j

                    if (rudolfPoint[0] == minY and rudolfPoint[1] == minX):
                        break

            if(1 <= minY <= n and 1<= minX <= n and not isSanta(minY, minX)
            and getDistance(rudolfPoint[0], rudolfPoint[1], minY,minX) < getDistance(rudolfPoint[0], rudolfPoint[1], santaY[i],santaX[i])):
                santaY[i] = minY
                santaX[i] = minX

            if(minDis==0):
                scoreSantas[i] += d
                sturnedSantas[i] += 2
                crashRudolf(i, santaDir[getOppositeDirection(dir)])

for _ in range(m):
    for i in range(1, p+1):
        sturnedSantas[i] -= 1
        if (sturnedSantas[i] < 0):
            sturnedSantas[i] = 0

    moveRudolf()
    if (isSantasAllOut()):
        break
    moveSantas()
    if (isSantasAllOut()):
        break

    for i in range(1,p+1):
        if(not outSantas[i]):
            scoreSantas[i] += 1

    # print("---------")
    # print("rudolf:", rudolfPoint)
    # print("santa")
    # for i in range(1,p+1):
    #     print(santaY[i], santaX[i])
    # print("outSanta", outSantas[1:p+1])
    # print("score: ", scoreSantas[1:p+1])
    # print("sturn: ", sturnedSantas[1:p+1])

for i in range(1, p+1):
    print(scoreSantas[i], end=" ")