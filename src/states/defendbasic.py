import math

from src.states.state import State
import src.util.util as util
from src.util.vec import Vec3
from src.util.orientation import relative_location

from rlbot.agents.base_agent import SimpleControllerState

from src.controllers.groundController import groundController

class Defend(State):
    """Defend attempts to divert the ball away from the bot's own goal"""
    def __init__(self):
        """Creates an instance of Defend"""
        super().__init__()
    
    def getExpired(self, gameInfo):
        if util.sign(gameInfo.ball.location.y) != util.sign(gameInfo.me.team):
            self.expired = True
    
    def execute(self, gameInfo):
        #aim to hit ball to the side
        #detect of ball is east or west of bot
        east_multiplier = util.sign(gameInfo.ball.location.x - gameInfo.me.location.x)
        #aim for side of the ball
        aim_location = gameInfo.ball.location + Vec3(east_multiplier * util.BALL_RADIUS, 0, 0)
        target_location = relative_location(gameInfo.ball.location, gameInfo.me.rotation, aim_location)

        return groundController(gameInfo, target_location)