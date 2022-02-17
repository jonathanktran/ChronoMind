# ChronoMind

 A UCSD Cogs 189 Project. This is a time-slowing bullet-hell game which uses the NeuroSky headset to augment the flow of
 time in the game.

## Setup

In your console, run the following commands from within the ChronoMind directory:

`pip install virtualenv`

`virtualenv common\venv`

`common\venv\Scripts\activate`

`pip install pipwin`

`pipwin install pyaudio`

`pip install -r common/requirements.txt`

## How to Modify the Gameplay

### Overview

Enemies are the objects in the game which can hit the player.

Rounds are an object which spawns a series of enemies.

Each of these objects spawn at a set time, which is defined the the `timeline.py` file.

### How to Start

The only file you will need to open will be the `timeline.py` file.

Scroll down to the `Timeline Creation` region.

Call the `add` function to add an `Enemy` or `Round` to the game.

The `add` function takes in a `time` to spawn the round in ms, and an instantiated `Enemy` or `Round`.

### Creating Enemies

To create an `Enemy`, look in the `enemies.py` file to see all currently defined instances.

Read the documentation to find the initialization documentation for whichever enemy you choose.

Use the defined `speed`, `direction`, `position`, and `color` constants defined in the `timeline.py` file to 
instantiate your enemies more easily.

Pick a time in ms to spawn the enemy at, and call the `add` function to add the enemy to the timeline at the given time.

*Example:*

`add(1000, enemies.Bullet(MIDDLE_RIGHT, SLOW_LEFT, GREEN))`

This function adds a `Bullet` `Enemy` at 1 second into the game, starting at the center of the right edge of the screen, 
going slowly to the left, colored green.

### Creating Rounds

To create an `Round`, look in the `rounds.py` file to see all currently defined instances.

Read the documentation to find the initialization documentation for whichever round you choose.

Use the defined `speed`, `direction`, `position`, and `color` constants defined in the `timeline.py` file to 
instantiate your rounds more easily.

Ensure that you are passing Enemy classes, and not instantiated enemies, to the round's initialization. 

Pick a time in ms to spawn the round at, and call the `add` function to add the round to the timeline at the given time.

*Example:*

`add(1000, rounds.Straight(enemies.Bullet, MIDDLE_RIGHT, SLOW_LEFT, GREEN, 100, 50))`

This function adds a `Round` at 1 second into the game, which spawns a `Bullet` `Enemy` at the center of the right edge
of the screen every 50 ms. These `Bullets` travel slowly to the left, and are green. The round will stop once it spawns
100 enemies.