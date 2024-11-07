from typing import List, Tuple, Dict, Set
import math

from classes import Component

def calculate_avg_component_area(
    data_device: List[Component],
    image_size: Tuple[int, int]
):
    """ Calculate the average area of the components in the image. """
    area = 0
    for device in data_device:
        area += device.get_area()
    
    return area / len(data_device) * image_size[0] * image_size[1]

def calculate_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)