import math

from controllers.hitController import hit_controller
from states.state import State
from util import util
from util.gameinformation import GameInformation
from util.orientation import relative_location


class AimShot(State):
    """Aims the shot toward the net"""

    def __init__(self):
        """Creates an instance of AimShot"""
        super().__init__()

    def check_expired(self, game_info: GameInformation):
        """If the ball is not reasonably close to being between the car and the goal, the state expires"""
        ball_direction = game_info.ball.local_location
        goal_location = relative_location(game_info.me.location, game_info.me.rotation,
                                          util.GOAL_HOME * -util.sign(game_info.me.team))
        angle = ball_direction.ang_to(goal_location)
        if angle < (math.pi / 2):
            return False
        return True

    def execute(self, game_info):
        team = util.sign(game_info.me.team)

        self.next_controller_state =  hit_controller(game_info, util.GOAL_HOME * team * -1)
