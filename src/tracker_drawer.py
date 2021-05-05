import sys
import cv2


class TrackerDrawer:
    color = (127, 255, 0)
    distance = 0

    def __init__(self, window_name, cap, output_file_name, is_background, areas):
        self.cap_frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.cap_frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.window_name = window_name
        self.cap = cap
        self.is_background = is_background
        self.video_writer = cv2.VideoWriter(output_file_name, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))

        self.rect_list = areas.values()

    def draw(self, track):
        self.distance += track['distance']
        ms = track['frame_elapsed_ms']
        frame = track['frame']

        if track['animal']:
            x, y = track['animal']['xy']
            contours = track['animal']['contours']
            cv2.circle(frame, (x, y), 10, (0, 0, 255), thickness=2)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), thickness=2)

            for react in self.rect_list:
                self.draw_rect(frame, react, False)

        frame_seconds = ms / 1000
        cv2.putText(
            frame,
            f'distance: {int(self.distance)} / time: {int(frame_seconds)}s',
            (50, 50),
            cv2.FONT_HERSHEY_COMPLEX,
            .35,
            self.color,
            1,
            cv2.LINE_AA
        )

        if not self.is_background:
            cv2.imshow(self.window_name, frame)

        self.video_writer.write(frame)
        self.wait_until_key()

    @staticmethod
    def draw_rect(frame, rect, should_fill_rect):
        height, width, _ = frame.shape
        thickness = -1 if should_fill_rect else 1
        top_left, bottom_right = rect
        cv2.rectangle(
            frame,
            top_left,
            bottom_right,
            (0, 255, 0),
            thickness
        )

    @staticmethod
    def wait_until_key():
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit()
