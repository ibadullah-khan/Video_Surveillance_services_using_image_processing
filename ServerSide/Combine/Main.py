import cv2
import os
import dlib
import webcolors
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


import DetectChars
import DetectPlates

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

class Detection:
    
    plate_val = ''
    no_plate = 'no plate detected'
    no_car = 'no car detected'
    no_color = "nothing"
    same_frame = 'same frame detected'
    no_plate_counter = 0
    plate_record = []
    
    def __init__(self):
        self.plate_val = 'none'
    
    def getPlateVal(self):
        return self.plate_val
    
    def setPlateVal(self, value):
        self.plate_val = value
    
    def closest_colour(self, requested_colour):
        min_colours = {}
        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]
    
    def get_colour_name(self, requested_colour):
        try:
            closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
        except ValueError:
            closest_name = self.closest_colour(requested_colour)
            actual_name = None
        return actual_name, closest_name
    
    def find_histogram(self, clt):
            
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    
        hist = hist.astype("float")
        hist /= hist.sum()
    
        return hist
    
    def plot_colors2(self, hist, centroids):
        bar = np.zeros((50, 300, 3), dtype="uint8")
        startX = 0
    
        
        maxPercent = -1
        maxColor = []
        
        for (percent, color) in zip(hist, centroids):
            # plot the relative percentage of each cluster
            
            
            if percent > maxPercent:
                maxPercent = percent
                maxColor = color
            
            endX = startX + (percent * 300)
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                          color.astype("uint8").tolist(), -1)
            startX = endX
    
        # return the bar chart
        
        #maxP = max(maxPercent)
        #maxC = maxColor[maxPercent.index(maxP)]
        #maxPercent.remove(maxP)
        #minP = max(maxPercent)
        
        #diffP = maxP - minP
        
        return bar, maxColor
       
        
    def detect_car(self, original_image):
    
        detector = dlib.fhog_object_detector("car_detector_100.svm")
        
        gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        
        cars = detector(gray)
        
        a = 1
        b = 1
        h = 1
        w = 1
        
        for i in cars:
            cv2.rectangle(original_image, (i.left(), i.top()), (i.right(), i.bottom()), (0, 0, 255), 2)
            a = i.left()
            b = i.top()
            h = i.bottom() - i.top()
            w = i.right() - i.left()
        
        cropped = original_image[b:b+h, a:a+w]
        
        if len(cropped) <= 1:
            return self.no_car, self.no_color
        else:
            return self.detect_plate(cropped)
        
    def detect_plate(self, cropped_image):
        
        detector = dlib.fhog_object_detector("plate_detector_100.svm")
        
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        
        cars = detector(gray)
        
        a = 1
        b = 1
        h = 1
        w = 1
        
        for i in cars:
            cv2.rectangle(cropped_image, (i.left(), i.top()), (i.right(), i.bottom()), (0, 0, 255), 2)
            a = i.left()
            b = i.top()
            h = i.bottom() - i.top()
            w = i.right() - i.left()
        
        cropped_plate = cropped_image[b:b+h, a:a+w]
        
        if len(cropped_plate) <= 1:
            if self.no_plate_counter == 1:
                return self.same_frame, self.no_color
            else:
                self.no_plate_counter = 1
                return self.no_plate, self.get_car_color(cropped_image)
        else:
            self.no_plate_counter = 0
            return self.main(cropped_plate, cropped_image)
    
    def getFromPlateRecord(self, plate):
        if plate in self.plate_record:
            return True
        else:
            return False
    
    def main(self, cropped_plate_image, cropped_car):
    
        blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         # attempt KNN training
    
        if blnKNNTrainingSuccessful == False:                               # if KNN training was not successful
            print("\nerror: KNN traning was not successful\n")  # show error message
            return                                                          # and exit program
    
        imgOriginalScene  = cropped_plate_image               # open image
    
        if imgOriginalScene is None:                            # if image was not read successfully
            print("\nerror: image not read from file \n\n")  # print error message to std out
            os.system("pause")                                  # pause so user can see error message
            return                                              # and exit program
    
        listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           # detect plates
    
        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates
    
    
        if len(listOfPossiblePlates) != 0:                          
            listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)
    
            licPlate = listOfPossiblePlates[0]
    
            if len(licPlate.strChars) == 0:                     # if no chars were found in the plate
                return self.no_plate, self.get_car_color(cropped_car)                                       # and exit program
            
            if not self.getFromPlateRecord(licPlate.strChars) :
                self.plate_record.append(licPlate.strChars)
                color_value = self.get_car_color(cropped_car)
                return licPlate.strChars, color_value
            else:
                return self.same_frame, self.no_color
        else:
            return self.no_plate, self.no_color
    
    def get_car_color(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        image = image.reshape((image.shape[0] * image.shape[1],3)) #represent as row*column,channel number
        clt = KMeans(n_clusters=3) #cluster number
        clt.fit(image)
        
        hist = self.find_histogram(clt)
        bar, maxColor = self.plot_colors2(hist, clt.cluster_centers_)
        
        requested_colour = (int(maxColor[0]), int(maxColor[1]), int(maxColor[2]))
        
        actual_name, closest_name = self.get_colour_name(requested_colour)
        
        return self.filter(closest_name)
    
    def filter(self, color_name):
        red = [ "maroon", "rosybrown", "darkred", "brown", "firebrick", "crimson", "tomato", "red", "coral", "indianred", "lightcoral", "darksalmon", "salmon", "lightsalmon", "orangered", "darkorange", "orange" ]
        blue = [ "aqua", "dimgrey", "slategrey", "cyan", "lightcyan", "darkturquoise", "mediumturquoise", "paleturquoise", "aquamarine", "powderblue", "cadetblue", "steelblue", "cornflowerblue", "deepskyblue", "dodgerblue", "lightsteelblue", "lightblue", "skyblue", "lightskyblue", "midnightblue", "navy", "darkblue", "mediumblue", "blue", "royalblue", "blueviolet", "indigo", "darkslateblue", "slateblue", "mediumslateblue" ]
        gray = [ "gray", "lightslategrey", "grey", "gray/grey", "darkslategrey", "silver", "darkgray", "darkgrey", "slategray", "lightslategray" ]
        black = [ "black", "dimgray", "dimgrey", "dimgray/dimgrey" ]
        white = [ "whitesmoke", "gainsboro", "white", "snow", "azure", "lightgrey", "floralwhite", "mintcreem", "ghostwhite" ]
        
        if color_name in red:
            return "red"
        elif color_name in blue:
            return "blue"
        elif color_name in gray:
            return "gray"
        elif color_name in white:
            return "white"
        if color_name in black:
            return "black"
        else:
            return color_name