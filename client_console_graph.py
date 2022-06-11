import sys
import asyncio
import websockets
import json
from os import system
from msvcrt import getch
from colorama import init, Fore, Back
from GameState import GameState

init()

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

game_state = GameState()
player = EMPTY

#TODO: create a class for field
# field = [
#     [EMPTY, EMPTY, EMPTY],
#     [EMPTY, EMPTY, EMPTY],
#     [EMPTY, EMPTY, EMPTY]
# ]

#
# field = [
#     [1, 0, 1,],
#     [-1, 0, 0,],
#     [1, 1, 0,]
# ]

PLATFORM_WIN = "WIN"
PLATFORM_LINUX = "LINUX"
PLATFORM = PLATFORM_WIN

DEBUG = False

def CLEAR():
    if DEBUG: return

    if PLATFORM == PLATFORM_WIN:
        system("cls")
    else:
        print("Platform not supported!")

CURRENT_POS = Position(0, 0)

def draw_field():
    global CURRENT_POS, game_state

    CLEAR()

    if SINGLEPLAYER_MODE:
        print("Now goes " + ("CROSS" if game_state.turn == CROSS else "ZERO"))
    else:
        print("NOW YOUR TURN!")

    for x_i, x in enumerate(game_state.field):
        for y_i, y in enumerate(x):
            # print("[draw_field] CUR_POS:", CURRENT_POS.x, CURRENT_POS.y)
            if x_i == CURRENT_POS.x and y_i == CURRENT_POS.y:
                print(Back.BLUE, end="")

            if y == CROSS:
                print("X", end="")
            elif y == ZERO:
                print("O", end="")
            else:
                print("_", end="")

            print(Back.RESET, end="")
        print()

def is_position_valid(pos: Position) -> bool:
    if ((pos.x >= 0 and pos.x < len(game_state.field)) and
        (pos.y >= 0 and pos.y < len(game_state.field[0]))):
        return True
    return False

def place(type: int, pos: Position) -> bool:
    global game_state
    if not is_position_valid(pos): return False
    if game_state.field[pos.x][pos.y] == EMPTY:
        game_state.field[pos.x][pos.y] = type
        return True
    return False

def parse_position(inp: str) -> Position:
    tmp = inp.strip().split(" ")
    if len(tmp) != 2:
        return NULL_POS
    y, x = map(int, tmp)
    return Position(x, y)

def next_turn() -> str:
    if game_state.turn == CROSS:
        return ZERO
    return CROSS


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
    for line in game_state.field:
        if is_all_items_same(line) and line[0] != EMPTY:
            return (True, line[0])

    for i in range(len(game_state.field[0])):
        column = get_column(game_state.field, i)
        if is_all_items_same(column) and column[0] != EMPTY:
            return (True, column[0])

    if (game_state.field[0][0] == game_state.field[1][1] and game_state.field[0][0] == game_state.field[2][2]) and game_state.field[0][0] != EMPTY:
        return (True, game_state.field[0][0])
    if (game_state.field[2][0] == game_state.field[1][1] and game_state.field[2][0] == game_state.field[0][2]) and game_state.field[2][0] != EMPTY:
        return (True, game_state.field[2][0])

    return (False, EMPTY)

def is_tie() -> bool:
    win, type = is_win()
    if not win:
        for line in game_state.field:
            for cell in line:
                if cell == -1:
                    return False
    return True


GET_PLAYER = "get_player"
GET_CURRENT_STATE = "get_current_state"
UPDATE_CURRENT_STATE = "update_current_state|"

def build_update() -> str:
    # return UPDATE_CURRENT_STATE + json.dumps(field)
    return UPDATE_CURRENT_STATE + game_state.to_json()

SINGLEPLAYER_MODE = False

HOST = ""
PORT = 0

async def main():
    global game_state, player, CURRENT_POS, HOST, PORT

    if not SINGLEPLAYER_MODE:
        if HOST == "" and PORT == 0:
            addr = input("Input server address [ip:port] (blank for localhost:8765): ")
            if addr == "":
                HOST = "localhost"
                PORT = 8765
            else:
                HOST = addr.split(":")[0]
                PORT = int(addr.split(":")[1])
        if HOST == "":
            HOST = "localhost"
        if PORT == 0:
            PORT = 8765

        uri = "ws://" + HOST + ":" + str(PORT)

        async with websockets.connect(uri) as websocket:
            await websocket.send(GET_PLAYER)
            player = int(await websocket.recv())

        if player == -1:
            print("You should wait for first player turn or this game is full!")
            return

        async with websockets.connect(uri) as websocket:
            await websocket.send(GET_CURRENT_STATE)
            game_state_json = await websocket.recv()
            game_state = GameState(game_state_json)
    else:
        game_state = GameState()
        game_state.field = [
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1]
        ]
        game_state.turn = CROSS


    # print("PLAYER", player)
    # print("gamestate", game_state.to_json())

    while True:
        # CLEAR()
        draw_field()
        # if SINGLEPLAYER_MODE:
        #     print("Now goes " + ("CROSS" if game_state.turn == CROSS else "ZERO"))
        # else:
        #     print("NOW YOUR TURN!")

        # pos = parse_position(input("Input pos: x y "))

        # CURRENT_POS = Position(0, 0)
        ch = getch()
        while ch != b'\r':
            # print("CUR_POS:", CURRENT_POS.x, CURRENT_POS.y)
            if ch == b'w':
                if CURRENT_POS.x > 0:
                    CURRENT_POS.x -= 1
            elif ch == b's':
                if CURRENT_POS.x < len(game_state.field) - 1:
                    CURRENT_POS.x += 1
            elif ch == b'a':
                if CURRENT_POS.y > 0:
                    CURRENT_POS.y -= 1
            elif ch == b'd':
                if CURRENT_POS.y < len(game_state.field[0]) - 1:
                    CURRENT_POS.y += 1
            # CLEAR()
            draw_field()
            ch = getch()
            if ch == b'q':
                return

        pos = CURRENT_POS
        if pos == NULL_POS:
            print("Error while parsing a position")
            continue
        if not place(game_state.turn, pos):
            print("Error while placing")
            continue

        # print(pos.x, pos.y)
        # print(game_state.to_json())
        game_state.turn = next_turn()

        if not SINGLEPLAYER_MODE:
            async with websockets.connect(uri) as websocket:
                await websocket.send(build_update())

        win, type = is_win()
        if win:
            # CLEAR()
            draw_field()
            if SINGLEPLAYER_MODE:
                print( ("CROSS" if type == CROSS else "ZERO") + " wins!!!" )
            else:
                if type == player:
                    print("You won!")
                else:
                    print("You lost!")
            break

        if is_tie():
            # CLEAR()
            draw_field()
            print("It`s TIE!!!")
            break

        # print(win)
        # input("Enter for next turn")

        # CLEAR()
        draw_field()

        if not SINGLEPLAYER_MODE:

            tmp_game_state = game_state
            while tmp_game_state.turn == game_state.turn:
                async with websockets.connect(uri) as websocket:
                    await websocket.send(GET_CURRENT_STATE)
                    tmp_game_state = GameState(await websocket.recv())
                await asyncio.sleep(1)

            game_state = tmp_game_state

        win, type = is_win()
        if win:
            # CLEAR()
            draw_field()
            if SINGLEPLAYER_MODE:
                print( ("CROSS" if type == CROSS else "ZERO") + " wins!!!" )
            else:
                if type == player:
                    print("You won!")
                else:
                    print("You lost!")
            break

        if is_tie():
            # CLEAR()
            draw_field()
            print("It`s TIE!!!")
            break

        # if pos.x == 88:
        #     break

if __name__ == "__main__":
    argv = sys.argv
    if "--debug" in argv or "-d" in argv:
        DEBUG = True
    if "--singleplayer" in argv or "-sp" in argv:
        SINGLEPLAYER_MODE = True

    if "--host" in argv:
        HOST = argv[argv.index("--host") + 1]
    if "-h" in argv:
        HOST = argv[argv.index("-h") + 1]
    if "--port" in argv:
        PORT = argv[argv.index("--port") + 1]
    if "-p" in argv:
        PORT = argv[argv.index("-p") + 1]
    #
    # print(HOST)
    # print(PORT)

    asyncio.run(main())
