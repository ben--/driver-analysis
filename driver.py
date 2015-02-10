import numpy as np

from trip import Trip

BORDER_FACTOR = 5
NUM_NEIGHBOURS = 30
NUMBER_TRIPS = 200
ROOT_NAME = 'E:/Programming/Python/Kaggle/Driver_Telematics_Analysis/Data_Drivers/npy'
#ROOT_NAME = 'E:/Programming/Python/Kaggle/Driver_Telematics_Analysis/driver_telematics_analysis_source/npy'

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
