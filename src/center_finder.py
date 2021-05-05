class CenterFinder:
    @staticmethod
    def find_center(center_size_rate, width, height):
        box_width = center_size_rate * width
        box_height = center_size_rate * height

        left_x = int(width / 2 - box_width / 2)
        top_y = int(height / 2 - box_height / 2)
        right_x = int(left_x + box_width)
        bottom_y = int(top_y + box_height)

        top_left = left_x, top_y
        bottom_right = right_x, bottom_y

        return top_left, bottom_right
