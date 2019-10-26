from dmx_test import SimpleFadeController
from array import array
from ola.ClientWrapper import ClientWrapper
import random
import time

UPDATE_INTERVAL = 25 # In ms, this comes about to ~40 frames a second
SHUTDOWN_INTERVAL = 4300 # in ms

def run_animation():
    wrapper = ClientWrapper()
    controller = SimpleFadeController(1, UPDATE_INTERVAL, wrapper)
    # Call it initially
    # Start the wrapper
    controller2 = SimpleFadeController(2, UPDATE_INTERVAL, wrapper )

    controller3 = SimpleFadeController(3, UPDATE_INTERVAL, wrapper)

    wrapper.AddEvent(SHUTDOWN_INTERVAL, wrapper.Stop)

    wrapper.Run()
if __name__ == '__main__':
    i = 0
    while i < 10:
        run_animation()
        i += 1
