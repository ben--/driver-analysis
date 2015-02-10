import math

ACCELERATION_TIME = 5
SPEED_FACTOR = 3.6                 # convert m/s to km/h

class Trip:
    '''
    Class describes one trip of one driver.
    '''
    def __init__(self, data):
        '''
        Initialize with initial coordinates of points in format:
        [[x0,x1,x2,...,x(n-1)],[y0,y1,y2,...,y(n-1)]
        '''
        self.coords = data
        self.features = {}

    def comp_angle_delta(self):
        '''
        Compute list of direction angles of each part of trajectory (momentary angle delta).
        '''
        self.fi = [0,0,]
        for i in range(2,len(self.coords[0])):
            # compute angle between two direction via three sides of triangle
            y3 = self.coords[1][i]
            x3 = self.coords[0][i]
            y2 = self.coords[1][i-1]
            x2 = self.coords[0][i-1]
            y1 = self.coords[1][i-2]
            x1 = self.coords[0][i-2]
            a = math.hypot((x3-x1),(y3-y1))
            b = math.hypot((x3-x2),(y3-y2))
            c = math.hypot((x2-x1),(y2-y1))
            try:
                angle = (math.pi - math.acos((c*c+b*b-a*a)/(2*c*b)))*(180/math.pi)
            except:
                angle = 0
            self.fi.append(angle)
        self.fi[0] = self.fi[1]
        return self.fi

    def comp_speed(self):
        '''
        Compute list of speed in every point of path (momentary speed)
        '''
        self.speed = [0]
        for i in range(1,len(self.coords[0])):
            y2 = self.coords[1][i]
            x2 = self.coords[0][i]
            y1 = self.coords[1][i-1]
            x1 = self.coords[0][i-1]
            moment_speed = (math.hypot((y2-y1),(x2-x1)))*SPEED_FACTOR
            self.speed.append(moment_speed)
        return self.speed

    def comp_features(self):
        '''
        Computes dictionary with parameters: maximum speed and maximum product of
        direction change angle and speed at this moment.
        '''
        self.comp_angle_delta()
        self.comp_speed()
        # compute length of trip
        self.features['length'] = float(len(self.speed))

        # compute maximum speed
        self.features['max_speed'] = float(max(self.speed))

        # compute average speed
        self.features['average_speed'] = float(sum(self.speed)/len(self.speed))

        # compute initial acceleration
        self.features['init_acceleration'] = float(self.speed[1])

        # compute maximum product of direction change angle and speed
        speed_angle_prod = [self.speed[i]*self.fi[i] for i in range(len(self.fi))]
        self.features['max_speed_angle_product'] = float(max(speed_angle_prod))

    def get_features(self, keys):
        features = []
        for key in keys:
            features.append(self.features[key])
        return features
