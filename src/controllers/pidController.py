import numpy as np
from rlbot.agents.base_agent import SimpleControllerState


class PID:

    def __init__(self, kp, ki, kd):
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        self.last_err = 0
        self.sum_err = 0
        self.err = 0

    def update(self, e_t):
        self.sum_err = self.sum_err + e_t
        term_p = self.Kp * e_t
        term_i = self.Ki * self.sum_err
        term_d = self.Kd * (self.last_err - e_t)
        self.last_err = e_t
        return term_p + term_i + term_d


class SteerPID(PID):

    def __init__(self):
        super().__init__(10, 0.01, 0.001)

    def get_steer(self, ang_to_target):  # angle should be in radians
        err = ang_to_target / (2 * np.pi)
        u_t = self.update(-err)
        if u_t > 1:
            u_t = 1
        elif u_t < -1:
            u_t = -1
        return u_t


def pid_steer(game_info, target_location, pid: SteerPID):
    """Gives a set of commands to move the car along the ground toward a target location

    Attributes:
        target_location (Vec3): The local location the car wants to aim for

    Returns:
        SimpleControllerState: the set of commands to achieve the goal
    """
    controller_state = SimpleControllerState()
    ball_direction = target_location

    angle = -np.arctan2(ball_direction.y, ball_direction.x)

    if angle > np.pi:
        angle -= 2 * np.pi
    elif angle < -np.pi:
        angle += 2 * np.pi

    # adjust angle
    turn_rate = pid.get_steer(angle)

    controller_state.throttle = 1
    controller_state.steer = turn_rate
    controller_state.jump = False
    return controller_state
