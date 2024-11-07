from typing import List
import uuid
from calculations import calculate_avg_component_area, calculate_distance
from classes import Component, Wire, FreeNode
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
    freenodes: List[FreeNode]
): 
    """ Match the wire endpoints to the device nodes. """

    matching_threshold = 0.2 * calculate_avg_component_area(components, (10, 10))
    
    def match_component_endpoints(c: Component, is_left: bool):
        """ Match a single component's left or right endpoint to the closest wire. """
        min_dist = float("inf")
        min_w = None
        min_flag = None

        # Get the appropriate endpoint UUID for the component
        component_uuid = c.get_uuid_endpoint_left() if is_left else c.get_uuid_endpoint_right()

        for w in wires:
            if w.is_attached_left and w.is_attached_right:
                continue

            # left endpoint
            w_uuid_left, x_left, y_left = w.get_endpoint_left()
            
            # right endpoint
            w_uuid_right, x_right, y_right = w.get_endpoint_right()
        
        
            temp_dist_left = c.get_distance_wire_to_component(x_left, y_left)
            temp_dist_right = c.get_distance_wire_to_component(x_right, y_right)

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
        
        if min_w:
        
            if min_flag == "left":
                min_w.update_uuid_endpoint_left(component_uuid)
                min_w.is_attached_left = True
                min_w.is_attached_to_component_left = True
            else:
                min_w.update_uuid_endpoint_right(component_uuid)
                min_w.is_attached_right = True
                min_w.is_attached_to_component_left = True

    def match_freenode_endpoints(f: FreeNode, is_left: bool):
        """ Match a single freenode's left or right endpoint to the closest wire. """
        min_dist = float("inf")
        min_w = None
        min_flag = None

        # Get the appropriate endpoint UUID for the freenode
        freenode_uuid = f.get_uuid_endpoint_left() if is_left else f.get_uuid_endpoint_right()

        for w in wires:
            if w.is_attached_left and w.is_attached_right:
                continue

            # left endpoint
            w_uuid_left, x_left, y_left = w.get_endpoint_left()
            
            # right endpoint
            w_uuid_right, x_right, y_right = w.get_endpoint_right()
        
        
            temp_dist_left = f.get_distance_wire_to_freenode(x_left, y_left)
            temp_dist_right = f.get_distance_wire_to_freenode(x_right, y_right)

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
        
        if min_w:
        
            if min_flag == "left":
                min_w.update_uuid_endpoint_left(freenode_uuid)
                min_w.is_attached_left = True
                min_w.is_attached_to_component_left = True
            else:
                min_w.update_uuid_endpoint_right(freenode_uuid)
                min_w.is_attached_right = True
                min_w.is_attached_to_component_left = True

    # Match left endpoints
    for c in components:
        match_component_endpoints(c, is_left=True)

    # Match right endpoints
    for c in components:
        match_component_endpoints(c, is_left=False)

    # Try both matching at once for each freenode
    # modify to match only wires, since no components to junctions
    # join all wires u can, except ones already joined from before
    for f in freenodes:
        match_freenode_endpoints(f, is_left=True)
        match_freenode_endpoints(f, is_left=False)
    



# def match_wire_device_points_ai(components: List[Component], wires: List[Wire]):
#     """Match the wire endpoints to the device nodes based on a threshold area around components."""
    
#     matching_threshold = 0.2 * calculate_avg_component_area()

#     def update_wire_endpoint(component_uuid, wire, flag):
#         """Update wire's endpoint UUID and attachment status based on the flag (left or right)."""
#         if flag == "left":
#             wire.update_uuid_endpoint_left(component_uuid)
#             wire.is_attached_left = True
#         elif flag == "right":
#             wire.update_uuid_endpoint_right(component_uuid)
#             wire.is_attached_right = True

#     # Match endpoints for each component
#     for c in components:
#         component_uuids = {
#             "left": c.get_uuid_endpoint_left(),
#             "right": c.get_uuid_endpoint_right()
#         }

#         for w in wires:
#             # Skip if wire is fully attached
#             if w.is_attached_left and w.is_attached_right:
#                 continue

#             # Calculate distances from wire endpoints to component
#             endpoints = {
#                 "left": (w.get_endpoint_left(), not w.is_attached_left),
#                 "right": (w.get_endpoint_right(), not w.is_attached_right)
#             }

#             for flag, ((w_uuid, x, y), is_available) in endpoints.items():
#                 if is_available:
#                     distance = c.get_distance_to_component(x, y)
#                     if distance < matching_threshold:
#                         update_wire_endpoint(component_uuids[flag], w, flag)

def match_wire_component_points(components: List[Component], wires: List[Wire], freenodes: List[FreeNode], threshold: float = 0.1):
    """Combine wires to form new free junction components."""
    
    def create_junction(endpoint):
        """Helper function to create a new junction component."""
        new_junction = FreeNode(str(uuid.uuid4()), endpoint[0], endpoint[1])
        # new_junction = Component(str(uuid.uuid4()), endpoint[0], endpoint[0], endpoint[1], endpoint[1], "10")
        # components.append(new_junction)
        freenodes.append(new_junction)
        return new_junction

    for i, wire1 in enumerate(wires):
        for wire2 in wires[i+1:]:

            new_junction = None
            # Skip if both wires are fully attached to components
            if wire1.is_attached_to_component_left and wire1.is_attached_to_component_right:
                continue

            new_junction = None
            # Check for matching unattached endpoints
            if wire1.is_attached_to_component_left and not wire1.is_attached_to_component_right:
                # Check for proximity with wire2
                if wire2.is_attached_left:
                    distance = calculate_distance(wire1.get_endpoint_right()[1:], wire2.get_endpoint_left()[1:])
                    if distance < threshold:
                        new_junction = create_junction(wire1.get_endpoint_right()[1:])
                elif wire2.is_attached_right:
                    distance = calculate_distance(wire1.get_endpoint_right()[1:], wire2.get_endpoint_right()[1:])
                    if distance < threshold:
                        new_junction = create_junction(wire1.get_endpoint_right()[1:])

            elif wire1.is_attached_to_component_right and not wire1.is_attached_to_component_left:
                # Check for proximity with wire2
                if wire2.is_attached_left:
                    distance = calculate_distance(wire1.get_endpoint_left()[1:], wire2.get_endpoint_left()[1:])
                    if distance < threshold:
                        new_junction = create_junction(wire1.get_endpoint_left()[1:])
                elif wire2.is_attached_right:
                    distance = calculate_distance(wire1.get_endpoint_left()[1:], wire2.get_endpoint_right()[1:])
                    if distance < threshold:
                        new_junction = create_junction(wire1.get_endpoint_left()[1:])
                else:
                    continue
            
            if new_junction:
                new_junction.is_attached_left = True
                new_junction.is_attached_right = True

def conversion_to_freenodes(
    components: List[Component], 
    wires: List[Wire], 
    freenodes: List[FreeNode]
):
    """Convert junctions and wire to wire connections(now junctions) to form new freenodes."""
    for f in freenodes:
        
        junc_endpoint_left = f.get_uuid_endpoint_left()
        junc_endpoint_right = f.get_uuid_endpoint_right()

        #get the wirepoints id connected to junctions
        # add wireid in earlier methods

        # wireId = [None, None] # id of left and right wire points connected to the junction

        # # iterate and check wire endpoints
        # for w in wires:
        #     # if both uuids are found
        #     if wireId[0] and wireId[1]:
        #         break
            
        #     if w.is_attached_to_component_left:
        #         if w.uuid_endpoint_left == comp_endpoint_left:
        #             wireId[0] = w.uuid_endpoint_left
        #         elif w.uuid_endpoint_left == comp_endpoint_right:
        #             wireId[1] = w.uuid_endpoint_left
        #     if w.is_attached_to_component_right:
        #         if w.uuid_endpoint_right == comp_endpoint_left:
        #             wireId[0] = w.uuid_endpoint_right
        #         elif w.uuid_endpoint_right == comp_endpoint_right:
        #             wireId[1] = w.uuid_endpoint_right
                
        # if wireId[0] and wireId[1]:
        #     # further operations
            

        #     pass