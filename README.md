# Perception stack for Autonomous vehicle

## 📌 **Project Overview**
This project integrates **YOLOv5 object detection**, **MiDaS depth estimation**, **Lane detection**, **Collision detection** and **Blender 3D visualization** to create a comprehensive obstacle detection and depth estimation system. The workflow includes detecting objects from video frames, estimating their depth values, converting 2D bounding boxes to 3D world coordinates, and visualizing the detected objects in a 3D scene using Blender.

---

## ✅ **Workflow Explanation**
This project involves Five main stages:

1. **Object Detection with YOLOv5**
2. **Depth Estimation with MiDaS**
3. **Lane detection**
4. **Collision detection**
5. **3D Visualization in Blender**

Let’s break each step down in detail:

### **1️⃣ Object Detection with YOLOv5**
uses the **YOLOv5 model** to detect objects like cars, trucks, persons, and road signs from images extracted from video frames.

#### **How It Works:**
- **Readvideo.py** obtains frames from the video.
- The **YOLOv5.py** script loads the pre-trained **YOLOv5x** model from the PyTorch Hub.
- It processes images from the **`Images`** folder and saves the bounding box results to **CSV files** to calculate object midpoints.
- Network: YOLOv5 (https://pytorch.org/hub/ultralytics_yolov5/)

#### **Steps to Run YOLOv5 Detection:**
```bash
python YOLOPY.py
```
This will generate CSV files in the **`Results`** folder, such as:
- **bounding_boxes_truck.csv**
- **bounding_boxes_persons.csv**
- **bounding_boxes_cars.csv**
- **bounding_boxes_Traffic_Lights.csv**
- **bounding_boxes_Stop_Signs.csv**

Example Image is as below

![image](https://github.com/user-attachments/assets/595ae806-6513-476c-bb38-4326775c3d6c)

---

### **2️⃣ Depth Estimation with MiDaS**
The **MiDaS model** is used to estimate depth maps from the input images.

#### **How It Works:**
- The **`depth_overall.py`** script loads the MiDaS model and processes images from the **`Images`** folder.
- It generates depth maps for each image,for the pixels inside bounding boxes and saves them to the **`Depth_Images`** folder.
- Here depth values are extracted by **`depthfunc.py`**only for the pixels inside bounding boxes to get more accurate depth values for each object.
- **`DepthWorld.py`** script takes depth values and bounding box coordinates from the depth estimation step and converts pixel coordinates to world coordinates in a 3D space. 
- Network: MiDaS Transformer (https://github.com/jankais3r/Video-Depthify)

#### **Steps to Run Depth Estimation:**
```bash
python depth_overall.py
```
```bash
python depthfunc.py
```
```bash
python DepthWorld.py
```
This will generate depth maps like below (This is a full image depth map)

![image](https://github.com/user-attachments/assets/c83f24cc-521a-479b-8f4e-b9218f998ab8)

---

### **3️⃣ Lane Detection **
includes lane detection functionality using **Blender** scripts:
- Network: YOLO Pv2 (https://github.com/CAIC-AD/YOLOPv2)
- **`create_dashed_lanes.py`**: Generates dashed lane lines using curves and meshes in Blender.
- **`create_solid_line.py`**: Creates solid lane lines in Blender to represent road boundaries.

These scripts are integrated into **`blender_final.py`** to add lane markings to the 3D scene.

#### **Steps to Run Lane Detection:**
1. **Create Dashed Lanes:**
   ```bash
   blender --background --python create_dashed_lanes.py
   ```
2. **Create Solid Lines:**
   ```bash
   blender --background --python create_solid_line.py
   ```
   
**Run `blender_final.py` to Integrate Everything:**
   ```bash
   blender --background --python blender_final.py
   ```

---

### **4️⃣ Collision Detection**
The project includes a **collision detection** script to check if any detected objects are within a **dangerous proximity** to the vehicle based on depth data.

#### **How It Works:**
- The **`collision_detection.py`** script loads depth values and calculates the distance between the vehicle and detected objects.
- If any object is within a **safe distance threshold**, it prints a **warning message**.

#### **Steps to Run Collision Detection:**
```bash
python collision_detection.py
```
This will check for potential collisions and display warnings like:
```
⚠️ Warning: Object detected within 5 meters! (Frame: frame_001, Distance: 4.8 meters)
```
---

### **5️⃣ 3D Visualization in Blender**
The final step is to visualize the detected objects in a **3D scene** using **Blender**.

#### **How It Works:**
- The **`blender_final.py`** script automates the process of:
  - Importing detected objects into Blender.
  - Adding lanes, dashed lines, and traffic lights.
  - Rendering images and saving them to the **`Blender`** folder.

#### **Steps to Run Blender Automation:**
```bash
blender --background --python blender_final.py
```
This will render the scene and save images to the **`Blender`** folder.

---

## References
1. Lane Detection: [LaneNet](https://github.com/IrohXu/lanenet-lane-detection-pytorch)
2. Monocular Depth Estimation: [MiDaS](https://github.com/isl-org/MiDaS)
3. Object Detection (Cars, Trucks, Traffic Lights, Road Signs): 
   - [MobilenetV1-SSD](https://github.com/xiaogangLi/tensorflow-MobilenetV1-SSD)
   - [YOLOv7](https://github.com/WongKinYiu/yolov7)
4. Traffic Light Detection: [YOLOv3 for Traffic Lights](https://github.com/sovit-123/TrafficLight-Detection-Using-YOLOv3)
5. Road Sign Detection: [Road Sign Detection](https://github.com/Anantmishra1729/Road-sign-detection)
6. 3D Bounding Boxes: [YOLO3D](https://github.com/ruhyadi/YOLO3D)
7. Pedestrian Keypoint Detection: [Multi-Person Pose Estimation](https://github.com/ZheC/Realtime_Multi-Person_Pose_Estimation)

## 🛠 **Dependencies**
- **Python 3.8+**
- **PyTorch**
- **OpenCV**
- **Matplotlib**
- **Blender**
- **MoviePy**
- **CUDA**
  
To install the required libraries, run:
```bash
pip install torch opencv-python matplotlib moviepy
```

---
