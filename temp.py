from typing import List
from calculations import calculate_avg_component_area, calculate_distance
from classes import Component, Wire
# check if junction
def is_junction(node):
    pass

wires = []
components = []

# for w in wires:
#     # left endpoint
#     w_uuid_left, x_left, y_left = w.get_endpoint_left()
#     # right endpoint
#     w_uuid_right, x_right, x_right = w.get_endpoint_right()

    # left match
for c in components:
    area = c.get_area()
    # temp_dist = calculate_distance(x_left, y_left, c.x, c.y)


    
    
    pass

def match_wire_device_points(
    components: List[Component],
    wires: List[Wire],
): 
    """ Match the wire endpoints to the device nodes. """

    matching_threshold = 0.2 * calculate_avg_component_area(components, (10, 10))
    
    # left uuid
    for c in components:
        min_dist = float("inf")
        min_w = None
        min_flag = None

        component_left_uuid = c.get_uuid_endpoint_left()

        for w in wires:
            if w.is_attached_left and w.is_attached_right:
                continue

            # left endpoint
            w_uuid_left, x_left, y_left = w.get_endpoint_left()
            
            # right endpoint
            w_uuid_right, x_right, y_right = w.get_endpoint_right()
        
        
            temp_dist_left = c.get_distance_to_component(x_left, y_left)
            temp_dist_right = c.get_distance_to_component(x_right, y_right)

            min_temp_dist = min(temp_dist_left, temp_dist_right)
            
            # skip if not within threshold
            if min_temp_dist > matching_threshold:
                continue

            if min_temp_dist == temp_dist_left and not w.is_attached_left:
                flag = "left"
            elif min_temp_dist == temp_dist_right and not w.is_attached_right:
                flag = "right"
            else:
                continue
            
            if min_temp_dist < min_dist:
                min_dist = min_temp_dist
                min_w = w
                min_flag = flag
        
        if min_flag == "left":
            min_w.update_uuid_endpoint_left(component_left_uuid)
            min_w.is_attached_left = True
            min_w.is_attached_to_component_left = True
        else:
            min_w.update_uuid_endpoint_right(component_left_uuid)
            min_w.is_attached_right = True
            min_w.is_attached_to_component_left = True
            
    # right uuid 
    for c in components:
        min_dist = float("inf")
        min_w = None
        min_flag = None

        component_right_uuid = c.get_uuid_endpoint_right()

        for w in wires:
            if w.is_attached_left and w.is_attached_right:
                continue
            
            # left endpoint
            w_uuid_left, x_left, y_left = w.get_endpoint_left()
            
            # right endpoint
            w_uuid_right, x_right, y_right = w.get_endpoint_right()
        
        
            temp_dist_left = c.get_distance_to_component(x_left, y_left)
            temp_dist_right = c.get_distance_to_component(x_right, y_right)

            min_temp_dist = min(temp_dist_left, temp_dist_right)

            # skip if not within threshold
            if min_temp_dist > matching_threshold:
                continue

            if min_temp_dist == temp_dist_left and not w.is_attached_left:
                flag = "left"
            elif min_temp_dist == temp_dist_right and not w.is_attached_right:
                flag = "right"
            else:
                continue
            
            if min_temp_dist < min_dist:
                min_dist = min_temp_dist
                min_w = w
                min_flag = flag
        if not min_w: continue
        if min_flag == "left":
            min_w.update_uuid_endpoint_left(component_right_uuid)
            min_w.is_attached_left = True
            min_w.is_attached_to_component_left = True
        else:
            min_w.update_uuid_endpoint_right(component_right_uuid)
            min_w.is_attached_right = True
            min_w.is_attached_to_component_left = True

def match_wire_device_points_ai(components: List[Component], wires: List[Wire]):
    """Match the wire endpoints to the device nodes based on a threshold area around components."""
    
    matching_threshold = 0.2 * calculate_avg_component_area()

    def update_wire_endpoint(component_uuid, wire, flag):
        """Update wire's endpoint UUID and attachment status based on the flag (left or right)."""
        if flag == "left":
            wire.update_uuid_endpoint_left(component_uuid)
            wire.is_attached_left = True
        elif flag == "right":
            wire.update_uuid_endpoint_right(component_uuid)
            wire.is_attached_right = True

    # Match endpoints for each component
    for c in components:
        component_uuids = {
            "left": c.get_uuid_endpoint_left(),
            "right": c.get_uuid_endpoint_right()
        }

        for w in wires:
            # Skip if wire is fully attached
            if w.is_attached_left and w.is_attached_right:
                continue

            # Calculate distances from wire endpoints to component
            endpoints = {
                "left": (w.get_endpoint_left(), not w.is_attached_left),
                "right": (w.get_endpoint_right(), not w.is_attached_right)
            }

            for flag, ((w_uuid, x, y), is_available) in endpoints.items():
                if is_available:
                    distance = c.get_distance_to_component(x, y)
                    if distance < matching_threshold:
                        update_wire_endpoint(component_uuids[flag], w, flag)
