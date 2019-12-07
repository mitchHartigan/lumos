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

    def fillStripWithColor(self, rgb_color_arr, length):
      i = 1
      strip_arr = []
      while i <= length:
        strip_arr.extend(rgb_color_arr)
        i += 1
      return strip_arr

    def genRedToOrange(self,pot_val, length):
      strip_arr = []

      pot_val = (pot_val/4)
      green_val = round((pot_val*15))
      green_val = int(green_val)

      rgb_color_arr = [ 255, green_val, 0 ]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr

    def genOrangeToYellow(self, pot_val, length):
      strip_arr = []

      pot_val = (pot_val/4)
      green_val = round( (150 + (pot_val * 10)) )
      green_val = int(green_val)
      
      rgb_color_arr = [255, green_val, 0]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr

    def genYellowToGreen(self, pot_val, length):
      strip_arr = []

      pot_val = (pot_val/4)
      red_val = round( (250 - (pot_val * 25)) ) 
      red_val = int(red_val)
      
      rgb_color_arr = [red_val, 250, 0]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr

    def genGreenToAqua(self, pot_val, length):
      strip_arr = []
    
      pot_val = (pot_val/4)
      blue_val = round((25 * pot_val))
      blue_val = int(blue_val)
      
      rgb_color_arr = [0, 255, blue_val]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr

    def genAquaToBlue(self, pot_val, length):
      strip_arr = []

      pot_val = (pot_val/4)
      green_val = round( (250 - (pot_val * 25)) )
      green_val = int(green_val)
      
      rgb_color_arr = [0, green_val, 255]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr

    def genBlueToPink(self, pot_val, length):
      strip_arr = []
      
      pot_val = (pot_val/4)
      red_val = round((pot_val * 25))
      red_val = int(red_val)

      rgb_color_arr = [red_val, 0, 255]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr

    def genPinkToRed(self, pot_val, length):
      strip_arr = []
      
      pot_val = (pot_val/4)
      blue_val = round( (250 - (pot_val * 25)) )
      blue_val = int(blue_val)
      
      rgb_color_arr = [255, 0, blue_val]

      strip_arr.extend(self.fillStripWithColor(rgb_color_arr, length))

      return strip_arr
    
    def UpdateDmx(self):
        # Gets the potentiometer value, each time the loop is run.
        pot_val = MCP3008(0).value
        pot_val = int(pot_val* 100)

        # Uses the potentiometer value to select different color gradients.
        if pot_val >= 0 and pot_val <= 40:

          self._universe_one_array = array('B', self.genGreenToAqua(pot_val, 180))
          self._universe_two_array = array('B', self.genPinkToRed(pot_val, 60))
          self._universe_three_array = array('B', self.genBlueToPink(pot_val, 180))
          self._universe_four_array = array('B', self.genYellowToGreen(pot_val, 180))
          print(self._universe_four_array)
          print('Length of universe 4: ', len(self._universe_four_array))

        if pot_val >= 41 and pot_val <= 80:
          # Keep the pot_val between 1 and 20, for ez multiplication.
          pot_val = int(pot_val - 40)

          self._universe_one_array = array('B', self.genAquaToBlue(pot_val, 180))
          self._universe_two_array = array('B', self.genRedToOrange(pot_val, 60))
          self._universe_three_array = array('B', self.genPinkToRed(pot_val, 180))
          self._universe_four_array = array('B', self.genGreenToAqua(pot_val, 180))
          print(self._universe_four_array)
          print('Length of universe 4: ', len(self._universe_four_array))

        if pot_val >= 81 and pot_val <= 100:
          # Keep the pot_val between 1 and 20, for ez multiplication.
          pot_val = pot_val - 80

          self._universe_one_array = array('B', self.genBlueToPink(pot_val, 180) )
          self._universe_two_array = array('B', self.genOrangeToYellow(pot_val, 60))
          self._universe_three_array = array('B', self.genRedToOrange(pot_val, 180))
          self._universe_four_array = array('B', self.genAquaToBlue(pot_val, 180))
          print(self._universe_four_array)
          print('Length of universe 4: ', len(self._universe_four_array))

        # Send each array, a frame of animation, to each respective universe.
        self._client.SendDmx(1, self._universe_one_array)
        self._client.SendDmx(2, self._universe_two_array)
        self._client.SendDmx(3, self._universe_three_array)
        self._client.SendDmx(4, self._universe_four_array)

        # Triggers the new update to be sent to the DMX controller.
        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)