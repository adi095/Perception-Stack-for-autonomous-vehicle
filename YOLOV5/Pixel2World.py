import os
import numpy as np
import pandas as pd

#  Camera Matrix (Intrinsic Parameters)
K = np.array([
    [800, 0, 640],  # fx, 0, cx
    [0, 800, 360],  # 0, fy, cy
    [0, 0, 1]       # 0, 0, 1
])

#  Print the Camera Matrix
print("Using generic camera matrix (K):")
print(K)

#  Directory containing bounding box CSV files
csv_dir = 'D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Results'

# List of object types to process
object_types = ['person', 'car', 'truck', 'traffic_light', 'stop_sign']

# Iterate through each object type
for obj_type in object_types:
    csv_file = os.path.join(csv_dir, f'bounding_boxes_{obj_type}.csv')

    # Check if the CSV file exists
    if os.path.exists(csv_file):
        print(f"Processing {obj_type} bounding boxes...")

        # Load the bounding boxes from the CSV file
        bounding_boxes = pd.read_csv(csv_file)

        # Convert pixel coordinates to world coordinates
        world_coordinates = []

        for index, row in bounding_boxes.iterrows():
            xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
            u = (xmin + xmax) / 2
            v = (ymin + ymax) / 2
            Z = 1.0  # Assume a default depth of 1.0

            # Convert pixel coordinates to world coordinates
            pixel_coords = np.array([[u], [v], [1]])
            world_coords = np.linalg.inv(K) @ (pixel_coords * Z)

            # Append the world coordinates
            world_coordinates.append([row['frame_name'], world_coords[0][0], world_coords[1][0], world_coords[2][0]])

        # Save the world coordinates to a CSV file
        output_csv = os.path.join(csv_dir, f'world_coordinates_{obj_type}.csv')
        pd.DataFrame(world_coordinates, columns=['frame_name', 'X', 'Y', 'Z']).to_csv(output_csv, index=False)
        print(f"World coordinates for {obj_type} saved to: {output_csv}")

    else:
        print(f"No bounding boxes found for {obj_type}. Skipping...")
