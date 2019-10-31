from dmx_test import SimpleFadeController
from array import array
from ola.ClientWrapper import ClientWrapper
from gpiozero import MCP3008
from time import sleep
import random
import time

UPDATE_INTERVAL = 25 # In ms, this comes about to ~40 frames a second
SHUTDOWN_INTERVAL = 5200 # in ms

UNIVERSE_1 = 1
UNIVERSE_2 = 2
UNIVERSE_3 = 3

pot = MCP3008(0)

def run_strip_animation():
    wrapper = ClientWrapper()
    controller = SimpleFadeController(UPDATE_INTERVAL, wrapper)
    wrapper.AddEvent(SHUTDOWN_INTERVAL, wrapper.Stop)
    wrapper.Run()

    #Clears the variables, to prevent scope pollution
    wrapper = None
    controller = None

if __name__ == '__main__':
    pot_val = pot.value
    while True:
        pot_val *= 100
        if pot_val == pot.value + 1 or pot_val == pot.value - 1: #value fluctuated so would never satisfy "=="
            # pot has been untouched, value is the same
            run_strip_animation()
        else:
            # pot has been turned, value has changed
            pot_val = pot.value
            # stop the system

    
 #while true fucked the code...
    # pot_val = pot.value * 100
    # while True:
    #     if pot_val == pot.value:
    #         # nothing has changed.
    #         i = 0
    #         while i < 10:
    #             run_strip_animation(wrapper)
    #             i += 1
    #     else:
    #         # the value has changed.
    #         pot_val = pot.value
    #         ClientWrapper.Stop