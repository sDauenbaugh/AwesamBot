import math

from rlbot.agents.base_agent import SimpleControllerState

from controllers.groundController import ground_controller
from states import State
from util.gameinformation import GameInformation
from util.sequence import Sequence, ControlStep, flip_sequence


class Kickoff(State):

    def __init__(self):
        super().__init__()
        self.flipped = False

    def check_expired(self, game_info: GameInformation) -> bool:
        self.expired = True
        return self.expired

    def execute(self, game_info: GameInformation):
        self.debug["target"] = game_info.ball.location
        # flip once when at appropriate distance
        if self.flipped is False and (game_info.me.location - game_info.ball.location).length() < 3600:
            self.flipped = True
            angle = -math.atan2(game_info.ball.local_location.y, game_info.ball.local_location.x)

            if angle > math.pi:
                angle -= 2 * math.pi
            elif angle < -math.pi:
                angle += 2 * math.pi
            self.sequence = flip_sequence(angle=angle, boosting=True)
        # otherwise steer toward ball and boost
        else:
            target = game_info.ball.local_location
            self.next_controller_state = ground_controller(game_info, target)
            self.next_controller_state.boost = True
            self.next_controller_state.throttle = 1
