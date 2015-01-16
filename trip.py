#2015-01-06
import math

import pandas as pd

ACCELERATION_TIME = 5
SPEED_CONSTANT = 3.6                 # convert m/s to km/h

class Trip:
    '''
    Class describes one trip of one driver.
    '''
    def __init__(self, filename):
        '''
        Class is initialized with Pandas Data Frame received from .csv file.
        '''
        self.coordinate_list = pd.read_csv(filename)

    def comp_length(self, start, stop):
        '''
        Returns length between two points appointed in seconds.
        '''
        x = self.coordinate_list['x']
        y = self.coordinate_list['y']
        length = 0
        for i in range(start, stop):            ####### must be (stop+1) ???
            x1 = float(x[i-1])
            x2 = float(x[i])
            y1 = float(y[i-1])
            y2 = float(y[i])
            segment = math.sqrt((y2-y1)**2+(x2-x1)**2)
            length += segment
        return length

    def comp_parameters(self):
        '''
        Computes parameters: acceleration, average speed, trip time, trip length.
        '''

        # compute trip time
        self.trip_time = len(self.coordinate_list)

        # compute trip length
        self.trip_length = self.comp_length(1,self.trip_time)

        # compute acceleration speed
        self.acceleration = ((self.comp_length(1,ACCELERATION_TIME-1))/ACCELERATION_TIME)/ACCELERATION_TIME

        # compute average speed of trip without taking acceleration time
        period = self.trip_time - ACCELERATION_TIME
        length = self.comp_length(ACCELERATION_TIME, self.trip_time)
        self.average_speed = (length/period)*SPEED_CONSTANT

    def get_coordinate_list(self):
        return self.coordinate_list

    def get_trip_time(self):
        return self.trip_time

    def get_trip_length(self):
        return self.trip_length

    def get_acceleration(self):
        return self.acceleration

    def get_average_speed(self):
        return self.average_speed
