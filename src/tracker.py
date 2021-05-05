import cv2
import numpy as np


class Tracker:
    threshold_animal_vs_floor = 70
    kernel_size = (25, 25)
    frame = None
    frame_number = None
    frame_ms = 0
    frame_elapsed_ms = 0

    def __init__(self, cap, width, height, floor_points, frame_without_animal):
        self.cap = cap
        self.width = width
        self.height = height
        self.floor_points = floor_points
        self.frame_without_animal = self.warp(frame_without_animal)

    def get_tracks(self):
        while self.grab_frame():
            yield {
                'frame': self.frame,
                'frame_number': self.frame_number,
                'frame_ms': self.frame_ms,
                'frame_elapsed_ms': self.frame_elapsed_ms,
                'animal': self.get_animal()
            }

    def grab_frame(self):
        has_frame, frame = self.cap.read()

        if has_frame:
            self.frame = self.warp(frame)
            self.frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.frame_ms = int(self.cap.get(cv2.CAP_PROP_POS_MSEC)) - self.frame_elapsed_ms
            self.frame_elapsed_ms += self.frame_ms

        return has_frame

    def get_animal(self):
        frame_diff = cv2.subtract(self.frame, self.frame_without_animal)
        frame_gray = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        frame_blur = cv2.GaussianBlur(frame_gray, self.kernel_size, 0)

        _, threshold = cv2.threshold(frame_blur, self.threshold_animal_vs_floor, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        if not len(contours):
            return None

        greater_contour_index = np.argmax(list(map(cv2.contourArea, contours)))
        contour = contours[greater_contour_index]
        moments = cv2.moments(contour)

        x = int(moments['m10'] / moments['m00'])
        y = int(moments['m01'] / moments['m00'])

        return {
            'xy': (x, y),
            'contours': contours,
            'contour_area': cv2.contourArea(contour)
        }

    def warp(self, frame):
        floor_points = np.float32(self.floor_points)
        box_points = np.float32([[0, 0], [self.width, 0], [self.width, self.height], [0, self.height]])
        perspective = cv2.getPerspectiveTransform(floor_points, box_points)
        return cv2.warpPerspective(frame, perspective, (self.width, self.height))
