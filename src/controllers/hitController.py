import math
import time

from rlbot.agents.base_agent import SimpleControllerState

from controllers.groundController import ground_controller
from util import util
from util.orientation import relative_location


def hit_controller(game_info, hit_target):
    """Gives a set of commands to make the car shoot the ball

    This function will flip the car into the ball in order to make a shot and
    it will adjust the car's speed and positioning to help make the shot.

    Attributes:
        hit_target (Vec3): The position that we want to hit the ball toward

    Returns:
        SimpleControllerState: the set of commands to achieve the goal
    """
    controller_state = SimpleControllerState()
    # get ball distance and angle from car
    ball_direction = game_info.ball.local_location
    ball_distance = game_info.ball.local_location.flat().length()
    ball_angle = -math.atan2(ball_direction.y, ball_direction.x)
    if ball_angle > math.pi:
        ball_angle -= 2 * math.pi
    elif ball_angle < -math.pi:
        ball_angle += 2 * math.pi
    # get target distance and angle from ball
    ball_to_target = game_info - game_info.ball.location
    target_distance = ball_to_target.length()
    ball_to_target_unit = ball_to_target.normalized()
    flip_ready = False
    if ball_distance < 400:
        flip_ready = True

    # flipping
    if flip_ready:
        time_diff = time.time() - game_info.timer1
        if time_diff > 2.2:
            game_info.timer1 = time.time()
        elif time_diff <= 0.1:
            # jump and turn toward the ball
            controller_state.jump = True
            if ball_angle > 0:
                controller_state.yaw = -1
            elif ball_angle < 0:
                controller_state.yaw = 1
        elif 0.1 <= time_diff <= 0.15:
            # keep turning
            controller_state.jump = False
            if ball_angle > 0:
                controller_state.yaw = -1
            elif ball_angle < 0:
                controller_state.yaw = 1
        elif 0.15 < time_diff < 1:
            # flip
            controller_state.jump = True
            if ball_angle > 0:
                controller_state.yaw = -1
            elif ball_angle < 0:
                controller_state.yaw = 1
            if math.fabs(ball_angle) > math.pi:
                controller_state.pitch = 1
            else:
                controller_state.pitch = -1
        else:
            flip_ready = False
            controller_state.jump = False
    else:
        aim_location = game_info.ball.location - (ball_to_target_unit * util.BALL_RADIUS)
        local_target = relative_location(game_info.me.location, game_info.me.rotation, aim_location)
        controller_state = ground_controller(game_info, local_target)

    return controller_state
