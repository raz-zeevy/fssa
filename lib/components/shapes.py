import numpy as np
from typing import Tuple, List



class Shape():
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

class ShapeFactory:
    @staticmethod
    def shape_from_dict(shape_dict):
        shape_type = shape_dict["shape"]
        if shape_type == "LINE":
            if shape_dict['y'] == 0:  # Handle vertical line
                if shape_dict['x'] == 0:
                    raise ValueError("Invalid parameters for a vertical line: x and y cannot both be zero.")
                slope = None  # Undefined slope for vertical line
                intercept = shape_dict['n'] / shape_dict['x']  # This represents the x-coordinate of the vertical line
                return VerticalLine(intercept=intercept)
            else:
                slope = -(shape_dict['x'] / shape_dict['y'])
                intercept = shape_dict['n'] / shape_dict['y']
                return Line(slope=slope, intercept=intercept)
        elif shape_type == "CIRCLE":
            return Circle(center=shape_dict['center'],
                          radius = shape_dict['radius'])
        elif shape_type == "AXIS":
            return DivideAxis(center=shape_dict['center'],
                          angle = shape_dict['angle'])
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")

    @staticmethod
    def shapes_from_list(shape_list):
        return [ShapeFactory.shape_from_dict(shape) for shape in shape_list]

class Line(Shape):
    def __init__(self, intercept, slope):
        self.intercept = intercept
        self.slope = slope

    def get_points(self, start, end) -> Tuple[np.array, np.array]:
        x_values = np.linspace(start, end,
                               1000)
        y_values = self.slope * x_values + self.intercept
        return x_values, y_values

class VerticalLine(Shape):
    def __init__(self, intercept):
        self.intercept = intercept  # This is the x-coordinate of the vertical line

    def get_points(self, start, end) -> Tuple[np.array, np.array]:
        # Vertical line: x is constant, y spans the range
        x_values = np.full(1000, self.intercept)  # x is constant
        y_values = np.linspace(start, end, 1000)  # y spans the range
        return x_values, y_values

class Circle(Shape):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def get_points(self, start, end) -> Tuple[np.array, np.array]:
        x_values = np.linspace(start, end,
                               1000)
        y_values = np.sqrt(
            self.radius ** 2 - (x_values - self.center[0]) ** 2) + self.center[
                       1]
        return x_values, y_values


class DivideAxis(Shape):
    def __init__(self, center, angle):
        self.center = center
        self.angle = angle

    def get_points(self, length=1000) -> Tuple[List[float], List[float]]:
        # Calculate the endpoint of the dividing axis starting from the center
        dx = length * np.cos(self.angle)
        dy = length * np.sin(self.angle)
        point = (self.center[0] + dx, self.center[1] + dy)
        return [self.center[0], point[0]], [self.center[1], point[1]]

if __name__ == '__main__':
    line = Line(-0.0762 / 0.9971, 68.0871 / 0.9971)
    circle = Circle((49.8782, 42), 19.8844)
    axis = DivideAxis((53.1744, 261.3525),  4.7732)