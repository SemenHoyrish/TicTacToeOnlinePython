import json

class GameState:
    field = []
    # player = -1
    turn = -1
    def __init__(self, json_obj="") -> None:
        if json_obj != "":
            obj = json.loads(json_obj)
            self.field = obj["field"]
            # self.player = obj["player"]
            self.turn = obj["turn"]

    def to_json(self) -> str:
        # res = "{\"field\": " + json.dumps(self.field) + ", \"player\": " + json.dumps(self.player) + ", \"turn\":" + json.dumps(self.turn) + "}"
        res = "{\"field\": " + json.dumps(self.field) + ", \"turn\":" + json.dumps(self.turn) + "}"
        return res
