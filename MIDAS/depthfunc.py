import os
import numpy as np
import pandas as pd
import cv2

# ✅ Input and output folders
depth_images_base_dir = 'D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code'
bounding_boxes_dir = 'D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Results'
output_dir = 'D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Depth_Values'
os.makedirs(output_dir, exist_ok=True)

# ✅ Object types and corresponding depth image folders
object_types = {
    'person': 'Depth_Images_Persons',
    'car': 'Depth_Images_Cars',
    'truck': 'Depth_Images_Trucks',
    'traffic_light': 'Depth_Images_Traffic_Lights',
    'stop_sign': 'Depth_Images_Stop_Signs'
}

# ✅ Process depth values for each object type
for obj_type, depth_folder in object_types.items():
    csv_file = os.path.join(bounding_boxes_dir, f'bounding_boxes_{obj_type}.csv')
    depth_images_dir = os.path.join(depth_images_base_dir, depth_folder)

    if not os.path.exists(csv_file):
        print(f"No bounding boxes found for {obj_type}. Skipping...")
        continue

    # ✅ Load bounding boxes
    bounding_boxes = pd.read_csv(csv_file)
    depth_values = []

    # ✅ Iterate through each bounding box and corresponding depth image
    for index, row in bounding_boxes.iterrows():
        frame_name = row['frame_name']
        depth_image_path = os.path.join(depth_images_dir, f'depth_{frame_name.replace(".jpg", ".png")}')

        if not os.path.exists(depth_image_path):
            print(f"Depth image not found for {frame_name} in {depth_folder}. Skipping...")
            continue

        # ✅ Load the depth image
        depth_image = cv2.imread(depth_image_path, cv2.IMREAD_UNCHANGED)

        # ✅ Extract bounding box coordinates
        xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

        # ✅ Calculate the center of the bounding box
        center_x = (xmin + xmax) // 2
        center_y = (ymin + ymax) // 2

        # ✅ Extract the depth value at the center of the bounding box
        try:
            depth_value = depth_image[center_y, center_x]
        except IndexError:
            print(f"Error accessing depth value for {frame_name} in {depth_folder}. Skipping...")
            continue

        # ✅ Append the depth value to the list
        depth_values.append([frame_name, xmin, ymin, xmax, ymax, depth_value, obj_type])

    # ✅ Save the depth values to a CSV file
    output_csv = os.path.join(output_dir, f'depth_values_{obj_type}.csv')
    pd.DataFrame(depth_values, columns=['frame_name', 'xmin', 'ymin', 'xmax', 'ymax', 'depth', 'object_type']).to_csv(output_csv, index=False)

    print(f"Depth values for {obj_type} saved to: {output_csv}")

print("All depth values processed and saved!")
