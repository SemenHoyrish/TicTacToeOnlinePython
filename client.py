from os import system

class Position:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

class NullPosition(Position):
    x = None
    y = None
    def __init__(self):
        pass


EMPTY = -1
CROSS = 1
ZERO = 0
NULL_POS = NullPosition()
turn = CROSS

#TODO: create a class for field
field = [
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY]
]

#
# field = [
#     [1, 0, 1,],
#     [-1, 0, 0,],
#     [1, 1, 0,]
# ]

PLATFORM_WIN = "WIN"
PLATFORM_LINUX = "LINUX"
PLATFORM = PLATFORM_WIN

def CLEAR():
    if PLATFORM == PLATFORM_WIN:
        system("cls")
    else:
        print("Platform not supported!")

def draw_field():
    for x in field:
        for y in x:
            if y == CROSS:
                print("X", end="")
            elif y == ZERO:
                print("O", end="")
            else:
                print("_", end="")
        print()

def is_position_valid(pos: Position) -> bool:
    if ((pos.x >= 0 and pos.x < len(field)) and
        (pos.y >= 0 and pos.y < len(field[0]))):
        return True
    return False

def place(type: int, pos: Position) -> bool:
    if not is_position_valid(pos): return False
    if field[pos.x][pos.y] == EMPTY:
        field[pos.x][pos.y] = type
        return True
    return False

def parse_position(inp: str) -> Position:
    tmp = inp.strip().split(" ")
    if len(tmp) != 2:
        return NULL_POS
    y, x = map(int, tmp)
    return Position(x, y)

def next_turn():
    global turn
    if turn == CROSS:
        turn = ZERO
    else:
        turn = CROSS


def is_all_items_same(arr: list) -> bool:
    if len(arr) == 0: return True
    item = arr[0]
    for i in arr:
        if item != i:
            return False
    return True

def get_column(arr: list, index: int) -> list:
    res = []
    for line in arr:
        res.append(line[index])
    return res

def is_win() -> (bool, int):
    for line in field:
        if is_all_items_same(line) and line[0] != EMPTY:
            return (True, line[0])

    for i in range(len(field[0])):
        column = get_column(field, i)
        if is_all_items_same(column) and column[0] != EMPTY:
            return (True, column[0])

    if (field[0][0] == field[1][1] and field[0][0] == field[2][2]) and field[0][0] != EMPTY:
        return (True, field[0][0])
    if (field[2][0] == field[1][1] and field[2][0] == field[0][2]) and field[2][0] != EMPTY:
        return (True, field[2][0])

    return (False, EMPTY)

while True:
    CLEAR()
    draw_field()
    print("Now goes " + ("CROSS" if turn == CROSS else "ZERO"))
    pos = parse_position(input("Input pos: x y "))
    if pos == NULL_POS:
        print("Error while parsing a position")
        continue
    if not place(turn, pos):
        print("Error while placing")
        continue

    win, type = is_win()
    if win:
        CLEAR()
        draw_field()
        print( ("CROSS" if type == CROSS else "ZERO") + " wins!!!" )
        break

    # print(win)
    # input("Enter for next turn")

    next_turn()

    if pos.x == 88:
        break
