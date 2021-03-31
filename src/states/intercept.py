from util.gameinformation import GameInformation


class State:

    def __init__(self):
        super().__init__()

    def check_expired(self, game_info: GameInformation) -> bool:
        return self.expired

    def execute(self, game_info: GameInformation):
        pass
