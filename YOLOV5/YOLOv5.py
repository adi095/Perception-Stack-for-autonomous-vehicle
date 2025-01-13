import os
import cv2
import pandas as pd
import torch

#  Check if CUDA is available and use GPU if possible
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

#  YOLOv5 Class Labels (COCO dataset)
CLASS_LABELS = {
    0: "person",
    2: "car",
    7: "truck",
    9: "traffic light",
    11: "stop sign"
}

#  Define CSV output file paths
OUTPUT_FILES = {
    "person": "bounding_boxes_person.csv",
    "car": "bounding_boxes_car.csv",
    "truck": "bounding_boxes_truck.csv",
    "traffic light": "bounding_boxes_traffic_light.csv",
    "stop sign": "bounding_boxes_stop_sign.csv"
}

#  Function to load and process images using YOLOv5
def yolomodel(imgs, filenames, valueid):
    #  Load the YOLOv5 model and move it to the device (GPU/CPU)
    model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True).to(device)

    #  Process images in smaller batches to avoid memory issues
    batch_size = 4  # Adjust this based on your GPU memory
    results_list = []

    for i in range(0, len(imgs), batch_size):
        batch_imgs = imgs[i:i + batch_size]
        batch_results = model(batch_imgs)
        results_list.extend(batch_results.xyxy)

    #  Initialize lists to store results for each object type
    results_dict = {label: [] for label in CLASS_LABELS.values()}

    #  Process results and categorize by object type
    for filename, result in zip(filenames, results_list):
        for box in result.cpu().numpy():
            xmin, ymin, xmax, ymax, confidence, label = box[:6]
            label = int(label)  # Convert label to int
            label_name = CLASS_LABELS.get(label, "unknown")

            #  Store the bounding box results
            if label_name in results_dict:
                results_dict[label_name].append([filename, xmin, xmax, ymin, ymax, confidence, label])

    #  Save results to separate CSV files
    output_dir = 'D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Results'
    os.makedirs(output_dir, exist_ok=True)

    for label, data in results_dict.items():
        if data:
            #  Load original image to get its dimensions
            img_path = os.path.join('D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Images', filenames[0])
            img = cv2.imread(img_path)
            img_height, img_width = img.shape[:2]

            #  Convert bounding box coordinates to match the original image size
            df = pd.DataFrame(data, columns=['frame_name', 'xmin', 'xmax', 'ymin', 'ymax', 'confidence', 'label'])

            scale_x = img_width / 640  # YOLOv5 default width
            scale_y = img_height / 640  # YOLOv5 default height

            df['xmin'] = df['xmin'] * scale_x
            df['xmax'] = df['xmax'] * scale_x
            df['ymin'] = df['ymin'] * scale_y
            df['ymax'] = df['ymax'] * scale_y

            output_file = os.path.join(output_dir, OUTPUT_FILES[label])
            df.to_csv(output_file, index=False)
            print(f"{label.capitalize()} bounding boxes saved to: {output_file}")

#  Function to process images from the folder
def boundingboxes_frame(folder_path):
    filepaths = []
    filenames = []

    #  Loop through all .jpg files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            filepath = os.path.join(folder_path, filename)
            filepaths.append(filepath)
            filenames.append(filename)

    #  Set the value ID for the output file
    valueid = 31

    #  Run YOLO model
    yolomodel(filepaths, filenames, valueid)

#  Call the function to process images from the folder
boundingboxes_frame('D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Images')
