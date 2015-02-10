# 2015-01-07

import time
import os

import pandas as pd

from driver import Driver, ROOT_NAME

def write_results():
    '''
    Creates csv file with records if trip belong to driver
    '''
    driver_trip = []
    prob = []
    dir_list = os.listdir(ROOT_NAME)
    dir_list = [int(item[:-4]) for item in dir_list]
    dir_list.sort()
    for dir in dir_list:
        print(dir)
        driver = Driver(dir, ('max_speed', 'max_speed_angle_product'))
        affil_list = driver.build_affiliation_list()
        for i in range(len(affil_list)):
            d_t = '%s_%d'%(dir,(i+1))
            driver_trip.append(d_t)
            prob.append(affil_list[i])
    df = pd.DataFrame(
        {'driver_trip':driver_trip, 'prob':prob}
    )
    df.to_csv('submission.csv', index=False)



if __name__ == '__main__':
    start = time.time()
    write_results()
    finish = time.time()
    print(finish-start)


