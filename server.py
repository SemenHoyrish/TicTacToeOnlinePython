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

async def game(websocket):
    global game_state, player_1, player_2
    request = await websocket.recv()
    if request.startswith("get_player"):
        if not player_1:
            await websocket.send("1")
            print("Player 1 connected!")
            player_1 = True
        elif not player_2:
            await websocket.send("2")
            print("Player 2 connected!")
            player_2 = True
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
    async with websockets.serve(game, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
