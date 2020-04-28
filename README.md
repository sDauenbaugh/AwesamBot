# AwesamBot

## Author: Sam Dauenbaugh

See my previous bot, FirstBot, [here](https://www.github.com/sDauenbaugh/FirstBot).

## Bot Overview

This bot operates through a state machine model.

- Bot behavior is controlled by `src/bot.py`
- Bot appearance is controlled by `src/appearance.cfg`
- States are contained in `src/states/`
- Controllers are contained in `src/controllers/`

## State Overview

This section outlines the intended behavior of each implemented state. States are immutable objects held by the bot to determine functionality. The bot is responsible for selecting a state, and the state is responsible for giving a set of commands to achieve it's goal.

### Ball Chase

This state causes the bot to drive directly toward the ball at all times. This is the default state of the bot, and so it will cede control to any other state. The ground controller is the only controller used by this state.

### Basic Defend

In this defensive state the bot will try to push the ball off to the side. This is intended for when the ball is moving toward the net and no other defensive state can be triggered. The ground controller is the default controller for this state.

## Controller Overview

This section outlines the basic use case for each controller. The purpose of a controller is to dictate how the bot moves to achieve the goal governed by the state.

### Ground Controller

The ground controller is the most basic controller available. It operates by turning the bot directly toward a target location and then moving to that location. This controller does not attempt to conserve boost, flip, jump, or aerial.

## States In Development

### Calcshot

This state will make the bot flip into the ball to take a shot toward the opponent's goal.

### GetBack

This state will return the bot to a defensive position in goal.

### GetBoost

This state will grab the boost based on how much boost the bot has, where boost pads are, and where the ball is.