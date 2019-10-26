from dmx_test import SimpleFadeController
from array import array
from ola.ClientWrapper import ClientWrapper
import random

UPDATE_INTERVAL = 25 # In ms, this comes about to ~40 frames a second
SHUTDOWN_INTERVAL = 3600 # in ms
UNIVERSE = 1

if __name__ == '__main__':
        wrapper = ClientWrapper()
        controller = SimpleFadeController(UNIVERSE, UPDATE_INTERVAL, wrapper)
        # Call it initially
        wrapper.AddEvent(SHUTDOWN_INTERVAL, wrapper.Stop)
        # Start the wrapper
        wrapper.Run()