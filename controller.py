from array import array
from ola.ClientWrapper import ClientWrapper
from gpiozero import MCP3008
from time import sleep
import random
import time

class SimpleFadeController(object):
    def __init__(self, update_interval, client_wrapper):
        self._update_interval = update_interval
        self._wrapper = client_wrapper
        self._client = client_wrapper.Client()
        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)
        self._iterable = 1

        # Initialize the unique array for each strip.
        self._universe_one_array = array('B', [])
        self._universe_two_array = array('B', [])
        self._universe_three_array = array('B', [])
        self._universe_four_array = array('B', [])

        # Initialize a data length for each strip.
        # These will update at different rates, as the strips remove array elements at different rates.
        self._universe_one_data_length = 360
        self._universe_two_data_length = 180
        self._universe_three_data_length = 180
        self._universe_four_data_length = 360

    def fillStripWithColor(self, rgb_color_arr, length):
      i = 1
      strip_arr = []
      while i <= length:
        strip_arr.extend(rgb_color_arr)
        i += 1
      return strip_arr

    def genRedToOrange(self,pot_val, length):
      print('entering genRedToOra')
      strip_arr = []
      if pot_val <= 0:
        pot_val = 1

      pot_val = (pot_val/2)
      print('pot_val from genRedToOrange', pot_val)
      green_val = round((pot_val*15), 0)
      print('green_val from genRedToOrange', green_val)

      rgb_color_arr = [ 255, green_val, 0 ]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr

    def genOrangeToYellow(self, pot_val, length):
      strip_arr = []

      if pot_val <= 0:
        pot_val = 1

      pot_val = (pot_val/2)
      green_val = round((150 + (pot_val * 10)), 0)
      
      rgb_color_arr = [255, green_val, 0]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr

    def genYellowToGreen(self, pot_val, length):
      strip_arr = []
      if pot_val <= 0:
        pot_val = 1

      pot_val = (pot_val/2)
      red_val = round((250 - (pot_val * 25)), 0)
      
      rgb_color_arr = [red_val, 250, 0]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr

    def genGreenToAqua(self, pot_val, length):
      strip_arr = []
      if pot_val <= 0:
        pot_val = 1
    
      pot_val = (pot_val/2)
      blue_val = round((25 * pot_val), 0)
      
      rgb_color_arr = [0, 255, blue_val]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr

    def genAquaToBlue(self, pot_val, length):
      strip_arr = []
      if pot_val <= 0:
        pot_val = 1

      pot_val = (pot_val/2)
      green_val = round((250 - (pot_val * 25)), 0)
      
      rgb_color_arr = [0, green_val, 255]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr

    def genBlueToPink(self, pot_val, length):
      strip_arr = []
      if pot_val <= 0:
        pot_val = 1
      
      pot_val = (pot_val/2)
      red_val = round((pot_val * 25), 0)

      rgb_color_arr = [red_val, 0, 255]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr

    def genPinkToRed(self, pot_val, length):
      strip_arr = []
      if pot_val <= 0:
        pot_val = 1
      
      pot_val = (pot_val/2)
      blue_val = round((250 - (pot_val * 25)), 0)
      
      rgb_color_arr = [255, 0, blue_val]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr
    
    def UpdateDmx(self):
        # Gets the potentiometer value, each time the loop is run.
        pot_val = MCP3008(0).value
        pot_val = int(pot_val* 100)
        print(pot_val)

        # Uses the potentiometer value to select different color gradients.
        if pot_val >= 0 and pot_val <= 20:
          if pot_val == 0:
            pot_val = 1
          
          self._universe_one_array = array('B', self.genRedToOrange(pot_val, 180))

        if pot_val >= 21 and pot_val <= 40:
          # Keep the pot_val between 1 and 20, for ez multiplication.
          pot_val = int(pot_val - 20)

          self._universe_one_array = array('B', self.genOrangeToYellow(pot_val, 180))

        if pot_val >= 41 and pot_val <= 60:
          # Keep the pot_val between 1 and 20, for ez multiplication.
          pot_val = pot_val - 40

          self._universe_one_array = array('B', self.genYellowToGreen(pot_val, 180))

        if pot_val >= 61 and pot_val <= 80:
          # Keep the pot_val between 1 and 20, for ez multiplication.
          pot_val = pot_val - 60

          self._universe_one_array = array('B', self.genGreenToAqua(pot_val, 180))

        if pot_val >= 81 and pot_val <= 100:
          # Keep the pot_val between 1 and 20, for ez multiplication.
          pot_val = pot_val - 80

          self._universe_one_array = array('B', self.genAquaToBlue(pot_val, 180) )

        self._iterable += 1

        # Send each array, a frame of animation, to each respective universe.
        self._client.SendDmx(1, self._universe_one_array)
        # self._client.SendDmx(2, self._universe_two_array)
        # self._client.SendDmx(3, self._universe_three_array)
        # self._client.SendDmx(4, self._universe_four_array)

        # Triggers the new update to be sent to the DMX controller.
        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)