from dmx_test import SimpleFadeController
from array import array
from ola.ClientWrapper import ClientWrapper
import random
import time

UPDATE_INTERVAL = 25 # In ms, this comes about to ~40 frames a second
SHUTDOWN_INTERVAL = 3600 # in ms

def run_animation(output_universe):
    wrapper = ClientWrapper()
    controller = SimpleFadeController(output_universe, UPDATE_INTERVAL, wrapper)
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
        run_animation(1)
        run_animation(2)
        run_animation(3)
        i += 1
