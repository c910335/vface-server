import cv2
import dlib
from gaze_tracking import GazeTracking

class Tracker:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH) / 4)
        self.height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT) / 4)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        self.gaze = GazeTracking()
        self.gaze._face_detector = lambda f : [self.face]
        self.frame = None
        self.face = None
        self.points = None

    def update(self):
        _, frame = self.cam.read()
        self.frame = cv2.resize(frame, (self.width, self.height))
        cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        if self.update_face():
            return self.update_points()
        return False

    def update_face(self):
        faces = self.detector(self.frame, 0)
        if faces:
            self.face = max(faces, key=lambda face: (face.right() - face.left()) * (face.bottom() - face.top()))
            return True
        return False

    def update_points(self):
        shape = self.predictor(self.frame, self.face)
        self.gaze.refresh(self.frame)
        points = []
        for i in range(68):
            point = shape.part(i)
            points.append((point.x, point.y))
        points.append(self.gaze.pupil_left_coords())
        points.append(self.gaze.pupil_right_coords())
        if all(point for point in points[:68]):
            self.points = points
            return True
        return False
