from dmx_test import SimpleFadeController
from array import array
from ola.ClientWrapper import ClientWrapper
import random
import time

UPDATE_INTERVAL = 25 # In ms, this comes about to ~40 frames a second
SHUTDOWN_INTERVAL = 3600 # in ms
UNIVERSE = 3

def run_animation():
    wrapper = ClientWrapper()
    controller = SimpleFadeController(UNIVERSE, UPDATE_INTERVAL, wrapper)
    # Call it initially
    wrapper.AddEvent(SHUTDOWN_INTERVAL, wrapper.Stop)
    # Start the wrapper
    wrapper.Run()

    wrapper = None
    controller = None
    time.sleep(1)

if __name__ == '__main__':
    i = 0
    while i < 10:
        run_animation()
        i += 1
