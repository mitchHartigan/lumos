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

        # Initialize the unique array for each strip
        self._strip_one_array = array('B', [])
        self._strip_two_array = array('B', [])
        self._strip_three_array = array('B', [])
        self._strip_four_array = array('B', [])

        # Testing gradient
        # self._strip_test_gradient_math = array('B', [217,120,0,206,114,13,195,108,26,184,102,38,174,96,51,163,90,64,152,84,77,141,78,89,130,72,102,119,66,115,109,60,128,98,54,140,87,48,153,76,42,166,65,36,179,54,30,191,43,24,204,33,18,217,22,12,230,11,6,242,0,0,255])
        # self._strip_test_gradient_chosen_values = array('B',[217,120,0,200,114,13,195,108,26,170,89,26,160,84,41,149,78,54,138,72,67,126,66,80,115,60,93,104,50,106,90,48,119,82,42,132,71,36,145,60,30,158,49,24,171,38,18,184,27,12,197,16,6,210,5,0,223,0,0,255])

        # Initialize a data length for each strip.
        # These will update at different rates, as the strips remove
        # array elements at different rates.
        self._strip_one_data_length = 180
        self._strip_two_data_length = 180
        self._strip_three_data_length = 180
        self._strip_four_data_length = 180

        self._current_no_lights = 20

    def GenerateRGBValue(self, end_val, current_val, current_no_lights):
        step = (end_val - start_val) / current_no_lights
        new_val = current_val + step
        self._current_no_lights -= 1
        return new_val

    def UpdateDmx(self):
        """
        This function gets called periodically based on UPDATE_INTERVAL
        """ 

        #----------------------------------
        # Strip one controller
        #----------------------------------

        # 5 is the amount of time we want to wait before starting to update this array.
        # Ie, this code is called every 25ms (UPDATE_INTERVAL), and it waits for five
        # intervals before outputting the first elem to the array.
        if(self._iterable >= 5):
            if (self._iterable >= 65):
                # 60 is the number of pixels in the strip, and after 65 iterations (since we
                # waited 5 iterations to run the first one) we'll have reached the end of the
                # strip. (ie, we offset this val by 5 in this case.)

                i = self._strip_one_data_length - 1 # gets the index pos of the last array elem
            
                # deletes the last set of (3) rgb values from the array.
                x = 0
                while x < 3:
                    self._strip_one_array[i-x] = 0
                    x += 1

                
                self._strip_one_data_length -= 3 #updates the length of this strip to match the deletion.
            else:  
                # if not at 65 iterations, the strip isn't full yet, and therefore is still ascending.
                # Adds a pixel to the array if so.  
                # self._strip_one_array.extend([0, 0, 255])
                self._strip_one_array.extend([GenerateRGBValue(74, 142, self._current_no_lights), GenerateRGBValue(0, 45, self._current_no_lights), GenerateRGBValue(224, 226, self._current_no_lights)])
        
        #----------------------------------
        # Strip two controller
        #----------------------------------
        if(self._iterable >= 10):
            if (self._iterable >= 70): # checks if the strip has reached the end.
                i = self._strip_two_data_length - 1
                
                x = 0
                while x < 3:
                    self._strip_two_array[i-x] = 0
                    x += 1
                self._strip_two_data_length -= 3
            else:    
                self._strip_two_array.extend([255, 0, 0])            

        #----------------------------------
        # Strip three controller
        #----------------------------------
        if(self._iterable >= 15):
            if (self._iterable >= 75): # checks if the strip has reached the end. offset by 15 from 60
                i = self._strip_three_data_length - 1
                
                x = 0
                while x < 3:
                    self._strip_three_array[i-x] = 0
                    x += 1
                self._strip_three_data_length -= 3
            else:    
                self._strip_three_array.extend([0, 255, 0])

        #----------------------------------
        # Strip four controller
        #----------------------------------
        if(self._iterable >= 20):
            if (self._iterable >= 80):
                i = self._strip_four_data_length - 1
                
                x = 0
                while x < 3:
                    self._strip_four_array[i-x] = 0
                    x += 1
                self._strip_four_data_length -= 3
            else:    
                self._strip_four_array.extend([210, 10, 255])


        # updates the iterable at the end of this iteration. (lel tf did I just write)
        self._iterable += 1

        # Send each array, a frame of animation, to each respective universe.
        # self._client.SendDmx(1, self._strip_one_array)
        # self._client.SendDmx(2, self._strip_two_array)
        # self._client.SendDmx(3, self._strip_three_array)
        # self._client.SendDmx(4, self._strip_four_array)
        # self._client.SendDmx(1, self._strip_test_gradient_math)
        # self._client.SendDmx(2, self._strip_test_gradient_chosen_values)


        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)