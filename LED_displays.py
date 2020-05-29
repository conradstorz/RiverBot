#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Provide routines to update connected displays such as SenseHat or another LED matrix

TODO
    Create OOP implementation. methods: display_text,init,display_color,...
"""
from loguru import logger

logger.remove()  # stop any default logger
LOGGING_LEVEL = "INFO"

# detect various add-on Rpi hats
try:
    SenseHatLoaded = True
    from sense_hat import SenseHat
    from random_colors import Set_Random_Pixels, random_to_solid

    SENSEHAT = SenseHat()
except ImportError as e:
    SenseHatLoaded = False

logger.info(f"Sense Hat loaded: {SenseHatLoaded}")

@logger.catch
def DisplayMessage(message):
    global SENSEHAT
    if SenseHatLoaded:
        # TODO add additonal data like temp and humidity of server hat
        SENSEHAT.show_message(message)
        time.sleep(1)
        # TODO monitor joystick input to exit pixel display early
        lastColor = Set_Random_Pixels(SENSEHAT)
        random_to_solid(SENSEHAT, colorName=lastColor, fast=True)
    return True
