# First Game
# Louis McCracken

import sys
import math
import random
import threading
import time
import cmd
import textwrap
import os

screen_width = 100


# Player Setup #
class player():
    def __init__(self):
        self.name = ''
        self.role = ''
        self.hp = 0
        self.mp = 0
        self.status_effects = []
        self.location = 'b2'
        self.game_over = False


myPlayer = player()


# Title Screen #
def title_screen_selections():
    option = input("> ")
    if option.lower() == "play":
        setup_game()
    elif option.lower() == "help":
        help_menu()
    elif option.lower() == "quit":
        sys.exit()
    while option.lower() not in ['play', 'help', 'quit']:
        print("Please enter a valid command.\n")
        option = input("> ")
        if option.lower() == "play":
            setup_game()
        elif option.lower() == "help":
            help_menu()
        elif option.lower() == "quit":
            sys.exit()


def title_screen():

    print('############################')
    print('# Welcome to the Text RPG! #')
    print('############################')
    print('#         - Play -         #')
    print('#         - Help -         #')
    print('#         - Quit -         #')
    print('############################')
    title_screen_selections()


def help_menu():
    print('#########################################')
    print('#        Welcome to the Text RPG!       #')
    print('#########################################')
    print('# - Use up, down, left, right to move - #')
    print('#   - Type your commands to do them -   #')
    print('#  - Use "Look" to inspect something -  #')
    print('#########################################')
    title_screen_selections()


# Map #

#  a1 a2...
# -------------
# |  |  |  |  | a4
# -------------
# |  |  |  |  | b4...
# -------------
# |  |  |  |  |
# -------------
# |  |  |  |  |
# -------------

ZONE_NAME = ''
DESCRIPTION = 'description'
EXAMINATION = 'examine'
SOLVED = False
UP = 'up', 'north'
DOWN = 'down', 'south'
LEFT = 'left', 'west'
RIGHT = 'right', 'east'

solved_places = {'a1': False, 'a2': False, 'a3': False, 'a4': False,
                 'b1': False, 'b2': False, 'b3': False, 'b4': False,
                 'c1': False, 'c2': False, 'c3': False, 'c4': False,
                 'd1': False, 'd2': False, 'd3': False, 'd4': False,
                 }

zonemap = {
    "a1": {ZONE_NAME: "Town hall",
           DESCRIPTION: "Where the Towns-People congregate.",
           EXAMINATION: "You can apply for Citizenship!",
           SOLVED: False,
           UP: "", DOWN: "b1", LEFT: "", RIGHT: "a2"
           },
    "a2": {ZONE_NAME: "Town Market",
           DESCRIPTION: "Loud with the shouts of traders, the market is busy with foreign goods and food.",
           EXAMINATION: "You can buy items",
           SOLVED: False,
           UP: "", DOWN: "b2", LEFT: "a1", RIGHT: "a3"
           },
    "a3": {ZONE_NAME: "Town Inn",
           DESCRIPTION: "Full of drunkards, shady characters and music.",
           EXAMINATION: "A shady character has a quest for you.",
           SOLVED: False,
           UP: "", DOWN: "b3", LEFT: "a2", RIGHT: "a4"
           },
    "a4": {ZONE_NAME: "Town Blacksmith",
           DESCRIPTION: "The smell of coal and the sounds of an anvil fill the air.",
           EXAMINATION: "You may buy a weapon",
           SOLVED: False,
           UP: "", DOWN: "b3", LEFT: "a3", RIGHT: ""
           },
    "b1": {ZONE_NAME: "",
           DESCRIPTION: "description",
           EXAMINATION: "info",
           SOLVED: False,
           UP: "a1", DOWN: "c1", LEFT: "", RIGHT: "b2"
           },
    "b2": {ZONE_NAME: "Home",
           DESCRIPTION: "This is your home",
           EXAMINATION: "You can sleep here.",
           SOLVED: False,
           UP: "a2", DOWN: "c2", LEFT: "b1", RIGHT: "b3"
           },
    "b3": {ZONE_NAME: "",
           DESCRIPTION: "description",
           EXAMINATION: "info",
           SOLVED: False,
           UP: "a3", DOWN: "c3", LEFT: "b2", RIGHT: "b4"
           },
    "b4": {ZONE_NAME: "",
           DESCRIPTION: "description",
           EXAMINATION: "info",
           SOLVED: False,
           UP: "a4", DOWN: "c4", LEFT: "b3", RIGHT: ""
           },
    "c1": {ZONE_NAME: "",
           DESCRIPTION: "description",
           EXAMINATION: "info",
           SOLVED: False,
           UP: "b1", DOWN: "d1", LEFT: "", RIGHT: "c2"
           },
    "c2": {ZONE_NAME: "",
           DESCRIPTION: "description",
           EXAMINATION: "info",
           SOLVED: False,
           UP: "b2", DOWN: "d2", LEFT: "c1", RIGHT: "c3"
           },
    "c3": {ZONE_NAME: "",
           DESCRIPTION: "description",
           EXAMINATION: "info",
           SOLVED: False,
           UP: "b3", DOWN: "d3", LEFT: "c2", RIGHT: "c4"
           },
    "c4": {ZONE_NAME: "",
           DESCRIPTION: "description",
           EXAMINATION: "info",
           SOLVED: False,
           UP: "b4", DOWN: "d4", LEFT: "c3", RIGHT: ""
           },
    "d1": {ZONE_NAME: "",
           DESCRIPTION: "description",
           EXAMINATION: "info",
           SOLVED: False,
           UP: "c1", DOWN: "", LEFT: "", RIGHT: "d2"
           },
    "d2": {ZONE_NAME: "",
           DESCRIPTION: "description",
           EXAMINATION: "info",
           SOLVED: False,
           UP: "c2", DOWN: "", LEFT: "d1", RIGHT: "d3"
           },
    "d3": {ZONE_NAME: "",
           DESCRIPTION: "description",
           EXAMINATION: "info",
           SOLVED: False,
           UP: "c3", DOWN: "", LEFT: "d2", RIGHT: "d4"
           },
    "d4": {ZONE_NAME: "",
           DESCRIPTION: "description",
           EXAMINATION: "info",
           SOLVED: False,
           UP: "c4", DOWN: "", LEFT: "d3", RIGHT: ""
           },
}

# Game Interactivity #

def print_location():
    print('\n' + ('#' * (4 + len(myPlayer.location))))
    print('# ' + myPlayer.location.upper() + ' #')
    print('# ' + zonemap[myPlayer.location][DESCRIPTION] + ' #')
    print('\n' + ('#' * (4 + len(myPlayer.location))))


def prompt():
    print("\n" + "==================")
    print("What would you like to do?")
    action = input("> ")
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'quit', 'examine', 'inspect', 'interact', 'look',]
    while action.lower() not in acceptable_actions:
        print("Unknown action, try again.\n")
        action = input("> ")
    if action.lower() == 'quit':
        sys.exit()
    elif action.lower() in ['move', 'go', 'travel', 'walk']:
        player_move(action.lower())
    elif action.lower() in ['examine', 'inspect', 'interact', 'look']:
        player_examine(action.lower())


def player_move(action):
    ask = "Where would you like to move to?\n"
    dest = input(ask)
    if dest in ['up', 'north']:
        destination = zonemap[myPlayer.location][UP]
        movement_handler(destination)
    elif dest in ['down', 'south']:
        destination = zonemap[myPlayer.location][DOWN]
        movement_handler(destination)
    elif dest in ['left', 'west']:
        destination = zonemap[myPlayer.location][LEFT]
        movement_handler(destination)
    elif dest in ['right', 'east']:
        destination = zonemap[myPlayer.location][RIGHT]
        movement_handler(destination)


def movement_handler(destination):
    print("\n" + "You have moved to the " + destination + ".")
    myPlayer.location = destination
    print_location()


def player_examine(action):
    if zonemap[myPlayer.location][SOLVED] == True:
        print("You have already exhausted this zone.")
    else:
        print("WORK IN PROGRESS")



# Game functionality #


def main_game_loop():
    while myPlayer.game_over is False:
        prompt()

def setup_game():


    # name collecting #
    question1 = "Hello, what is your name?\n"
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input("> ")
    myPlayer.name = player_name

    # role collecting #
    question2 = "Hello " + player_name + ", what is your role?\n"
    question2added = "(You can play as a warrior, archer or mage)\n"
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in question2added:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.02)
    player_role = input("> ")
    valid_role = ['warrior', 'mage', 'archer']
    if player_role.lower() in valid_role:
        myPlayer.role = player_role
        print("You are now a " + player_role + "!\n")
    while player_role.lower() not in valid_role:
        player_role = input("> ")
        if player_role.lower() in valid_role:
            myPlayer.role = player_role
            print("You are now a " + player_role + "!\n")

    # Player stats #
    #if myPlayer.role == 'warrior':
#        self.hp = 200
 #       self.mp = 0
  #  elif myPlayer.role == 'mage':
  #      self.hp = 100
   #     self.mp = 150
   # elif myPlayer.role == 'archer':
  #      self.hp = 150
  #      self.mp = 50)

    # player introduction #
    question3 = "welcome, " + player_name + " the " + player_role + '\n'
    for character in question3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    speech1 = "Welcome to this fantasy world!\n"
    for character in speech1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.06)
    speech2 = "I hope you enjoy it!\n"
    for character in speech2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    speech3 = "Just try and not get too lost...\n"
    for character in speech3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.09)


    print("#########################")
    print("#  - Lets start now! -  #")
    print("#########################")
    main_game_loop()

title_screen()