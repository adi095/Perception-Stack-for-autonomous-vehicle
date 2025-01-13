import os
import cv2
import torch
import matplotlib.pyplot as plt
import pandas as pd

#  Load MiDaS model
model_type = "DPT_Large"
midas = torch.hub.load("intel-isl/MiDaS", model_type)
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
midas.to(device)
midas.eval()

#  Load MiDaS transforms
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
transform = midas_transforms.dpt_transform if model_type == "DPT_Large" else midas_transforms.small_transform

#  Input folders
input_folder = "D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Images"
bounding_boxes_folder = "D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Results"

#  Output folders
output_folders = {
    "car": "D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Depth_Images_Cars",
    "person": "D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Depth_Images_Persons",
    "truck": "D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Depth_Images_Trucks",
    "traffic_light": "D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Depth_Images_Traffic_Lights",
    "stop_sign": "D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Depth_Images_Stop_Signs",
}

#  Create output folders if they don't exist
for folder in output_folders.values():
    os.makedirs(folder, exist_ok=True)

#  List of object classes to process
object_classes = ["car", "person", "truck", "traffic_light", "stop_sign"]

#  Iterate over each object class and its corresponding bounding boxes CSV
for obj_class in object_classes:
    csv_file = os.path.join(bounding_boxes_folder, f"bounding_boxes_{obj_class}.csv")

    #  Check if the CSV file exists
    if not os.path.exists(csv_file):
        print(f"No bounding boxes found for {obj_class}. Skipping...")
        continue

    #  Load bounding boxes
    bounding_boxes = pd.read_csv(csv_file)

    #  Process each image in the input folder
    for filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image: {filename}")
            continue

        print(f"Processing {obj_class} in: {filename}")
        h, w = image.shape[:2]

        #  Apply MiDaS model to compute the depth map
        input_batch = transform(image).to(device)
        with torch.no_grad():
            prediction = midas(input_batch)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=(h, w),
                mode="bicubic",
                align_corners=False,
            ).squeeze()
        depth_map = prediction.cpu().numpy()

        #  Filter depth map based on bounding boxes for the current class
        relevant_boxes = bounding_boxes[bounding_boxes["frame_name"] == filename]
        for index, row in relevant_boxes.iterrows():
            xmin, ymin, xmax, ymax = int(row["xmin"]), int(row["ymin"]), int(row["xmax"]), int(row["ymax"])

            #  Create a mask to highlight the object area in the depth map
            masked_depth_map = depth_map.copy()
            masked_depth_map[:ymin, :] = 0
            masked_depth_map[ymax:, :] = 0
            masked_depth_map[:, :xmin] = 0
            masked_depth_map[:, xmax:] = 0

            #  Save the output depth map in the appropriate folder
            output_filename = f"depth_{os.path.splitext(filename)[0]}_{obj_class}.png"
            plt.figure(figsize=(10, 10))
            plt.imshow(masked_depth_map, cmap="plasma")
            plt.axis("off")
            plt.savefig(os.path.join(output_folders[obj_class], output_filename), format="png", dpi=300)
            plt.close()

            print(f"Saved depth map for {obj_class}: {output_filename}")

print("All images processed and depth maps saved per class!")
