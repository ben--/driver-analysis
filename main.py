import time
import os
import random

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import preprocessing

from driver import Driver, ROOT_NAME, NUMBER_TRIPS

NUMBER_NEGATIVES = 200

class ClassificationModel:
    '''
    '''
    def __init__(self, dir_name):
        '''
        Initialize model with data as dictionary, where key is driver number and value contains trips features.
        '''
        self.model_data = {}
        dir_list = os.listdir(ROOT_NAME)
        dir_list = [int(item[:-4]) for item in dir_list]
        dir_list.sort()
        for dir in dir_list:
            print(dir)
            driver_data = (Driver(dir,('length', 'init_acceleration', 'average_speed', \
                           'max_speed', 'max_speed_angle_product'))).get_drive_data()
            self.model_data[dir] = driver_data

    def predict_model(self):
        '''
        Use 200 trips from target driver with positive labels (prob = 1)
        and 200 trips from random drivers as examples with negative labels (prob =0)
        '''
        prob_data = {}
        key_list = list(dict.keys(self.model_data))
        for key, value in (self.model_data).items():
            print(key)
            # add positive samples
            x = list.copy(value)
            y = [1]*NUMBER_TRIPS
            # add negative samples
            for i in range(NUMBER_NEGATIVES):
                key_list_negative = list.copy(key_list)
                key_list_negative.remove(key)
                driver_num = random.choice(key_list_negative)
                trip_num = random.randrange(NUMBER_TRIPS)
                negative_trip = self.model_data[driver_num][trip_num]
                x.append(negative_trip)
                y.append(0)
            # prepocessing data, scaling to [0; 1] range
            min_max_scaler = preprocessing.MinMaxScaler()
            x_train = min_max_scaler.fit_transform(np.array(x))
            y_train = np.array(y)
            # train model
            clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, \
                  max_depth=1, random_state=0).fit(x_train, y_train)
            # predict data
            prob_data[key] = list(clf.predict(value))
        return prob_data

    def write_results(self):
            '''
            Write results to file 'submission.csv' with pandas
            '''
            driver_trip = []
            prob = []
            prob_data = self.predict_model()
            for key, value in prob_data.items():
                for i in range(len(value)):
                    d_t = '%d_%d' %(key, i+1)
                    driver_trip.append(d_t)
                    prob.append(value[i])
            df = pd.DataFrame(
                 {'driver_trip':driver_trip, 'prob':prob})
            df.to_csv('submission.csv', index=False)


if __name__ == '__main__':
    start = time.time()
    ClassificationModel(ROOT_NAME).write_results()
    finish = time.time()
    print(finish-start)