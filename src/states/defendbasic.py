import math

from src.states.state import State
import src.util.util as util
from src.util.vec import Vec3
from src.util.orientation import relative_location

from rlbot.agents.base_agent import SimpleControllerState

class Defend(State):
    """Defend attempts to divert the ball away from the bot's own goal"""
    def __init__(self):
        """Creates an instance of Defend"""
        super().__init__()
        
    def checkAvailable(self, agent):
        """Available when the ball is on the friendly side of the field"""
        if util.sign(agent.ball.location.y) == util.sign(agent.team):
            return True
        return False
    
    def checkExpired(self, me, ball):
        if util.sign(ball.location.y) != util.sign(me.team):
            self.expired = True
    
    def execute(self, me, ball):
        self.checkExpired(me, ball)

        #aim to hit ball to the side
        #detect of ball is east or west of bot
        east_multiplier = util.sign(ball.location.x - me.location.x)
        #aim for side of the ball
        aim_location = ball.location + Vec3(east_multiplier * util.BALL_RADIUS, 0, 0)
        target_location = relative_location(me.location, me.rotation, aim_location)

        return target_location