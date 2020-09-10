import cv2
import dlib
from gaze_tracking import GazeTracking

class Tracker:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.width = self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        self.gaze = GazeTracking()
        self.frame = None
        self.face = None
        self.points = None

    def update(self):
        _, self.frame = self.cam.read()
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
        if all(point for point in points):
            self.points = points
            return True
        return False
