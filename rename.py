import os

# Define the folder containing the JSON files
json_folder = "/Users/deepesh/Documents/BDS_SP25/Clustering_HW_1/final_jsons"  # Update with your actual folder path

# Iterate through all files in the folder
for file_name in os.listdir(json_folder):
    if file_name.endswith("_combined.json"):  # Find matching files
        old_path = os.path.join(json_folder, file_name)
        new_name = file_name.replace("_combined.json", ".json")  # Remove "_combined"
        new_path = os.path.join(json_folder, new_name)

        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {file_name} → {new_name}")
        except Exception as e:
            print(f"Error renaming {file_name}: {e}")

print("File renaming complete!")