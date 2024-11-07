import sys
from typing import List, Tuple, Dict
import math
import uuid
import json
from classes import Component, Wire, FreeNode
from calculations import calculate_avg_component_area
from temp import match_wire_device_points, match_wire_component_points, conversion_to_freenodes
from class_map import get_class_mapping

def classInitialisation(
    data_device: Dict[str, Tuple[float, float, float, float]],
    data_wire: Dict[str, Tuple[float, float, float, float, float]],
    device_uuids: Dict[str, List[str]],
    image_size: List[Tuple[str, str]],
    classes: List[str],
    average_area: float,
) -> Tuple[List[Component], List[Wire]]:
    """ Initialize the classes and the data. """

    device_list = []
    wire_list = []
    freenode_list = []

    for i, device in enumerate(data_device):
        if get_class_mapping(classes[i]) == "junction":
            x_top_left, y_top_left, x_bottom_right, y_bottom_right = data_device[device]
            
            x, y = (x_top_left + x_bottom_right) / 2, (y_top_left + y_bottom_right) / 2
            freenode_uuid = str(uuid.uuid4())
            freenode = FreeNode(freenode_uuid, x, y)
            freenode_list.append(freenode)
            continue

        # normal devices
        device_uuid = str(uuid.uuid4())
        x_top_left, y_top_left, x_bottom_right, y_bottom_right = data_device[device]
        device = Component(device_uuid, x_top_left, y_top_left, x_bottom_right, y_bottom_right, classes[i])
        device_list.append(device)
    
    for wire in data_wire:
        angle, x_top_left, y_top_left, x_bottom_right, y_bottom_right = wire[0], wire[1], wire[2], wire[3], wire[4]
        wire = Wire(angle, x_top_left, y_top_left, x_bottom_right, y_bottom_right)
        wire_list.append(wire)
    
    return device_list, wire_list, freenode_list

def match_wire_device_points(
    components: List[Component],
    wires: List[Wire],
): 
    """ Match the wire endpoints to the device nodes. """

    # Threshold for matching the wire endpoints to the device nodes
    # matching_threshold = 0.2 * calculate_avg_component_area()

    for w in wires:
        
        pass
    
    for w in wire_uuid:
        wire_uuid_endpoint_1, wire_uuid_endpoint_2 = w

    device_uuids_eg = device_uuids["deviceId"]   #2/4 uuids of device nodes to join

    
if __name__ == "__main__":
    with open('stored_data.json', 'r') as file:
        data = json.load(file)
    
    # Assuming the JSON structure matches the function parameters
    data_device = data['data_device']
    data_wire = data['data_wire']
    device_uuids = data['device_uuids']
    image_size = data['image_size']
    classes = data['classes']
    average_area = 0

    # based on the len of data_wire
    wire_uuid = [(str(uuid.uuid4()), str(uuid.uuid4())) for _ in range(len(data_wire))] 
    
    devices, wires, freenodes = classInitialisation(data_device, data_wire, device_uuids, image_size, classes, average_area)

    # pass 1 - from components to wires only
    match_wire_device_points(devices, wires, freenodes)

    # pass 2 - from wires
    match_wire_component_points(wires, devices, freenodes)

    # conversion of junctions, wire to wire => freenodes
    conversion_to_freenodes(wires, devices, freenodes) 


    # [print(device) for device in devices]
    # [print(wire) for wire in wires]

    print(image_size)
    print("Average Area: ", calculate_avg_component_area(devices, image_size))