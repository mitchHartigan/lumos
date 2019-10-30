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

        # Initialize a data length for each strip.
        # These will update at different rates, as the strips remove
        # array elements at different rates.
        self._strip_one_data_length = 180
        self._strip_two_data_length = 180
        self._strip_three_data_length = 180
        self._strip_four_data_length = 180

        # self.gradient1 = self.generate_multicolor_gradient(142, 45, 226, 74, 0, 224, 255, 0, 153)

        self.gradient1 = [ 
                        [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], 
                        [255, 43, 0], [255, 43, 0], [255, 43, 0], [255, 43, 0], [255, 43, 0], 
                        [255, 85, 0], [255, 85, 0], [255, 85, 0], [255, 85, 0], [255, 85, 0], 
                        [255, 128, 0], [255, 128, 0], [255, 128, 0], [255, 128, 0], [255, 128, 0],
                        [255, 170, 0], [255, 170, 0], [255, 170, 0], [255, 170, 0], [255, 170, 0],
                        [255, 213, 0], [255, 213, 0], [255, 213, 0], [255, 213, 0], [255, 213, 0],
                        [255, 255, 0], [255, 255, 0], [255, 255, 0], [255, 255, 0], [255, 255, 0],
                        [213, 255, 0], [213, 255, 0], [213, 255, 0], [213, 255, 0], [213, 255, 0],
                        [170, 255, 0], [170, 255, 0], [170, 255, 0], [170, 255, 0], [170, 255, 0],
                        [128, 255, 0], [128, 255, 0], [128, 255, 0], [128, 255, 0], [128, 255, 0],
                        [85, 255, 0], [85, 255, 0], [85, 255, 0], [85, 255, 0], [85, 255, 0],
                        [43, 255, 0], [43, 255, 0], [43, 255, 0], [43, 255, 0], [43, 255, 0],
                        [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [204, 0, 204 ]
                         ] 

        self.gradient2 = [
                        [130, 0, 144], [130, 0, 144], [130, 0, 144], [130, 0, 144], [130, 0, 144], 
                        [202, 0, 144], [202, 0, 144], [202, 0, 144], [202, 0, 144], [202, 0, 144], 
                        [246, 0, 103], [246, 0, 103], [246, 0, 103], [246, 0, 103], [246, 0, 103],
                        [255, 0, 79], [255, 0, 79], [255, 0, 79], [255, 0, 79], [255, 0, 79], 
                        [255, 0, 51], [255, 0, 51], [255, 0, 51], [255, 0, 51], [255, 0, 51], 
                        [255, 0, 17], [255, 0, 17], [255, 0, 17], [255, 0, 17], [255, 0, 17], 
                        [255, 95, 0], [255, 95, 0], [255, 95, 0], [255, 95, 0], [255, 95, 0], 
                        [243, 96, 0], [243, 96, 0], [243, 96, 0], [243, 96, 0], [243, 96, 0], 
                        [255, 135, 0], [255, 135, 0], [255, 135, 0], [255, 135, 0], [255, 135, 0], 
                        [255, 154, 0], [255, 154, 0], [255, 154, 0], [255, 154, 0], [255, 154, 0], 
                        [255, 195, 0], [255, 195, 0], [255, 195, 0], [255, 195, 0], [255, 195, 0], 
                        [255, 197, 2], [255, 197, 2], [255, 197, 2], [255, 197, 2], [255, 197, 2]
                        ]

    def read_values(self, offset, gradient_list):
        """
        Reads the each color value out of the pre-generated arrays, returning them as a list.
        """
        # We're off by one somewhere. I don't like this, but I can't find where it is.
        
        # The current RGB value array, selected from our array of arrays. We subtract the offset to account for the iterations we've
        # spent waiting for this specific strip.
        current_rgb_set = (self._iterable - offset)
        
        vals = []

        i = 0
        while i < 3: 
            vals.append(gradient_list[current_rgb_set][i])
            i += 1

        print(vals)
        return vals

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
        strip_one_offset = 5
        if(self._iterable >= strip_one_offset):
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

                new_value = self.read_values(strip_one_offset, self.gradient1)

                self._strip_one_array.extend(new_value)
        #----------------------------------
        # Strip two controller
        #----------------------------------
        strip_two_offset = 10
        if(self._iterable >= strip_two_offset):
            if (self._iterable >= 70): # checks if the strip has reached the end.
                i = self._strip_two_data_length - 1
                
                x = 0
                while x < 3:
                    self._strip_two_array[i-x] = 0
                    x += 1
                self._strip_two_data_length -= 3
            else:    
                new_value = self.read_values(strip_two_offset, self.gradient2)

                self._strip_two_array.extend(new_value)         

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
        self._client.SendDmx(1, self._strip_one_array)
        self._client.SendDmx(2, self._strip_two_array)
        self._client.SendDmx(3, self._strip_three_array)
        self._client.SendDmx(4, self._strip_four_array)

        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)