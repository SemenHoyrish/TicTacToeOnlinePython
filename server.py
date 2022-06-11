import sys
import asyncio
import websockets
import json
from GameState import GameState

game_state = GameState()
game_state.field = [
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1]
]
game_state.turn = 1

player_1 = False
player_2 = False

HOST = ""
PORT = 0

async def game(websocket):
    global game_state, player_1, player_2
    request = await websocket.recv()
    if request.startswith("get_player"):
        if not player_1:
            await websocket.send("1")
            print("Player 1 connected!")
            player_1 = True
        elif not player_2:
            if game_state.turn == 0:
                await websocket.send("2")
                print("Player 2 connected!")
                player_2 = True
            else:
                await websocket.send("-1")
                print("Player 2 should wait")
        else:
            await websocket.send("-1")
    elif request.startswith("get_current_state"):
        await websocket.send(game_state.to_json())
        print("Someone get current state")
    elif request.startswith("update_current_state"):
        game_state = GameState(request.replace("update_current_state|", ""))
        print("Someone update current state")
        print(game_state.to_json())
        await websocket.send("OK")


async def main():
    global HOST, PORT
    if HOST == "" and PORT == 0:
        inp = input("Enter [ip:port] (blank for localhost:8765): ")
        if inp == "":
            HOST = "locahost"
            PORT = 8765
        else:
            HOST = inp.split(":")[0]
            PORT = int(inp.split(":")[1])
    if HOST == "":
        HOST = "localhost"
    if PORT == 0:
        PORT = 0

    async with websockets.serve(game, HOST, PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    argv = sys.argv
    if "--host" in argv:
        HOST = argv[argv.index("--host") + 1]
    if "-h" in argv:
        HOST = argv[argv.index("-h") + 1]
    if "--port" in argv:
        PORT = argv[argv.index("--port") + 1]
    if "-p" in argv:
        PORT = argv[argv.index("-p") + 1]

    asyncio.run(main())
