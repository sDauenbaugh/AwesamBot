from states.state import State

from rlbot.agents.base_agent import SimpleControllerState
from controllers.groundController import ground_controller

from util import util
from util.gameinformation import GameInformation


class Shoot(State):
    """Shoot aims to drive the ball into position to take a shot and then flip into the ball to shoot

        This State has no regard for other cars or the movement of the ball.

        Note:
            This state expires when the opponent clears the ball or when the shot has been made

        """

    def __init__(self):
        """Creates an unexpired instance of Shoot"""
        super().__init__()

    def get_expired(self, game_info: GameInformation):
        """Determines if the state is no longer useful"""
        if util.sign(game_info.ball.location.y) == util.sign(game_info.team):
            self.expired = True

    def execute(self, game_info: GameInformation):
        """Attempts to drive into the ball in a direction that hits the ball towards the goal.

        Overrides the State class's execute function.
        The ground controller is automatically used.
        The target location is on the outside of the ball on a line connecting the ball and the opponents goal.

        Attributes:
            game_info: information detailing the current status of various game objects

        """

        team = util.sign(game_info.me.team)
        target_goal = util.GOAL_HOME * -team

        ball_to_goal = target_goal - game_info.ball.location
        # distance_to_goal = ball_to_goal.length()
        direction_to_goal = ball_to_goal.normalized()

        aim_location = game_info.ball.location - (direction_to_goal * util.BALL_RADIUS)
        local_target = util.relative_location(game_info.me.location, game_info.me.rotation, aim_location)

        return ground_controller(game_info, local_target)
