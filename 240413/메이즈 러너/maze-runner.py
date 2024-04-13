# 좌상단 (1,1)
n, m, k = map(int, input().split())
maze = [[0 for _ in range(n+1)] for _ in range(n+1)]
runners = [0 for _ in range(m)]
is_escape = [False for _ in range(m)]
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # 우좌하상
exitPoint = ()

for i in range(1, n+1):
    tmp = [0]
    tmp.extend(list(map(int, input().split())))
    maze[i] = tmp

for i in range(m):
    runners[i] = tuple(map(int, input().split()))

exitPoint = tuple(map(int, input().split()))

def get_distance(point1, point2):
    return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1])

def is_in_range(point):
    return 1 <= point[0] <= n and 1 <= point[1] <= n

def can_move(point):
    return is_in_range(point) and maze[point[0]][point[1]] == 0

def is_runner_point(point):
    for i in range(m):
        if not is_escape[i] and runners[i] == point:
            return True
    return False

def is_good_square(y,x, length):
    # 좌상단으로 시작
    is_in_runners = False
    for i in range(y, y+length):
        for j in range(x, x+length):
            if not is_in_range((i, j)):
                return False

            is_in_runners = is_in_runners or is_runner_point((i, j))

    return is_in_runners


def find_square():
    length = 2
    square_lst = []
    while True:
        for i in range(exitPoint[0], exitPoint[0]-length, -1):
            for j in range(exitPoint[1], exitPoint[1]-length, -1):
                if is_good_square(i, j, length):
                    square_lst.append((i, j))

        if len(square_lst) > 0:
            break
        length += 1

    ## 제일 작은 y,x(좌상단), length
    return sorted(square_lst, key=lambda x:(x[0], x[1]))[0], length

def in_area(area, point):
    return area[0] <= point[0] <= area[0]+area[2]-1 and area[1] <= point[1] <= area[1]+area[2]-1

def get_rotate_90_point(area, point):
    ## transpose
    axis_gap = area[0]-area[1]
    my_gap = point[0]-point[1]
    y = point[0]
    x = point[1]
    if my_gap != axis_gap:
        y = point[0]-(my_gap-axis_gap)
        x = point[1]+(my_gap-axis_gap)

    ## reverse
    x = area[1]*2+area[2]-1-x
    return (y, x)

def runners_rotate_90(area):
    for i in range(len(runners)):
        if not is_escape[i] and in_area(area, runners[i]):
            runners[i] = get_rotate_90_point(area, runners[i])


def minus_or_zero(num):
    if (num == 0):
        return 0
    return num-1

def rotate_90(point, length):
    # transpose
    tmp_maze = [[0]*(n+1) for _ in range(n+1)]

    for y in range(point[0], point[0]+length):
        for x in range(point[1], point[1]+length):
            rotate_point = get_rotate_90_point((point[0],point[1], length), (y,x))
            tmp_maze[rotate_point[0]][rotate_point[1]] = maze[y][x]

    for y in range(point[0], point[0] + length):
        for x in range(point[1], point[1] + length):
            maze[y][x] = minus_or_zero(tmp_maze[y][x])

def move_runners():
    move_sum = 0
    for i in range(m):
        if is_escape[i]:
            continue

        minY = -1
        minX = -1
        minDis = 50000
        for d in range(4):
            tmpY = runners[i][0] + directions[d][0]
            tmpX = runners[i][1] + directions[d][1]
            tmpDis = get_distance(exitPoint, (tmpY, tmpX))

            if can_move((tmpY, tmpX)) and tmpDis <= minDis:
                minY = tmpY
                minX = tmpX
                minDis = tmpDis

        if minY != -1 and get_distance(exitPoint, runners[i]) > minDis:
            runners[i] = (minY, minX)
            move_sum+=1

        if runners[i] == exitPoint:
            is_escape[i] = True

    return move_sum

move_sum = 0
for t in range(1, k+1):
    move_sum += move_runners()

    is_all_escape = True
    for i in range(m):
        if not is_escape[i]:
            is_all_escape = False
            break
    if is_all_escape:
        break

    square_point, length = find_square()
    rotate_90(square_point, length)
    runners_rotate_90((square_point[0], square_point[1], length))
    exitPoint = get_rotate_90_point((square_point[0], square_point[1], length), exitPoint)

print(move_sum)
print(*exitPoint)