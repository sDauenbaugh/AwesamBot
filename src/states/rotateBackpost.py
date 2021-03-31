from states import State
import util.util as util
from util.vec import Vec3
from util.gameinformation import GameInformation


class RotateBackpost(State):

    def __init__(self):
        super().__init__()

    def check_expired(self, game_info: GameInformation) -> bool:
        # expired if ball is of wrong half or on direct trajectory toward goal
        # check if ball on defensive half
        ball_location = game_info.ball.location
        if util.sign(ball_location.y) != util.sign(game_info.me.team):
            self.expired = True
        # check direction of ball movement
        ball_direction = game_info.ball.velocity


        return self.expired

    def execute(self, game_info: GameInformation):
        pass
