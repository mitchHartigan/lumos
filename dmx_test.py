from array import array
from ola.ClientWrapper import ClientWrapper
from ola.DMXConstants import DMX_MIN_SLOT_VALUE, DMX_MAX_SLOT_VALUE, \
    DMX_UNIVERSE_SIZE
import random

UPDATE_INTERVAL = 100 # In ms, this comes about to ~40 frames a second
SHUTDOWN_INTERVAL = 10000 # in ms, This is 10 seconds
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

  def UpdateDmx(self):
    """
    This function gets called periodically based on UPDATE_INTERVAL
    """
    """
    if self._iterable < 120:
     self._data.extend([0, 0, self._iterable])
     self._iterable += 10
    elif self._iterable >= 120 and self._iterable < 240: 
      self._data.extend([self._iterable, 0, 0])
      self._iterable += 10
    elif self._iterable == 240: 
      self._iterable = 10
    print(self._iterable)
    """
    
    while self._iterable <= SHUTDOWN_INTERVAL/2:
        movingUpwards = False
    if movingUpwards:
        self._data.extend([75, 249, 145, 239, 180, 63, 247, 121, 125])
    else:
        i = 0
        while i < 3:
            self._data.pop()
            i+= 1
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
