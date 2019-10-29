from dmx_test import SimpleFadeController
from array import array
from ola.ClientWrapper import ClientWrapper
from gpiozero import MCP3008
import random
import time

UPDATE_INTERVAL = 25 # In ms, this comes about to ~40 frames a second
SHUTDOWN_INTERVAL = 5200 # in ms

pot = MCP3008(0)

UNIVERSE_1 = 1
UNIVERSE_2 = 2
UNIVERSE_3 = 3

def run_strip_animation():
    wrapper = ClientWrapper()
    controller = SimpleFadeController(UPDATE_INTERVAL, wrapper)
    wrapper.AddEvent(SHUTDOWN_INTERVAL, wrapper.Stop)
    wrapper.Run()

    #Clears the variables, to prevent scope pollution
    wrapper = None
    controller = None

if __name__ == '__main__':
    while True:
      print(pot.value)
