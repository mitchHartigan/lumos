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

        # working atm need to fix 
        # self.gradient1 = [ 
        #                 [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], 
        #                 [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], 
        #                 [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], 
        #                 [255, 43, 0], [255, 43, 0], [255, 43, 0], [255, 43, 0], [255, 43, 0], 
        #                 [255, 43, 0], [255, 43, 0], [255, 43, 0], [255, 43, 0], [255, 43, 0], 
        #                 [255, 85, 0], [255, 85, 0], [255, 85, 0], [255, 85, 0], [255, 85, 0], 
        #                 [255, 128, 0], [255, 128, 0], [255, 128, 0], [255, 128, 0], [255, 128, 0],
        #                 [255, 170, 0], [255, 170, 0], [255, 170, 0], [255, 170, 0], [255, 170, 0],
        #                 [255, 213, 0], [255, 213, 0], [255, 213, 0], [255, 213, 0], [255, 213, 0],
        #                 [255, 255, 0], [255, 255, 0], [255, 255, 0], [255, 255, 0], [255, 255, 0],
        #                 # [213, 255, 0], [213, 255, 0], [213, 255, 0], [213, 255, 0], [213, 255, 0],
        #                 [170, 255, 0], [170, 255, 0], [170, 255, 0], [170, 255, 0], [170, 255, 0],
        #                 # [128, 255, 0], [128, 255, 0], [128, 255, 0], [128, 255, 0], [128, 255, 0],
        #                 # [85, 255, 0], [85, 255, 0], [85, 255, 0], [85, 255, 0], [85, 255, 0],
        #                 [43, 255, 0], [43, 255, 0], [43, 255, 0], [43, 255, 0], [43, 255, 0],
        #                 [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [204, 0, 204 ]
        #                  ] 

        # redish purple > orange > yellowish green
        self.gradient1 = [ 
                        [255, 0, 128], [255, 4, 123], [255, 9, 119], [255, 14, 114], [255, 19, 110], 
                        [255, 24, 105], [255, 28, 101], [255, 33, 97], [255, 38, 92], [255, 43, 88], 
                        [255, 48, 83], [255, 53, 79], [255, 57, 75], [255, 62, 70], [255, 67, 66], 
                        [255, 72, 61], [255, 77, 57], [255, 82, 52], [255, 86, 48], [255, 91, 44], 
                        [255, 96, 39], [255, 101, 35], [255, 106, 30], [255, 111, 26], [255, 115, 22], 
                        [255, 120, 17], [255, 125, 13], [255, 130, 8], [255, 135, 4], [255, 140, 0],
                        [255, 142, 0], [252, 145, 0], [250, 148, 0], [255, 150, 0], [245, 152, 0],              
                        [242, 153, 0], [240, 156, 0], [238, 159, 0], [235, 161, 0], [233, 164, 0],
                        [230, 167, 0], [228, 169, 0], [226, 172, 0], [223, 175, 0], [221, 178, 0],
                        [218, 180, 0], [216, 183, 0], [213, 186, 0], [221, 189, 0], [209, 191, 0],
                        [206, 194, 0], [204, 197, 0], [201, 199, 0], [199, 202, 0], [197, 205, 0],
                        [194, 208, 0], [192, 210, 0], [189, 213, 0], [187, 216, 0], [185, 219, 0 ]
                         ] 

        #fixed not tested dark purple > redish orange > yellow
        self.gradient2 = [
                        [130, 0, 144], [134, 1, 140], [138, 2, 137], [142, 4, 133], [146, 5, 130], 
                        [150, 7, 127], [155, 8, 123], [159, 10, 120], [163, 11, 116], [167, 13, 113], 
                        [171, 14, 110], [175, 16, 106], [180, 17, 103], [184, 19, 99], [188, 20, 96],
                        [192, 22, 93], [196, 23, 89], [200, 24, 86], [205, 26, 82], [209, 27, 79], 
                        [213, 29, 76], [217, 30, 72], [221, 32, 69], [225, 33, 65], [230, 35, 62], 
                        [234, 36, 59], [238, 38, 55], [242, 39, 52], [246, 41, 48], [250, 42, 45], 
                        [255, 44, 42], [255, 49, 40], [255, 54, 39], [255, 59, 37], [255, 65, 36], 
                        [255, 70, 35], [255, 75, 33], [255, 80, 32], [255, 86, 30], [255, 91, 29], 
                        [255, 96, 28], [255, 102, 26], [255, 107, 25], [255, 112, 24], [255, 117, 22], 
                        [255, 123, 21], [255, 128, 19], [255, 133, 18], [255, 138, 17], [255, 144, 15], 
                        [255, 149, 14], [255, 154, 13], [255, 160, 11], [255, 165, 10], [255, 170, 8], 
                        [255, 175, 7], [255, 181, 6], [255, 186, 4], [255, 191, 3], [255, 197, 2]
                        ]
        #working atm
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

        # Green > Blue > light / purple
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
                        [133, 25, 150], [110, 19, 130], [110, 8, 110], [80, 4, 80], [70, 4, 70]
                        ]

        self.gradient_array = [self.gradient1, self.gradient2, self.gradient3]

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