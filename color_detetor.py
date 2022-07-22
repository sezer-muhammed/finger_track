import numpy as np
import cv2

class ColorManager():
    def __init__(self, logger) -> None:
        self.h_min = 0
        self.s_min = 0
        self.v_min = 0
        self.h_max = 180
        self.s_max = 222
        self.v_max = 255

        self.logger = logger

        self.kernel = np.ones((5,5),np.uint8)

    def update_color_range(self, h_min = 0, s_min = 0, v_min = 0, h_max = 180, s_max = 255, v_max = 255):

        self.h_min = h_min
        self.s_min = s_min
        self.v_min = v_min

        self.h_max = h_max
        self.s_max = s_max
        self.v_mxa = v_max

        self.lower = np.array([self.h_min, self.s_min, self.v_min])
        self.upper = np.array([self.h_max, self.s_max, self.v_max])

    def filter_points(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower, self.upper)
        self.mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        self.logger.info(f"Filtering Done & Mask Created")


    def get_points(self):
        points = []
        contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) > 80:
                (x,y),radius = cv2.minEnclosingCircle(cnt)
                points.append([x, y])
        self.logger.info(f"{len(points)} Points Detected on the Image")
        return np.array(points)