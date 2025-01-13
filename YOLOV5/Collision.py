import pandas as pd
import numpy as np

#  Load the world coordinates CSV file
csv_file = 'D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Results/world_coordinates.csv'
df = pd.read_csv(csv_file)

#  Define the vehicle's current position (in world coordinates)
vehicle_position = np.array([0, 0, 0])  # Example: Vehicle is at (0, 0, 0)

#  Set a safe distance threshold
safe_distance = 5.0  # Distance in meters

#  Check for potential collisions
for index, row in df.iterrows():
    object_position = np.array([row['X'], row['Y'], row['Z']])
    distance = np.linalg.norm(vehicle_position - object_position)

    if distance < safe_distance:
        print(f"⚠️ Warning: Object detected within {safe_distance} meters! (Frame: {row['frame_name']}, Distance: {distance:.2f} meters)")

print("Collision check complete.")
