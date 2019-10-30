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
                        [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], 
                        [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], 
                        [255, 43, 0], [255, 43, 0], [255, 43, 0], [255, 43, 0], [255, 43, 0], 
                        [255, 43, 0], [255, 43, 0], [255, 43, 0], [255, 43, 0], [255, 43, 0], 
                        [255, 85, 0], [255, 85, 0], [255, 85, 0], [255, 85, 0], [255, 85, 0], 
                        [255, 128, 0], [255, 128, 0], [255, 128, 0], [255, 128, 0], [255, 128, 0],
                        [255, 170, 0], [255, 170, 0], [255, 170, 0], [255, 170, 0], [255, 170, 0],
                        [255, 213, 0], [255, 213, 0], [255, 213, 0], [255, 213, 0], [255, 213, 0],
                        [255, 255, 0], [255, 255, 0], [255, 255, 0], [255, 255, 0], [255, 255, 0],
                        # [213, 255, 0], [213, 255, 0], [213, 255, 0], [213, 255, 0], [213, 255, 0],
                        [170, 255, 0], [170, 255, 0], [170, 255, 0], [170, 255, 0], [170, 255, 0],
                        # [128, 255, 0], [128, 255, 0], [128, 255, 0], [128, 255, 0], [128, 255, 0],
                        # [85, 255, 0], [85, 255, 0], [85, 255, 0], [85, 255, 0], [85, 255, 0],
                        [43, 255, 0], [43, 255, 0], [43, 255, 0], [43, 255, 0], [43, 255, 0],
                        [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [204, 0, 204 ]
                         ] 

        self.gradient2 = [
                        [130, 0, 144], [130, 0, 144], [130, 0, 144], [130, 0, 144], [130, 0, 144], 
                        [202, 0, 144], [202, 0, 144], [202, 0, 144], [202, 0, 144], [202, 0, 144], 
                        [246, 0, 103], [246, 0, 103], [246, 0, 103], [246, 0, 103], [246, 0, 103],
                        [255, 0, 79], [255, 0, 79], [255, 0, 79], [255, 0, 79], [255, 0, 79], 
                        [255, 0, 51], [255, 0, 51], [255, 0, 51], [255, 0, 51], [255, 0, 51], 
                        [255, 44, 42], [255, 44, 42], [255, 44, 42], [255, 44, 42], [255, 44, 42], 
                        # [255, 0, 17], [255, 0, 17], [255, 0, 17], [255, 0, 17], [255, 0, 17], 
                        [255, 95, 0], [255, 95, 0], [255, 95, 0], [255, 95, 0], [255, 95, 0], 
                        [243, 96, 0], [243, 96, 0], [243, 96, 0], [243, 96, 0], [243, 96, 0], 
                        [255, 135, 0], [255, 135, 0], [255, 135, 0], [255, 135, 0], [255, 135, 0], 
                        [255, 154, 0], [255, 154, 0], [255, 154, 0], [255, 154, 0], [255, 154, 0], 
                        [255, 195, 0], [255, 195, 0], [255, 195, 0], [255, 195, 0], [255, 195, 0], 
                        [255, 197, 2], [255, 197, 2], [255, 197, 2], [255, 197, 2], [255, 197, 2]
                        ]

        # self.gradient3 = [
        #                 [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], 
        #                 [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], 
        #                 [29, 5, 231], [29, 5, 231], [29, 5, 231], [29, 5, 231], [29, 5, 231], 
        #                 [42, 7, 220], [42, 7, 220], [42, 7, 220], [42, 7, 220], [42, 7, 220], 
        #                 [96, 16, 197], [96, 16, 197], [96, 16, 197], [96, 16, 197], [96, 16, 197], 
        #                 [146, 25, 133], [146, 25, 133], [146, 25, 133], [146, 25, 133], [146, 25, 133], 
        #                 [184, 32, 101], [184, 32, 101], [184, 32, 101], [184, 32, 101], [184, 32, 101], 
        #                 [216, 37, 74], [216, 37, 74], [216, 37, 74], [216, 37, 74], [216, 37, 74], 
        #                 [255, 35, 34], [255, 35, 34], [255, 35, 34], [255, 35, 34], [255, 35, 34], 
        #                 [246, 0, 103], [246, 0, 103], [246, 0, 103], [246, 0, 103], [246, 0, 103],
        #                 [246, 0, 103], [246, 0, 103], [246, 0, 103], [246, 0, 103], [246, 0, 103],
        #                 [246, 0, 103], [246, 0, 103], [246, 0, 103], [246, 0, 103], [246, 0, 103]
        #                 ]

        self.gradient3 = [
                        [17, 189, 0], [16, 187, 8], [16, 186, 16], [16, 185, 24], [16, 184, 32], 
                        [15, 183, 41], [15, 181, 49], [15, 180, 57], [15, 179, 65], [15, 178, 74], 
                        [14, 177, 82], [14, 176, 90], [14, 174, 98], [14, 173, 107], [14, 172, 115], 
                        [13, 171, 123], [13, 170, 131], [13, 169, 140], [13, 167, 148], [13, 166, 156], 
                        [12, 165, 164], [12, 164, 173], [12, 163, 181], [12, 162, 189], [12, 160, 197], 
                        [11, 159, 206], [11, 158, 214], [11, 157, 222], [11, 156, 230], [11, 155, 239], 
                        [11, 155, 239], [18, 150, 239], [26, 145, 239], [34, 140, 239], [42, 135, 239], 
                        [50, 130, 240], [54, 124, 236], [58, 119, 232], [62, 114, 229], [66, 109, 225], 
                        [70, 103, 222], [75, 98, 218], [79, 93, 214], [83, 88, 211], [87, 82, 207], 
                        [91, 77, 204], [95, 72, 200], [100, 67, 197], [104, 61, 193], [108, 56, 189],
                        [112, 51, 186], [116, 46, 182], [120, 40, 179], [125, 35, 175], [129, 30, 171],
                        [133, 25, 168], [137, 19, 164], [141, 14, 161], [145, 9, 157], [150, 4, 154]
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
        strip_three_offset = 15
        if(self._iterable >= strip_three_offset):
            if (self._iterable >= 75): # checks if the strip has reached the end. offset by 15 from 60
                i = self._strip_three_data_length - 1
                
                x = 0
                while x < 3:
                    self._strip_three_array[i-x] = 0
                    x += 1
                self._strip_three_data_length -= 3
            else:    
                new_value = self.read_values(strip_three_offset, self.gradient3)

                self._strip_three_array.extend(new_value)   

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