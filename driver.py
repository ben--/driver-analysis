# 2015-01-08

import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import NearestNeighbors

from trip import Trip

BORDER_FACTOR =10
NUM_NEIGHBOURS = 5
NUMBER_TRIPS = 200

class Driver:
    '''
    Describes one driver with trips.
    '''
    def __init__(self, driver_num):
        '''
        Initializes driver with 200 trips with calculated parameters.
        '''
        self.driver_num = driver_num
        self.trips = []
        for i in range(1,NUMBER_TRIPS+1):
            filename = 'drivers/' + str(driver_num) + '/' + str(i) + '.csv'
            trip = Trip(filename)
            trip.comp_parameters()
            self.trips.append(trip)
            # Creates lists with parameters of trip
            self.aver_speed_list = []
            self.accel_list = []
            self.length_list = []
            self.time_list = []
            for trip in self.trips:
                self.aver_speed_list.append(trip.get_average_speed())
                self.accel_list.append(trip.get_acceleration())
                self.length_list.append(trip.get_trip_length())
                self.time_list.append(trip.get_trip_time())

    def add_trip(self, filename):
        '''
        Add trip to trip list of driver.
        Filename: csv file with trip data.
        '''
        trip = Trip(filename)
        trip.comp_parameters()
        self.trips.append(trip)

    def get_aver_speed_list(self):
        return self.aver_speed_list

    def get_accel_list(self):
        return self.accel_list

    def get_length_list(self):
        return self.length_list

    def get_time_list(self):
        return self.time_list

    def comp_reach_dist(self):
        '''
        Builds list of average distance of object to nearest neighbours.
        Uses only average speed and acceleration data.
        num_neigh: number of nearest neighbours including object itself.
        '''
        speed = self.get_aver_speed_list()
        accel = self.get_accel_list()
        speed_accel = []
        for i in range(len(speed)):
            speed_accel.append([speed[i],accel[i]])
        samples = np.array(speed_accel)
        neigh = NearestNeighbors(n_neighbors=NUM_NEIGHBOURS)
        neigh.fit(samples)
        reach_dist_list = []
        for i in range(len(speed)):
            dist, ind = neigh.kneighbors(samples[i])
            reach_dist_list.append(sum(dist[0])/(len(dist[0])-1))
        return reach_dist_list

    def build_affiliation_list(self):
        '''
        Builds list of affiliation of trips to driver.
        List contains '1' if trip belongs to drive and '0' in other case.
        '''
        dist_list = self.comp_reach_dist()
        average = np.mean(np.array(dist_list))
        border = BORDER_FACTOR*average
        affiliation_list = []
        for i in range(len(dist_list)):
            if dist_list[i] > border:
                affiliation_list.append(0)
            else:
                affiliation_list.append(1)
        return affiliation_list


    def plot_parameters(self):
        '''
        Builds plot with four parameters: average speed, acceleration speed,
        trip length, trip duration.
        '''
        plt.figure()
        plt.subplot(221)
        speed_list = self.get_aver_speed_list()
        accel_list = self.get_accel_list()
        plt.plot(speed_list,accel_list, 'ro')
        plt.xlabel('Speed')
        plt.ylabel('Acceleration')

        plt.subplot(222)
        length_list = self.get_length_list()
        time_list = self.get_time_list()
        plt.plot(length_list,time_list, 'kx')
        plt.xlabel('Length')
        plt.ylabel('Time')

        plt.subplot(212)
        reach_dist = self.comp_reach_dist()
        plt.plot(reach_dist)
        ###################
        average = np.mean(np.array(reach_dist))
        x = range(len(reach_dist))
        y = [BORDER_FACTOR*average]*len(reach_dist)
        plt.plot(x,y, color='r')
        ###################
        plt.show()


