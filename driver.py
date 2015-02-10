# 2015-01-08

import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from sklearn.covariance import EllipticEnvelope
from sklearn.svm import OneClassSVM
from sklearn.neighbors import NearestNeighbors

from trip import Trip

BORDER_FACTOR = 5
NUM_NEIGHBOURS = 30
NUMBER_TRIPS = 200
ROOT_NAME = 'E:/Programming/Python/Kaggle/Driver_Telematics_Analysis/Data_Drivers/npy'

class Driver:
    '''
    Describes one driver with trips.
    '''
    def __init__(self, filename, keys):
        '''
        Initializes driver with features of 200 trips.
        '''
        npy_file = '%s/%d.npy' %(ROOT_NAME, filename)
        load_data = np.load(npy_file)
        self.drive_data = []
        for i in range(len(load_data)):
            trip = Trip(load_data[i])
            trip.comp_features()
            trip_features = trip.get_features(keys)
            self.drive_data.append(trip_features)

    def get_drive_data(self):
        return self.drive_data

    def find_outliers(self):
        '''

        '''
        features = np.array(self.drive_data)
        min_max_scaler = preprocessing.MinMaxScaler()
        samples = min_max_scaler.fit_transform(features)
        # build and train classifier
        cls = EllipticEnvelope(support_fraction=0.5, contamination=0.025)
        cls.fit(samples)
        self.predicts = cls.predict(samples)
        return self.predicts

    def build_affiliation_list(self):
        '''
        Builds list of affiliation of trips to driver.
        List contains '1' if trip belongs to drive and '0' in other case.
        '''
        affil_list = []
        self.find_outliers()
        for i in range(len(self.predicts)):
            if self.predicts[i] == 1:
                affil_list.append(1)
            else:
                affil_list.append(0)
        return affil_list

    def comp_reach_dist(self):
        '''
        Builds list of average distance of object to nearest neighbours.
        Uses only average speed and acceleration data.
        num_neigh: number of nearest neighbours including object itself.
        '''
        features = np.array(self.drive_data)
        min_max_scaler = preprocessing.MinMaxScaler()
        samples = min_max_scaler.fit_transform(features)
        neigh = NearestNeighbors(n_neighbors=NUM_NEIGHBOURS)
        neigh.fit(samples)
        reach_dist_list = []
        for i in range(len(features)):
            dist, ind = neigh.kneighbors(samples[i])
            reach_dist_list.append(sum(dist[0])/(len(dist[0])-1))
        return reach_dist_list

    def build_affiliation_list1(self):
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

    def plot_data(self):
        '''

        '''
        affil_list = self.build_affiliation_list()
        inliers = []
        outliers = []
        for i in range(len(affil_list)):
            if affil_list[i] == 1:
                inliers.append(self.drive_data[i])
            else:
                outliers.append(self.drive_data[i])
        ins = [[],[]]
        outs = [[],[]]
        for i in range(len(inliers)):
            ins[0].append(inliers[i][0])
            ins[1].append(inliers[i][1])
        for i in range(len(outliers)):
            outs[0].append(outliers[i][0])
            outs[1].append(outliers[i][1])
        plt.plot(ins[0],ins[1],'ro')
        plt.plot(outs[0],outs[1],'ko')
        plt.grid(True)
        plt.show()