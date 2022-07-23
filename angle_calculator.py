import numpy as np
import math

class AngleCalculator():
    def __init__(self, logger) -> None:
        self.logger = logger
        self.__all_angles = []
        pass

    def get_angle(self, joints):
        keys = list(joints.keys())
        angles = {}
        for i, joint in enumerate(joints):
            if "uc" in joint:
                continue
            angle_name = f"{keys[i]}"
            angle = self.__calculate_angle(joints[keys[i-1]], joints[keys[i]], joints[keys[i+1]])
            angles[angle_name] = angle
        self.__all_angles.append(angles)
        self.logger.info(f"Getting Angle Dict")
        return angles
        
    def get_all(self):
        return self.__all_angles

    def __calculate_angle(self, a, b, c):
        ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))

        return 360 - (ang + 360 if ang < 0 else ang)