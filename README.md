# AwesamBot

## Author: Sam Dauenbaugh

## Bot Overview

This bot operates through a state machine model.

- Bot behavior is controlled by `src/bot.py`
- Bot appearance is controlled by `src/appearance.cfg`
- States are contained in `src/states/`
- Controllers are contained in `src/controllers/`

## State Overview

This section outlines the intended behavior of each implemented state.

### Ball Chase

This state causes the bot to drive directly toward the ball at all times. This is the default state of the bot, and so it will cede control to any other state.
The ground controller is the only controller used by this state.

## Controller Overview

This section outlines the basic use case for each controller. The purpose of a controller is to dictate how the bot moves to achieve the goal governed by the state.

### Ground Controller

The ground controller is the most basic controller available. It operates by turning the bot directly toward a target location and then moving to that location. There is no
boost or drifting in this controller and the controller will not attempt to leave the ground.
