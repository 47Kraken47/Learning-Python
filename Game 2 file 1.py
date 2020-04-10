# Louis McCracken #
# Game 2 (original) #

import sys
import math
import random
import threading
import time
import cmd
import textwrap
import os


# Player Setup #
class player():
    def __init__(self):
        self.name = ''
        self.role = ''
        self.ability = ''
        self.game_over = False

myPlayer = player()

# game interactivity #

def prompt():
    print("\n")
    print("You see a man acting loud n hes talking down on ur name\n")
    print("Would you like to use your ability or do nothing?\n")
    print("If you have forgotten your ability type 'show ability'\n")
    action = input("> ")
    acceptable_actions = ['yes', 'no', 'ability', 'nothing', 'quit', 'show ability']
    while action.lower() not in acceptable_actions:
        print("Unknown answer, try again.\n")
        action = input("> ")
    if action.lower() == 'quit':
        sys.exit()
    elif action.lower() in ['yes', 'ability']:
        print("ADD PLAYER ACTION")
        #player_ability(action.lower())
    elif action.lower() in ['no', 'nothing']:
        print("ADD RESULT")
        #player_nothing(action.lower())
    elif action.lower() in ['show ability']:
        showability = myPlayer.ability + "\n"
        for character in showability:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.03)
        time.sleep(1)

        #player_nothing(action.lower())


# game functionality #

def main_game_loop():
    while myPlayer.game_over is False:
        prompt()

def setup_game():
    # name collecting #
    question1 = "Hello, what is your name?\n"
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)
    player_name = input("> ")
    myPlayer.name = player_name

    # role collecting #
    question2 = "Hello " + player_name + ", what is your profession?\n"
    question2added = "(You can play as a snitch, roadman or stoner)\n"
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)
    for character in question2added:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)
    player_role = input("> ")

    roadman_role = ['roadman']
    stoner_role = ['stoner']
    snitch_role = ['snitch']

    if player_role.lower() in roadman_role:
        myPlayer.role = player_role
        myPlayer.ability = 'Can ching any man up no matter how much street cred they got'
        print("You are now a " + player_role + "! Good luck cheffing down man til da soles red!\n")
    elif player_role.lower() in snitch_role:
        myPlayer.role = player_role
        myPlayer.ability = 'Can call the police and get anyone bagged up.'
        print("You are now a " + player_role + "! how fucking bent...\n")
    elif player_role.lower() in stoner_role:
        myPlayer.role = player_role
        myPlayer.ability = 'Can smoke a fat head and make everyone fall asleep'
        print("You are now a " + player_role + "! I got dat high grade stinky ched if u need g.\n")
#    while player_role.lower() not in roadman_role or snitch_role or stoner_role:
#        player_role = input("> ")
#        if player_role.lower() in roadman_role:
#            myPlayer.role = player_role
#            myPlayer.ability = 'can ching any man up no matter how much street cred they got'
#            print("You are now a " + player_role + "! Good luck cheffing down man til da soles red!\n")
#        elif player_role.lower() in snitch_role:
#            myPlayer.role = player_role
#            myPlayer.ability = 'can call the police and get anyone bagged up.'
#            print("You are now a " + player_role + "! how fucking bent...\n")
#        elif player_role.lower() in stoner_role:
#            myPlayer.role = player_role
#            myPlayer.ability = 'can smoke a fat head and make everyone fall asleep'
#            print("You are now a " + player_role + "! I got dat high grade stinky ched if u need g.\n")

        # player introduction #
        speech1 = "welcome, " + player_name + " the " + player_role + '\n'
        for character in speech1:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.02)
        speech2 = "To this pointless game...\n"
        for character in speech2:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.03)
        speech3 = "I hope you enjoy it!\n"
        for character in speech3:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.02)
        speech4 = "Just try and not get bagged up or put 6 feet under...\n"
        for character in speech4:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.05)
        speech5 = "Also because your a " + player_role + ", you " + myPlayer.ability + "\n"
        for character in speech5:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.03)
    time.sleep(1)
    print("\n")
    print("#########################")
    print("#  - Lets start now! -  #")
    print("#########################")
    main_game_loop()


setup_game()