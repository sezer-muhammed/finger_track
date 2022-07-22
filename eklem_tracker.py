import numpy as np
import cv2
from numba import jit

@jit(nopython = True)
def match_numba(points, joints_coords):
    result = []
    for j in joints_coords:
        min = 1e5
        index = -1
        for i, p in enumerate(points):
            p_x = p[0]
            p_y = p[1]

            j_x = j[0]
            j_y = j[1]

            error = (p_x - j_x) ** 2 + (p_y - j_y) ** 2

            if error < min and error < 16000:
                min = error
                index = i
        result.append(index)
    return result




class EklemTracker():
    def __init__(self) -> None:
        cv2.setMouseCallback('Image', self.get_input)

        self.click_x = 0
        self.click_y = 0

        self.__all_coords = []

        self.__last_joint_coords = {"isaret_uc": [0, 0], 
                                    "isaret_DIP": [0, 0], 
                                    "isaret_PIP": [0, 0], 
                                    "isaret_MP": [0, 0], 
                                    "CMC": [0, 0], 
                                    "bas_PIP": [0, 0], 
                                    "bas_DIP": [0, 0], 
                                    "bas_uc": [0, 0]}
        self.combined_uc = [0, 0]

    def get_all(self):
        return self.__all_coords

    def initialize_joints(self, frame, color_manager):
        frame_origin = frame.copy()
        for joint in self.__last_joint_coords:
            message = f"Please Click on The {joint} Joint, Then Click 'S'"
            frame = cv2.putText(frame_origin.copy(), message, (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1.4, (25, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow("Image", frame)
            cv2.waitKey(0)
            self.__last_joint_coords[joint] = [self.click_x, self.click_y]
        self.__all_coords.append(self.__last_joint_coords)

    def match(self, points):
        result = match_numba(points, np.array(list(self.__last_joint_coords.values())))
        for i, joint in enumerate(self.__last_joint_coords):
            if result[i] == -1:
                continue
            try:
                self.__last_joint_coords[joint] = points[result[i]]
            except:
                pass
        self.__all_coords.append(self.__last_joint_coords)

    def draw(self, frame):
        for joint in self.__last_joint_coords:
            coord = (int(self.__last_joint_coords[joint][0]), int(self.__last_joint_coords[joint][1]))
            frame = cv2.putText(frame, joint, coord, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 100, 255), 1, cv2.LINE_AA)
        return frame

    def get_input(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.click_x = x
            self.click_y = y
            print(f"x: {x}, y: {y} Coordiantes Saved.")


    def get_joints(self):
        return self.__last_joint_coords