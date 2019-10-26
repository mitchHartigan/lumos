from array import array
from ola.ClientWrapper import ClientWrapper
from ola.DMXConstants import DMX_MIN_SLOT_VALUE, DMX_MAX_SLOT_VALUE, \
    DMX_UNIVERSE_SIZE
import random

UPDATE_INTERVAL = 100 # In ms, this comes about to ~40 frames a second
SHUTDOWN_INTERVAL = 12000 # in ms, This is 10 seconds
DMX_DATA_SIZE = 60
UNIVERSE = 1
movingUpwards = True

class SimpleFadeController(object):
    def __init__(self, universe, update_interval, client_wrapper,
               dmx_data_size=DMX_UNIVERSE_SIZE):
        dmx_data_size = min(dmx_data_size, DMX_UNIVERSE_SIZE)
        self._universe = universe
        self._update_interval = update_interval
        self._data = array('B', [])
        self._wrapper = client_wrapper
        self._client = client_wrapper.Client()
        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)
        self._iterable = 0
        self._ascending = True
        self._index = 0
        self._data_length = 120

    def UpdateDmx(self):
        """
        This function gets called periodically based on UPDATE_INTERVAL
        """

        if self._ascending:
            self._data.extend([255, 0, 0])
        else: 
            i = self._data_length - 1
            
            x = 0
            while x < 3:
                self._data[i-x] = 0
                x += 1
            
            self._data_length -= 3
            
        if self._iterable > 60:
            self._ascending = False

        self._iterable += 1

        print(self._data)
        # Send the DMX data
        self._client.SendDmx(self._universe, self._data)
        # For more information on Add Event, reference the OlaClient
        # Add our event again so it becomes periodic
        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)


if __name__ == '__main__':
        wrapper = ClientWrapper()
        controller = SimpleFadeController(UNIVERSE, UPDATE_INTERVAL, wrapper,
                                        DMX_DATA_SIZE)
        # Call it initially
        wrapper.AddEvent(SHUTDOWN_INTERVAL, wrapper.Stop)
        # Start the wrapper
        wrapper.Run()