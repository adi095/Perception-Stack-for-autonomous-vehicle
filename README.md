# Perception stack for Autonomous vehicle**

## 📌 **Project Overview**
This project integrates **YOLOv5 object detection**, **MiDaS depth estimation**, **Lane detection**, **Collision detection** and **Blender 3D visualization** to create a comprehensive obstacle detection and depth estimation system. The workflow includes detecting objects from video frames, estimating their depth values, converting 2D bounding boxes to 3D world coordinates, and visualizing the detected objects in a 3D scene using Blender.

---

## 📁 **Project Structure**
```plaintext
📂 Perception_Stack_Autonomous_Vehicles
├── 📂 Images                     # Input images for object detection
├── 📂 Depth_Images               # Depth maps generated from MiDaS
├── 📂 Results                    # CSV files with bounding boxes and depth values
├── 📂 Blender                    # Rendered images from Blender
├── 📂 Videos                     # Final video output
├── 📄 object_detection_depth_estimation.py  # YOLOv5 + MiDaS script
├── 📄 depthfunc.py               # Extract depth values from images
├── 📄 blender_final.py           # Blender automation script
├── 📄 make_video.py              # Convert rendered images to video
├── 📄 create_dashed_lanes.py     # Creates dashed lane lines in Blender
├── 📄 create_solid_line.py       # Creates solid lane lines in Blender
├── 📄 collision_detection.py     # Checks for potential collisions using depth data
├── 📄 README.md                  # Project documentation (this file)
└── 📝 Additional Python Scripts  # Helper scripts for lane creation, brake lights, etc.
```

---

## ✅ **Workflow Explanation**
This project involves three main stages:

1. **Object Detection with YOLOv5**
2. **Depth Estimation with MiDaS**
3. **Lane detection**
4. **Collision detection**
5. **3D Visualization in Blender**

Let’s break each step down in detail:

### **1️⃣ Object Detection with YOLOv5**
The project uses the **YOLOv5 model** to detect objects like cars, trucks, persons, and road signs from images extracted from video frames.

#### **How It Works:**
- The **YOLOPY.py** script loads the pre-trained **YOLOv5x** model from the PyTorch Hub.
- It processes images from the **`Images`** folder and saves the bounding box results to **CSV files**.

#### **Steps to Run YOLOv5 Detection:**
```bash
python YOLOPY.py
```
This will generate CSV files in the **`Results`** folder, such as:
- **bounding_boxes_truck_31.csv**
- **bounding_boxes_persons.csv**
- **bounding_boxes_cars.csv**

---

### **2️⃣ Depth Estimation with MiDaS**
The **MiDaS model** is used to estimate depth maps from the input images.

#### **How It Works:**
- The **`depth_overall.py`** script loads the MiDaS model and processes images from the **`Images`** folder.
- It generates depth maps for each image and saves them to the **`Depth_Images`** folder.

#### **Steps to Run Depth Estimation:**
```bash
python depth_overall.py
```
This will generate depth maps like:
- **depth_frame_001.png**
- **depth_frame_002.png**

---

### **3️⃣ Lane Detection in Blender**
Your project includes lane detection functionality using **Blender** scripts:

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
3. **Run `blender_final.py` to Integrate Everything:**
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

## 🖥️ **How to Run the Entire Workflow**

### **Step 1: Object Detection**
```bash
python YOLOPY.py
```

### **Step 2: Depth Estimation**
```bash
python depth_overall.py
```

### **Step 3: Depth Extraction**
```bash
python depthfunc.py
```

### **Step 4: Blender 3D Visualization**
```bash
blender --background --python blender_final.py
```

### **Step 5: Create Video Output**
```bash
python make_video.py
```

### **Step 6: Collision Detection**
```bash
python collision_detection.py
```
---

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

## 📄 **License**
This project is licensed under the MIT License.

---

