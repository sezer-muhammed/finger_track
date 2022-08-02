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
    def __init__(self, logger) -> None:
        cv2.setMouseCallback('Image', self.get_input)

        self.logger = logger

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
            self.logger.info(f"{joint} Has Been Created. Coordinates: x: {self.click_x}, y: {self.click_y}")
            self.__last_joint_coords[joint] = [self.click_x, self.click_y]
        self.__all_coords.append(self.__last_joint_coords)

    def match(self, points):
        result = match_numba(points, np.array(list(self.__last_joint_coords.values())))

        self.logger.info(f"Results Matched for New Frame")

        for i, joint in enumerate(self.__last_joint_coords):
            if result[i] == -1:
                continue
            try:
                self.__last_joint_coords[joint] = points[result[i]]
            except:
                pass
        self.__all_coords.append(self.__last_joint_coords.copy())

    def draw(self, frame, empty, angles):
        for joint in self.__last_joint_coords:
            coord = (int(self.__last_joint_coords[joint][0]), int(self.__last_joint_coords[joint][1]))
            frame = cv2.putText(frame, joint, coord, cv2.FONT_HERSHEY_COMPLEX, 0.3, (0, 100, 255), 1, cv2.LINE_AA)
        self.logger.info(f"Joint Points & Names Now Are on the Frame")
        joint_list = list(self.__last_joint_coords.keys())
        self.logger.info(f"Angles & Lines Are on the Image")
        for i, j in enumerate(self.__last_joint_coords):
            try:
                cv2.line(frame, (int(self.__last_joint_coords[j][0]), int(self.__last_joint_coords[j][1])), (int(self.__last_joint_coords[joint_list[i+1]][0]), int(self.__last_joint_coords[joint_list[i+1]][1])), (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(empty, (int(self.__last_joint_coords[j][0]), int(self.__last_joint_coords[j][1])), (int(self.__last_joint_coords[joint_list[i+1]][0]), int(self.__last_joint_coords[joint_list[i+1]][1])), (0, 255, 0), 2, cv2.LINE_AA)
            except:
                pass
        joint_list = list(self.__last_joint_coords.keys())
        for i, angle in enumerate(angles):
            cv2.putText(frame, f"{round(angles[angle], 1)}", (int(self.__last_joint_coords[angle][0]), int(self.__last_joint_coords[angle][1]) - 20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (2, 10, 255), 1, cv2.LINE_AA)
            # TODO ADD ARC
            p1 = self.__last_joint_coords[joint_list[i+1+1]]
            p2 = self.__last_joint_coords[angle]

            world_angle = np.arctan( (p2[1] - p1[1]) / (p2[0] - p1[0]) ) * 180 / np.pi

            if i > 2:
                cv2.ellipse(frame, (int(p2[0]), int(p2[1])), (20, 20), world_angle - 180, 0, int(angles[angle]), (255, 205, 185), 2, cv2.LINE_AA)
                cv2.ellipse(empty, (int(p2[0]), int(p2[1])), (20, 20), world_angle - 180, 0, int(angles[angle]), (255, 205, 185), 2, cv2.LINE_AA)
            else:
                cv2.ellipse(frame, (int(p2[0]), int(p2[1])), (20, 20), world_angle, 0, int(angles[angle]), (255, 205, 185), 2, cv2.LINE_AA)
                cv2.ellipse(empty, (int(p2[0]), int(p2[1])), (20, 20), world_angle, 0, int(angles[angle]), (255, 205, 185), 2, cv2.LINE_AA)

        return frame, empty

    def get_input(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.click_x = x
            self.click_y = y
            print(f"x: {x}, y: {y} Coordiantes Saved.")


    def get_joints(self):
        self.logger.info(f"Getting Joints Dict")
        return self.__last_joint_coords