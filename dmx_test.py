from array import array
from ola.ClientWrapper import ClientWrapper
import random
import time

class SimpleFadeController(object):
    def __init__(self, universe, update_interval, client_wrapper, time_offset):
        self._universe = universe
        self._update_interval = update_interval
        self._data = array('B', [])
        self._wrapper = client_wrapper
        self._client = client_wrapper.Client()
        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)
        self._iterable = 1
        self._ascending = True
        self._data_length = 180
        self._time_offset = time_offset
        self._is_first_update = True

    def UpdateDmx(self):
        """
        This function gets called periodically based on UPDATE_INTERVAL
        """

        if self._is_first_update:
            time.sleep(self._time_offset)
            self._is_first_update = False

        if self._ascending:
            self._data.extend([255, 0, 0])
            print('added 3 values to array')
        else: 
            i = self._data_length - 1
            
            x = 0
            while x < 3:
                self._data[i-x] = 0
                x += 1            
            self._data_length -= 3
        
            print('deleted 3 values from array')

        print(self._data_length)

        # Checks if the led strip is full (ie, it has 60 pixel values)    
        if self._iterable == 60:
            self._ascending = False
            print('ascending set false!')

        self._iterable += 1

        print(self._data)
        # Send the DMX data
        self._client.SendDmx(self._universe, self._data)
        # For more information on Add Event, reference the OlaClient
        # Add our event again so it becomes periodic
        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)