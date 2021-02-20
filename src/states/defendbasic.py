import math

from util.gameinformation import GameInformation
from states.state import State
import util.util as util
from util.vec import Vec3
from util.orientation import relative_location

from rlbot.agents.base_agent import SimpleControllerState

from controllers.groundController import ground_controller


class Defend(State):
    """Defend attempts to divert the ball away from the bot's own goal"""

    def __init__(self):
        """Creates an instance of Defend"""
        super().__init__()

    def check_expired(self, game_info: GameInformation) -> bool:
        if util.sign(game_info.ball.location.y) != util.sign(game_info.me.team):
            self.expired = True
        return self.expired

    def execute(self, game_info):
        # aim to hit ball to the side
        # detect of ball is east or west of bot
        east_multiplier = util.sign(game_info.me.location.x - game_info.ball.location.x)
        # aim for side of the ball
        aim_location = game_info.ball.location + Vec3(east_multiplier * util.BALL_RADIUS, 0, 0)
        target_location = relative_location(game_info.me.location, game_info.me.rotation, aim_location)
        self.debug['target'] = aim_location

        return ground_controller(game_info, target_location)

