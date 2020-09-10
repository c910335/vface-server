import math

class Calculator:
    def __init__(self, width):
        self.width = width

    def update(self, points):
        self.points = points

    def angle_x(self):
        return (self.distance(self.points[2], self.points[33]) - self.distance(self.points[33], self.points[14])) / 6

    def angle_y(self):
        return (self.distance(self.points[30], self.points[51]) - self.distance(self.points[28], self.points[30]) * 1.2)

    def angle_z(self):
        return math.atan2(self.points[27][0] - self.points[33][0],  self.points[33][1] - self.points[27][1]) * 100
    
    def eye_l_open(self):
        d = self.distance(self.points[43], self.points[44]) + self.distance(self.points[46], self.points[47])
        t = self.distance(self.points[43], self.points[47]) + self.distance(self.points[44], self.points[46])
        return (t / d - 0.5) * 2

    def eye_r_open(self):
        d = self.distance(self.points[37], self.points[38]) + self.distance(self.points[40], self.points[41])
        t = self.distance(self.points[37], self.points[41]) + self.distance(self.points[38], self.points[40])
        return (t / d - 0.5) * 2

    def eye_ball_x(self):
        ln = self.distance(self.points[36], self.points[68])
        rn = self.distance(self.points[42], self.points[69])
        return (-1 + ln / (ln + self.distance(self.points[39], self.points[68])) + rn / (rn + self.distance(self.points[42], self.points[69]))) * 2

    def eye_ball_y(self):
        lt = self.middle(self.points[37], self.points[38])
        ld = self.middle(self.points[40], self.points[41])
        rt = self.middle(self.points[43], self.points[44])
        rd = self.middle(self.points[46], self.points[47])
        ln = self.distance(ld, self.points[68])
        rn = self.distance(rd, self.points[69])
        return (-1 + ln / (ln + self.distance(lt, self.points[68])) + rn / (rn + self.distance(rt, self.points[69]))) * 2

    def mouth_open_y(self):
        return (self.distance(self.points[62], self.points[66]) / self.distance(self.points[33], self.points[66])) * 2

    def body_angle_z(self):
        return (self.points[2][0] + self.points[14][0] - self.points[33][0] - self.width / 2) / 20
        
    def middle(self, p1, p2):
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

    def distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
