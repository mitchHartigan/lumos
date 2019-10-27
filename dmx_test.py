from array import array
from ola.ClientWrapper import ClientWrapper
import random
import time

#should keep our update interval the same?

class SimpleFadeController(object):
    def __init__(self, update_interval, client_wrapper):
        self._update_interval = update_interval
        self._data = array('B', [])
        self._wrapper = client_wrapper
        self._client = client_wrapper.Client()
        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)
        self._iterable = 1

        self._strip_one_array = array('B', [])
        self._strip_two_array = array('B', [])
        self._strip_three_array = array('B', [])
        self._strip_four_array = array('B', [])

    def UpdateDmx(self):
        """
        This function gets called periodically based on UPDATE_INTERVAL
        """ 
        
        if(self._iterable >= 2):
            self._strip_one_array.extend([255, 0, 0])

        if(self._iterable >= 4):
            self._strip_two_array.extend([255, 0, 0])

        if(self._iterable >= 6):
            self._strip_three_array.extend([255, 0, 0])

        if(self._iterable >= 8):
            self._strip_four_array.extend([255, 0, 0])

        self._iterable += 1
        # Send the DMX data
        self._client.SendDmx(1, self._strip_one_array)
        self._client.SendDmx(2, self._strip_two_array)
        self._client.SendDmx(3, self._strip_three_array)
        self._client.SendDmx(4, self._strip_four_array)

        # For more information on Add Event, reference the OlaClient
        # Add our event again so it becomes periodic
        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)