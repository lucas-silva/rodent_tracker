import sys
import cv2
import numpy as np


class PolygonDrawer:
    color = (127, 255, 0)
    points = []

    def __init__(self, window_name, image, min_points=3, max_points=sys.maxsize):
        assert 3 <= min_points <= max_points

        self.window_name = window_name
        self.image = image
        self.min_points = min_points
        self.max_points = max_points

    def draw(self):
        cv2.imshow(self.window_name, self.image)
        cv2.setMouseCallback(self.window_name, self.draw_callback)

        if self.confirm_when(lambda: len(self.points) >= self.min_points):
            cv2.destroyWindow(self.window_name)
            return self.points
        else:
            sys.exit()

    def draw_callback(self, event, mouse_x, mouse_y, *_):
        mouse_point = (mouse_x, mouse_y)

        should_clear_points = event == cv2.EVENT_MBUTTONDOWN
        should_add_point = event == cv2.EVENT_LBUTTONDOWN
        should_draw_trace = event == cv2.EVENT_MOUSEMOVE and 0 < len(self.points) < self.max_points

        if should_clear_points:
            self.points.clear()
            cv2.imshow(self.window_name, self.image)

        if should_add_point:
            self.points.append(mouse_point)

        if should_draw_trace:
            self.draw_points(self.points + [mouse_point])

    def draw_points(self, trace_points):
        trace_frame = self.image.copy()
        trace_overlay = self.image.copy()
        trace_points = np.array(trace_points, np.int32)
        cv2.fillPoly(trace_overlay, [trace_points], self.color, cv2.LINE_AA)
        output = cv2.addWeighted(trace_frame, 0.75, trace_overlay, 0.25, 1)
        cv2.imshow(self.window_name, output)

    @staticmethod
    def confirm_when(predicate):
        key = None
        keys = ['q', '\r']

        while not (key in keys and predicate()):
            key = chr(cv2.waitKey(0))

        return key == '\r'
