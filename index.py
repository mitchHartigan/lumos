from dmx_test import SimpleFadeController
from array import array
from ola.ClientWrapper import ClientWrapper
import random
import time

UPDATE_INTERVAL = 25 # In ms, this comes about to ~40 frames a second
SHUTDOWN_INTERVAL = 4500 # in ms

UNIVERSE_1 = 1
UNIVERSE_2 = 2
UNIVERSE_3 = 3

def run_strip_animation(universe, time_offset):
    wrapper = ClientWrapper()
    controller = SimpleFadeController(universe, UPDATE_INTERVAL, wrapper)
    wrapper.AddEvent(SHUTDOWN_INTERVAL, wrapper.Stop)
    wrapper.Run()

    #Clears the variables, to prevent scope pollution
    wrapper = None
    controller = None

if __name__ == '__main__':
    i = 0
    while i < 10:
        run_strip_animation(UNIVERSE_1, 0)
        run_strip_animation(UNIVERSE_2, 1)
        run_strip_animation(UNIVERSE_3, 2)
        i += 1
