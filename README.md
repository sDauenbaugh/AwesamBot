# AwesamBot

## Author: Sam Dauenbaugh

See my previous bot, FirstBot, [here](https://www.github.com/sDauenbaugh/FirstBot).

## Bot Overview

AwesamBot is a 1v1 generalist bot. The bot operates through a state machine model.

- Overall bot behavior is controlled by `src/bot.py`
- Bot appearance is controlled by `src/appearance.cfg`
- States are contained in `src/states/`
- Controllers are contained in `src/controllers/`
- Useful utility functions can be found in `src/util/`

## State Overview

This section outlines the intended behavior of each implemented state. States are immutable objects held by the bot to 
determine functionality. The bot is responsible for selecting a state, and the state is responsible for giving a set of 
commands to achieve its goal.

### Ball Chase

This state causes the bot to drive directly toward the ball at all times. This is the default state of the bot, and so 
it will cede control to any other state.

### Basic Defend

In this defensive state the bot will try to push the ball off to the side. This is intended for when the ball is moving 
toward the net and no other defensive state can be triggered.

### Shoot
This state attempts to push the ball toward the opponents net. Currently this state uses a "dumb" implementation and 
does not aim well.

## States In Development

### Aim Shot

This state will make the bot flip into the ball to take a shot toward the opponent's goal.

### Kickoff

This state will initiate a sequence of pre-programmed inputs during a kickoff.

## Controllers

Controllers are used to translate data generated by a state into a set of inputs that dictate the bot's movement. When 
more states are available information will be added here.