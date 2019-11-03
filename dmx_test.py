from array import array
from ola.ClientWrapper import ClientWrapper
from gpiozero import MCP3008
from time import sleep
import random
import time

class SimpleFadeController(object):
    def __init__(self, update_interval, client_wrapper):
        self._update_interval = update_interval
        self._data = array('B', [])
        self._wrapper = client_wrapper
        self._client = client_wrapper.Client()
        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)
        self._iterable = 1

        # Initialize the unique array for each strip
        self._universe_one_array = array('B', [])
        self._universe_two_array = array('B', [])
        self._universe_three_array = array('B', [])
        self._universe_four_array = array('B', [])

        # Initialize a data length for each strip.
        # These will update at different rates, as the strips remove
        # array elements at different rates.

        self._universe_one_data_length = 360
        self._universe_two_data_length = 180
        self._universe_three_data_length = 180
        self._universe_four_data_length = 360

        # red > orange > green
        # self.gradient1 = [
        #                 [255, 0, 0], [255, 5, 0], [255, 10, 0], [255, 15, 0], [255, 20, 0],
        #                 [255, 26, 0], [255, 31, 1], [255, 36, 1], [255, 41, 1], [255, 46, 1],
        #                 [255, 51, 1], [255, 57, 1], [255, 62, 1], [255, 67, 2], [255, 72, 2],
        #                 [255, 77, 2], [255, 82, 2], [255, 87, 2], [255, 93, 3], [255, 98, 3], 
        #                 [255, 103, 3], [255, 108, 3], [255, 113, 3], [255, 118, 3], [255, 123, 4],
        #                 [255, 128, 4], [255, 133, 4], [255, 138, 4], [255, 143, 4], [255, 148, 4],
        #                 [255, 153, 5], [251, 164, 5], [248, 173, 5], [245, 183, 5], [242, 192, 5], 
        #                 [238, 201, 5], [235, 209, 6], [232, 217, 6], [229, 225, 6], [218, 225, 6], 
        #                 [205, 222, 6], [192, 219, 6], [179, 216, 6], [166, 212, 7], [154, 209, 7], 
        #                 [142, 206, 7], [130, 203, 7], [119, 199, 7], [108, 196, 7], [97, 193, 7], 
        #                 [87, 190, 7], [77, 186, 7], [63, 183, 7], [57, 180, 7], [48, 177, 7], 
        #                 [40, 173, 7], [23, 167, 7], [31, 170, 7], [15, 164, 7], [7, 160, 8],
        #                  ]

        # # redish purple > orange > yellowish green
        # self.gradient2 = [ 
        #                 [255, 0, 128], [255, 4, 123], [255, 9, 119], [255, 14, 114], [255, 19, 110], 
        #                 [255, 24, 105], [255, 28, 101], [255, 33, 97], [255, 38, 92], [255, 43, 88], 
        #                 [255, 48, 83], [255, 53, 79], [255, 57, 75], [255, 62, 70], [255, 67, 66], 
        #                 [255, 72, 61], [255, 77, 57], [255, 82, 52], [255, 86, 48], [255, 91, 44], 
        #                 [255, 96, 39], [255, 101, 35], [255, 106, 30], [255, 111, 26], [255, 115, 22], 
        #                 [255, 120, 17], [255, 125, 13], [255, 130, 8], [255, 135, 4], [255, 140, 0],
        #                 [255, 142, 0], [252, 145, 0], [250, 148, 0], [255, 150, 0], [245, 152, 0],              
        #                 [242, 153, 0], [240, 156, 0], [238, 159, 0], [235, 161, 0], [233, 164, 0],
        #                 [230, 167, 0], [228, 169, 0], [226, 172, 0], [223, 175, 0], [221, 178, 0],
        #                 [218, 180, 0], [216, 183, 0], [213, 186, 0], [221, 189, 0], [209, 191, 0],
        #                 [206, 194, 0], [204, 197, 0], [201, 199, 0], [199, 202, 0], [197, 205, 0],
        #                 [194, 208, 0], [192, 210, 0], [189, 213, 0], [187, 216, 0], [185, 219, 0]
        #                  ] 

        # # fixed not tested dark purple > redish orange > yellow
        # self.gradient3 = [
        #                 [130, 0, 144], [134, 1, 140], [138, 2, 137], [142, 4, 133], [146, 5, 130], 
        #                 [150, 7, 127], [155, 8, 123], [159, 10, 120], [163, 11, 116], [167, 13, 113], 
        #                 [171, 14, 110], [175, 16, 106], [180, 17, 103], [184, 19, 99], [188, 20, 96],
        #                 [192, 22, 93], [196, 23, 89], [200, 24, 86], [205, 26, 82], [209, 27, 79], 
        #                 [213, 29, 76], [217, 30, 72], [221, 32, 69], [225, 33, 65], [230, 35, 62], 
        #                 [234, 36, 59], [238, 38, 55], [242, 39, 52], [246, 41, 48], [250, 42, 45], 
        #                 [255, 44, 42], [255, 49, 40], [255, 54, 39], [255, 59, 37], [255, 65, 36], 
        #                 [255, 70, 35], [255, 75, 33], [255, 80, 32], [255, 86, 30], [255, 91, 29], 
        #                 [255, 96, 28], [255, 102, 26], [255, 107, 25], [255, 112, 24], [255, 117, 22], 
        #                 [255, 123, 21], [255, 128, 19], [255, 133, 18], [255, 138, 17], [255, 144, 15], 
        #                 [255, 149, 14], [255, 154, 13], [255, 160, 11], [255, 165, 10], [255, 170, 8], 
        #                 [255, 175, 7], [255, 181, 6], [255, 186, 4], [255, 191, 3], [255, 197, 2],
        #                  ]

        # # green > blue > light blue/ purple
        # self.gradient4 = [
        #                 [17, 189, 0], [16, 187, 8], [16, 186, 16], [16, 185, 24], [16, 184, 32], 
        #                 [15, 183, 41], [15, 181, 49], [15, 180, 57], [15, 179, 65], [15, 178, 74], 
        #                 [14, 177, 82], [14, 176, 90], [14, 174, 98], [14, 173, 107], [14, 172, 115], 
        #                 [13, 171, 123], [13, 170, 131], [13, 169, 140], [13, 167, 148], [13, 166, 156], 
        #                 [12, 165, 164], [12, 164, 173], [12, 163, 181], [12, 162, 189], [12, 160, 197], 
        #                 [11, 159, 206], [11, 158, 214], [11, 157, 222], [11, 156, 230], [11, 155, 239], 
        #                 [11, 155, 239], [18, 150, 239], [26, 145, 239], [34, 140, 239], [42, 135, 239], 
        #                 [50, 130, 240], [54, 124, 236], [58, 119, 232], [62, 114, 229], [66, 109, 225], 
        #                 [70, 103, 222], [75, 98, 218], [79, 93, 214], [83, 88, 211], [87, 82, 207], 
        #                 [91, 77, 204], [95, 72, 200], [100, 67, 197], [104, 61, 193], [108, 56, 189],
        #                 [112, 51, 186], [116, 46, 182], [120, 40, 179], [125, 35, 175], [129, 30, 171],
        #                 [133, 25, 150], [110, 19, 130], [110, 8, 110], [80, 4, 80], [70, 4, 70],
        #                  ]

        # # red > orange > purple
        # self.gradient5 = [ 
        #                 [255, 0, 0], [255, 4, 0], [255, 9, 0], [255, 14, 0], [255, 18, 0], 
        #                 [255, 23, 0], [255, 28, 0], [255, 32, 0], [255, 37, 0], [255, 42, 0], 
        #                 [255, 46, 0], [255, 51, 0], [255, 56, 0], [255, 60, 0], [255, 65, 0], 
        #                 [255, 70, 0], [255, 74, 0], [255, 79, 0], [255, 84, 0], [255, 88, 0], 
        #                 [255, 93, 0], [255, 98, 0], [255, 102, 0], [255, 107, 0], [255, 112, 0], 
        #                 [255, 116, 0], [255, 121, 0], [255, 126, 0], [255, 130, 0], [255, 135, 0], 
        #                 [255, 140, 0], [253, 135, 7], [251, 130, 14], [249, 125, 21], [247, 120, 29],
        #                 [245, 115, 36], [244, 110, 43], [242, 105, 51], [240, 100, 58], [238, 95, 65],
        #                 [236, 90, 72], [234, 85, 80], [233, 80, 87], [231, 75, 94], [229, 70, 102],
        #                 [227, 65, 109], [225, 60, 116], [224, 55, 123], [222, 50, 131], [220, 45, 138],
        #                 [218, 40, 145], [216, 35, 135], [214, 30, 160], [213, 25, 167], [211, 20, 174],
        #                 [209, 15, 182], [207, 10, 189], [205, 5, 196], [204, 0, 204], [200, 0, 200],
        #                  ]
        self.gradient1 = [
                            [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
                            [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
                            [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
                            [255, 0, 0], [255, 0, 5], [255, 0, 5], [255, 0, 10], [255, 0, 15],
                            [255, 0, 20], [255, 0, 25], [255, 0, 30], [255, 0, 40], [255, 0, 40],
                            [255, 0, 40], [255, 0, 40],[255, 0, 40],[255, 0, 40],[255, 0, 40],
                            [255, 0, 120], [255, 0, 120], [255, 0, 120], [255, 0, 120], [255, 0, 120],
                            [255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 0, 255],
                            [100, 0, 255], [100, 0, 255], [90, 0, 255], [90, 0, 255],[90, 0, 255],
                            [70, 0, 255], [60, 0, 255], [50, 0, 255], [50, 0, 255], [50, 0, 255],
                            [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255],
                            [0, 0, 255], [0, 0, 255],[0, 0, 255], [0, 0, 255], [0, 0, 255],
                         ]

        self.gradient2 = [
                            [255, 255, 0], [255, 255, 0], [255, 255, 0], [255, 255, 0], [255, 255, 0],
                            [255, 255, 0], [255, 255, 0], [255, 255, 0], [255, 255, 0], [255, 255, 0],
                            [255, 255, 0], [255, 255, 0], [255, 255, 0], [255, 255, 0], [255, 255, 0],
                            [200, 255, 0], [200, 255, 0], [200, 255, 0], [200, 255, 0], [200, 255, 0],
                            [180, 255, 0], [190, 200, 0], [200, 180, 10], [220, 150, 15], [220, 100, 20],
                            [237, 38, 36], [237, 38, 36], [237, 38, 36], [237, 28, 36], [237, 28, 36], 
                            [237, 38, 36], [237, 28, 10], [237, 28, 20], [237, 28, 10], [237, 28, 0], 
                            [200, 60, 0], [180, 80, 0], [160, 100, 0], [140, 120, 0], [80, 160, 0],
                            [0, 180, 0], [0, 200, 0], [0, 230, 0], [0, 255, 0], [0, 255, 0],
                            [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                            [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                            [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0],
                         ]
        
        self.gradient3 = [
                            [100, 0, 255], [100, 0, 255],[100, 0, 255],[100, 0, 255], [100, 0, 255],
                            [100, 0, 255], [100, 0, 255],[100, 0, 255],[100, 0, 255], [100, 0, 255],
                            [100, 0, 255], [100, 0, 255],[100, 0, 255],[100, 0, 255], [100, 0, 255],
                            [100, 0, 255], [100, 0, 255],[100, 0, 255],[100, 0, 255], [100, 0, 255],
                            [100, 0, 255], [100, 0, 255],[100, 0, 255],[100, 0, 255], [100, 0, 255],
                            [100, 0, 255], [100, 0, 255],[100, 0, 255],[100, 0, 255], [100, 0, 255],
                            [100, 0, 255], [100, 0, 255],[100, 0, 255],[100, 0, 255], [100, 0, 255],
                            [100, 0, 255], [100, 0, 255],[100, 0, 255],[100, 0, 255], [100, 0, 255],
                            [100, 0, 255], [100, 0, 255],[100, 0, 255],[100, 0, 255], [100, 0, 255],
                            [100, 0, 255], [100, 0, 255],[100, 0, 255],[100, 0, 255], [100, 0, 255],
                            [100, 0, 255], [100, 0, 255],[100, 0, 255],[100, 0, 255], [100, 0, 255],
                            [100, 0, 255], [100, 0, 255],[100, 0, 255],[100, 0, 255], [100, 0, 255],
                         ]
        
        self.gradient4 = [
                        [91, 255, 51], [88, 253, 65], [85, 251, 80], [82, 249, 94], [79, 247, 109],
                        [76, 246, 123], [73, 244, 136], [71, 242, 153], [68, 240, 167], [65, 238, 182],
                        [62, 237, 196], [59, 235, 211], [56, 233, 225], [53, 231, 240], [51, 230, 255],
                        [51, 218, 255], [51, 207, 255], [40, 180, 255], [30, 160, 255], [20, 140, 255], 
                        [10, 120, 255], [0, 100, 255], [0, 80, 255], [0, 60, 255], [0, 40, 255],
                        [51, 106, 255], [51, 95, 255], [51, 84, 255], [51, 73, 255], [61, 71, 255],
                        [72, 69, 255], [83, 68, 255], [94, 66, 255], [105, 65, 255], [116, 63, 255], 
                        [127, 62, 255], [138, 60, 255], [149, 58, 255], [160, 57, 255], [171, 55, 255], 
                        [182, 54, 255], [193, 52, 255], [204, 51, 255], [207, 48, 238], [210, 46, 221], 
                        [214, 44, 205], [217, 41, 188], [220, 39, 172], [224, 37, 155], [227, 34, 138], 
                        [230, 32, 122], [234, 30, 105], [237, 27, 89], [240, 25, 72], [244, 23, 55], 
                        [247, 20, 39], [250, 18, 22], [254, 16, 5], [255, 10, 0], [255, 0, 0],
                         ]

        self.gradient5 = [
                        [64, 224, 241], [64, 224, 241], [64, 224, 221], [64, 224, 221], [64, 224, 221],
                        [64, 224, 221], [64, 224, 221], [64, 224, 221], [64, 224, 221], [64, 224, 221],
                        [64, 224, 180], [64, 224, 150], [64, 224, 130], [64, 224, 100], [64, 224, 100],
                        [64, 224, 100], [80, 200, 80], [100, 180, 60], [120, 160, 50], [150, 140, 40], 
                        [170, 120, 20], [190, 140, 0], [220, 140, 0], [240, 140, 0], [255, 140, 0],
                        [255, 140, 0], [255, 140, 0], [255, 140, 0], [255, 140, 0], [255, 140, 0],
                        [255, 140, 0], [255, 120, 20], [255, 100, 40], [255, 80, 60], [255, 60, 80], 
                        [255, 40, 100], [255, 20, 120], [255, 0, 128], [250, 0, 128], [250, 0, 128], 
                        [250, 0, 128], [250, 0, 128], [250, 0, 128], [250, 0, 128], [250, 0, 128], 
                        [230, 0, 140], [200, 0, 160], [180, 0, 180], [160, 0, 200], [140, 0, 220], 
                        [155, 0, 240], [155, 0, 250], [155, 0, 253], [155, 0, 255], [155, 0, 255], 
                        [155, 0, 255], [155, 0, 255], [155, 0, 255], [155, 0, 255], [155, 0, 255],
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

        return vals

    def UpdateDmx(self):
        # gradient = random.choice(self.gradient_array)
        pot_val = MCP3008(0).value
        pot_val = int(pot_val* 100)

        # if pot_val != int(self.pot.value * 100):
        #     pot_val = int(self.pot.value * 100)
        #     self.pot_val_unchanged = False # ie. the value has changed

        if pot_val >= 0 and pot_val < 5:
            universe_one_gradient = self.gradient1
            universe_two_gradient = self.gradient2
            universe_three_gradient = self.gradient3
            universe_four_gradient = self.gradient4

        if pot_val >= 5 and pot_val < 10:
            universe_one_gradient = self.gradient4
            universe_two_gradient = self.gradient1
            universe_three_gradient = self.gradient2
            universe_four_gradient = self.gradient3

        if pot_val >= 10 and pot_val < 15:
            universe_one_gradient = self.gradient3
            universe_two_gradient = self.gradient4
            universe_three_gradient = self.gradient1
            universe_four_gradient = self.gradient2

        if pot_val >= 15 and pot_val < 20:
            universe_one_gradient = self.gradient5
            universe_two_gradient = self.gradient4
            universe_three_gradient = self.gradient2
            universe_four_gradient = self.gradient1

        if pot_val >= 20 and pot_val < 25:
            universe_one_gradient = self.gradient1
            universe_two_gradient = self.gradient5
            universe_three_gradient = self.gradient4
            universe_four_gradient = self.gradient3

        if pot_val >= 25:
            universe_one_gradient = self.gradient2
            universe_two_gradient = self.gradient3
            universe_three_gradient = self.gradient1
            universe_four_gradient = self.gradient5

        print(pot_val)
            
        """
        This function gets called periodically based on UPDATE_INTERVAL
        """ 

        #----------------------------------
        # Universe One Controller
        #----------------------------------

        # 5 is the amount of time we want to wait before starting to update this array.
        # Ie, this code is called every 25ms (UPDATE_INTERVAL), and it waits for five
        # intervals before outputting the first elem to the array.
        universe_one_offset = 10
        universe_one_length = 60
        
        if(self._iterable >= universe_one_offset):
            if (self._iterable >=universe_one_offset + universe_one_length):
                # 60 is the number of pixels in the strip, and after 65 iterations (since we
                # waited 5 iterations to run the first one) we'll have reached the end of the
                # strip. (ie, we offset this val by 5 in this case.)

                i = self._universe_one_data_length - 1 # gets the index pos of the last array elem
            
                # deletes the last set 6 rgb values from the array, as we are removing two pixels
                x = 0
                while x < 6:
                    self._universe_one_array[i-x] = 0
                    x += 1
                #Prevents negative values, by not subtracting past 0.
                if self._universe_one_data_length > 6:
                  self._universe_one_data_length -= 6
            else:  
                # if not at 65 iterations, the strip isn't full yet, and therefore is still ascending.
                # Adds a pixel to the array if so.  

                new_value = self.read_values(universe_one_offset, universe_one_gradient)

                self._universe_one_array.extend(new_value)
                self._universe_one_array.extend(new_value)

                # self._universe_one_array.extend([255, 0, 0])
                # self._universe_one_array.extend([255, 0, 0])
        #----------------------------------
        # Universe two controller
        #----------------------------------

        universe_two_offset = 3
        universe_two_length = 60

        if(self._iterable >= universe_two_offset):
            if (self._iterable >= universe_two_offset + universe_two_length): # checks if the strip has reached the end.
                i = self._universe_two_data_length - 1

                x = 0
                while x < 3:
                    self._universe_two_array[i-x] = 0
                    x += 1
                  
                #Prevents negative values, by not subtracting past 0.
                if self._universe_two_data_length > 3:                           
                    self._universe_two_data_length -= 3

            else:    
                new_value = self.read_values(universe_two_offset, universe_two_gradient)

                self._universe_two_array.extend(new_value)  

                # self._universe_two_array.extend([255, 0, 0])

        #----------------------------------
        # Universe three controller
        #----------------------------------
        universe_three_offset = 11
        universe_three_length = 60

        if(self._iterable >= universe_three_offset):
            if (self._iterable >= universe_three_offset + universe_three_length): # checks if the strip has reached the end. offset by 15 from 60
                i = self._universe_three_data_length - 1
                
                x = 0
                while x < 3:
                    self._universe_three_array[i-x] = 0
                    x += 1

                #Prevents negative values, by not subtracting past 0.
                if self._universe_three_data_length > 3:
                    self._universe_three_data_length -= 3
            else:    
                new_value = self.read_values(universe_three_offset, universe_three_gradient)

                self._universe_three_array.extend(new_value)

                # self._universe_three_array.extend([255, 0, 0])
 
        #----------------------------------
        # Universe four controller
        #----------------------------------
        universe_four_offset = 5
        universe_four_length = 60

        if(self._iterable >= universe_four_offset):
            if (self._iterable >= universe_four_offset + universe_four_length):
                i = self._universe_four_data_length - 1
                
                x = 0
                while x < 6:
                    self._universe_four_array[i-x] = 0
                    x += 1
                
                #Prevents negative values, by not subtracting past 0.
                if self._universe_four_data_length > 6:
                    self._universe_four_data_length -= 6

            else:
                new_value = self.read_values(universe_four_offset, universe_four_gradient)

                self._universe_four_array.extend(new_value)
                self._universe_four_array.extend(new_value)

                # self._universe_four_array.extend([255, 0, 0])
                # self._universe_four_array.extend([255, 0, 0])
                
                
        # updates the iterable at the end of this iteration. (lel tf did I just write)
        self._iterable += 1

        # Send each array, a frame of animation, to each respective universe.
        self._client.SendDmx(1, self._universe_one_array)
        self._client.SendDmx(2, self._universe_two_array)
        self._client.SendDmx(3, self._universe_three_array)
        self._client.SendDmx(4, self._universe_four_array)

        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)