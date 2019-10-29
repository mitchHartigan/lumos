from dmx_test import SimpleFadeController
from array import array
from ola.ClientWrapper import ClientWrapper
from gpiozero import MCP3008
from time import sleep
import random
import time

UPDATE_INTERVAL = 25 # In ms, this comes about to ~40 frames a second
SHUTDOWN_INTERVAL = 5200 # in ms

pot = MCP3008(0)
wrapper = ClientWrapper()

UNIVERSE_1 = 1
UNIVERSE_2 = 2
UNIVERSE_3 = 3

def run_strip_animation(wrapper):
    controller = SimpleFadeController(UPDATE_INTERVAL, wrapper)
    wrapper.AddEvent(SHUTDOWN_INTERVAL, wrapper.Stop)
    wrapper.Run()
    
    wrapper = None
    controller = None

if __name__ == '__main__':
    pot_val = pot.value * 100
    while True:
        print(pot_val)
        if pot_val == pot.value * 100:
            # nothing has changed.
            i = 0
            while i < 10:
                run_strip_animation(wrapper)
                i += 1
        else:
            # the value has changed.
            pot_val = pot.value * 100
            wrapper.Stop()




