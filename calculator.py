import math

class Calculator:
    def __init__(self, width):
        self.width = width
        self.params = {
            'angle_x': [0],
            'angle_y': [0],
            'angle_z': [0],
            'eye_l_open': [1],
            'eye_r_open': [1],
            'eye_ball_x': [0],
            'eye_ball_y': [0],
            'mouth_open_y': [0],
            'body_angle_z': [0]
        }
        for k in self.params:
            self.params[k] *= 5
            setattr(self, k, lambda l = k : sum(self.params[l]) / len(self.params[l]))

    def update(self, points):
        self.points = points
        for k in self.params:
            f = getattr(self, f'calc_{k}')
            self.params[k].append(f())
            self.params[k].pop(0)

    def calc_angle_x(self):
        t = self.distance(self.points[2], self.points[33]) - self.distance(self.points[33], self.points[14])
        d = self.distance(self.points[2], self.points[14])
        return (t / d) * 50

    def calc_angle_y(self):
        t = self.distance(self.points[30], self.points[51]) - self.distance(self.points[28], self.points[30])
        d = self.distance(self.points[28], self.points[51])
        return (t / d - 0.2) * 90

    def calc_angle_z(self):
        return math.atan2(self.points[27][0] - self.points[33][0],  self.points[33][1] - self.points[27][1]) * 100
    
    def calc_eye_l_open(self):
        t = self.distance(self.points[43], self.points[47]) + self.distance(self.points[44], self.points[46])
        d = self.distance(self.points[23], self.points[43]) + self.distance(self.points[24], self.points[44])
        return (t / d - 0.15) * 7

    def calc_eye_r_open(self):
        t = self.distance(self.points[37], self.points[41]) + self.distance(self.points[38], self.points[40])
        d = self.distance(self.points[19], self.points[37]) + self.distance(self.points[20], self.points[38])
        return (t / d - 0.15) * 7

    def calc_eye_ball_x(self):
        if not self.points[68] or not self.points[69]:
            return self.params['eye_ball_x'][4]
        ln = self.distance(self.points[36], self.points[68])
        rn = self.distance(self.points[42], self.points[69])
        return (-1 + ln / (ln + self.distance(self.points[39], self.points[68])) + rn / (rn + self.distance(self.points[45], self.points[69]))) * 3

    def calc_eye_ball_y(self):
        if not self.points[68] or not self.points[69]:
            return self.params['eye_ball_y'][4]
        lt = self.middle(self.points[37], self.points[38])
        ld = self.middle(self.points[40], self.points[41])
        rt = self.middle(self.points[43], self.points[44])
        rd = self.middle(self.points[46], self.points[47])
        ln = self.distance(ld, self.points[68])
        rn = self.distance(rd, self.points[69])
        return (-1.3 + ln / (ln + self.distance(lt, self.points[68])) + rn / (rn + self.distance(rt, self.points[69]))) * 3

    def calc_mouth_open_y(self):
        return (self.distance(self.points[62], self.points[66]) / self.distance(self.points[33], self.points[66])) * 2

    def calc_body_angle_z(self):
        t = self.points[2][0] + self.points[14][0] - self.points[33][0] - self.width / 2
        return (t / self.width) * 100
        
    def middle(self, p1, p2):
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

    def distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
