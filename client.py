import asyncio
import websockets
import json
from os import system
from GameState import GameState

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

def CLEAR():
    if PLATFORM == PLATFORM_WIN:
        system("cls")
    else:
        print("Platform not supported!")

def draw_field():
    for x in game_state.field:
        for y in x:
            if y == CROSS:
                print("X", end="")
            elif y == ZERO:
                print("O", end="")
            else:
                print("_", end="")
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

GET_PLAYER = "get_player"
GET_CURRENT_STATE = "get_current_state"
UPDATE_CURRENT_STATE = "update_current_state|"

def build_update() -> str:
    # return UPDATE_CURRENT_STATE + json.dumps(field)
    return UPDATE_CURRENT_STATE + game_state.to_json()

async def main():
    global game_state, player
    uri = "ws://localhost:8765"


    async with websockets.connect(uri) as websocket:
        await websocket.send(GET_PLAYER)
        player = int(await websocket.recv())

    if player == -1:
        print("Game is full!")
        return

    async with websockets.connect(uri) as websocket:
        await websocket.send(GET_CURRENT_STATE)
        game_state_json = await websocket.recv()
        game_state = GameState(game_state_json)

    # print("PLAYER", player)
    # print("gamestate", game_state.to_json())

    while True:
        CLEAR()
        draw_field()
        # print("Now goes " + ("CROSS" if game_state.turn == CROSS else "ZERO"))
        print("NOW YOUR TURN!")
        pos = parse_position(input("Input pos: x y "))
        if pos == NULL_POS:
            print("Error while parsing a position")
            continue
        if not place(game_state.turn, pos):
            print("Error while placing")
            continue

        # print(pos.x, pos.y)
        # print(game_state.to_json())
        game_state.turn = next_turn()

        async with websockets.connect(uri) as websocket:
            await websocket.send(build_update())

        win, type = is_win()
        if win:
            CLEAR()
            draw_field()
            # print( ("CROSS" if type == CROSS else "ZERO") + " wins!!!" )
            if type == player:
                print("You won!")
            else:
                print("You lost!")
            break

        # print(win)
        # input("Enter for next turn")

        CLEAR()
        draw_field()

        tmp_game_state = game_state
        while tmp_game_state.turn == game_state.turn:
            async with websockets.connect(uri) as websocket:
                await websocket.send(GET_CURRENT_STATE)
                tmp_game_state = GameState(await websocket.recv())
            await asyncio.sleep(1)

        game_state = tmp_game_state

        win, type = is_win()
        if win:
            CLEAR()
            draw_field()
            # print( ("CROSS" if type == CROSS else "ZERO") + " wins!!!" )
            if type == player:
                print("You won!")
            else:
                print("You lost!")
            break

        # if pos.x == 88:
        #     break

if __name__ == "__main__":
    asyncio.run(main())
