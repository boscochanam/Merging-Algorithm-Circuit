import json
import uuid
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

from calculations import calculate_avg_component_area
from main import classInitialisation
from temp import match_wire_device_points

def plot_components_and_wires(components, wires):
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot each component as a rectangle
    for c in components:
        width = c.x_bottom_right - c.x_top_left
        height = c.y_bottom_right - c.y_top_left

        rect = patches.Rectangle(
            (c.x_top_left, c.y_top_left), width, height, 
            linewidth=1, edgecolor='blue', facecolor='lightblue', alpha=0.5
        )
        ax.add_patch(rect)
        ax.text(
            c.x_top_left + width / 2, c.y_top_left + height / 2, 
            f"Comp {str(c.uuid)[-4:]}", ha="center", va="center", color="blue"
        )

    # Define colors for connected endpoints
    color_map = {"left": "green", "right": "red"}

    # Plot each wire with its left and right endpoints
    for w in wires:
        # Plot wire as a line
        x_vals = [w.x_top_left, w.x_bottom_right]
        y_vals = [w.y_top_left, w.y_bottom_right]
        ax.plot(x_vals, y_vals, "k-", lw=2)

        # Plot endpoints
        endpoints = {
            "left": w.get_endpoint_left(),
            "right": w.get_endpoint_right()
        }

        for side, (uuid, x, y) in endpoints.items():
            color = color_map[side] if (side == "left" and w.is_attached_left) or (side == "right" and w.is_attached_right) else "gray"
            ax.plot(x, y, "o", color=color)
            ax.text(x, y, f"{side[:1].upper()}{str(uuid)[-4:]}", ha="right", color=color)

    # Configure plot
    ax.set_aspect('equal', 'box')
    ax.set_title("Components and Wires with Matched Endpoints")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Example data (add your own component and wire instances)

    with open('stored_data_2.json', 'r') as file:
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
    
    devices, wires = classInitialisation(data_device, data_wire, device_uuids, image_size, classes, average_area)
    [print(device) for device in devices]
    [print(wire) for wire in wires]

    # Perform matching
    match_wire_device_points(devices, wires)

    # Visualize
    plot_components_and_wires(devices, wires)
