from rlbot.agents.base_agent import SimpleControllerState

from controllers.groundController import ground_controller
from states import State
from util.drive import steer_toward_target
from util.gameinformation import GameInformation
from util.sequence import Sequence, ControlStep
from util.vec import Vec3


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
            self.sequence = Sequence([
                ControlStep(duration=0.5, controls=SimpleControllerState(boost=True)),
                ControlStep(duration=0.05, controls=SimpleControllerState(jump=True, boost=True)),
                ControlStep(duration=0.05, controls=SimpleControllerState(jump=False, boost=True)),
                ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, pitch=-1, boost=True)),
                ControlStep(duration=0.6, controls=SimpleControllerState()),
            ])
            target = game_info.ball.local_location
            self.next_controller_state = ground_controller(game_info, target)
            self.next_controller_state.boost = True
            self.next_controller_state.throttle = 1
        # otherwise steer toward ball and boost
        else:
            target = game_info.ball.local_location
            self.next_controller_state = ground_controller(game_info, target)
            self.next_controller_state.boost = True
            self.next_controller_state.throttle = 1
