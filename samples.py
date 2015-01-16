import time

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

from driver import Driver

def plot_one_trip(filename):
    driver_trip = pd.read_csv(filename)
    x = np.array(driver_trip['x'])
    y = np.array(driver_trip['y'])
    plt.plot(x,y)

def plot_trips_one_driver():
    start = time.time()
    for j in range(1,3):
        for i in range(1,201):
            print(i)
            filename = 'drivers/' + str(j) + '/' + str(i) + '.csv'
            plot_one_trip(filename)
        plt.grid(True)
        plt.show()

    finish = time.time()
    print(finish-start)

def from_csv_to_npy(dirname):
    for i in range(1,201):
        filename = 'drivers/' + str(dirname) + '/' + str(i) +'.csv'
        trip = pd.read_csv(filename)
        data  = np.array([np.array(trip['x']), np.array(trip['y'])])
        npy_file = 'npy/' + str(i) + '.npy'
        np.save(npy_file, data)
        np_array = np.load(npy_file)


if __name__ == '__main__':
    start = time.time()
    driver = Driver(2)
    speed = driver.get_aver_speed_list()
    accel = driver.get_accel_list()
    speed_accel = []
    for i in range(len(speed)):
        speed_accel.append([speed[i],accel[i]])
    samples = np.array(speed_accel)
    neigh = NearestNeighbors(n_neighbors=4)
    neigh.fit(samples)
    aver_dist = []
    for i in range(len(speed)):
        dist, ind = neigh.kneighbors(samples[i])
        aver_dist.append(sum(dist[0])/(len(dist[0])-1))
    finish = time.time()
    print(finish-start)
    plt.plot(aver_dist)
    plt.show()




# d1_t1 = pd.read_csv('drivers/1/1.csv')
# x = d1_t1['x']
# y = d1_t1['y']
# x1 = np.array(x)
# y1 = np.array(y)
# plt.plot(x1, y1)
# plt.grid(True)
# plt.show()