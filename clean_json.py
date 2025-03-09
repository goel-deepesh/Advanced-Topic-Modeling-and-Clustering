import os
import re
import json

json_folder = "/Users/deepesh/Documents/BDS_SP25/Clustering_HW_1/json_files"  

def clean_json_content(json_text):
    
    json_text = re.sub(r"```json\s*(.*?)\s*```", r"\1", json_text, flags=re.DOTALL)

    match = re.search(r"\{.*\}", json_text, re.DOTALL)
    return match.group(0) if match else None  

for file_name in os.listdir(json_folder):
    if file_name.endswith("_combined.json"):  
        file_path = os.path.join(json_folder, file_name)

        try:
           
            with open(file_path, "r", encoding="utf-8") as file:
                json_content = file.read()

            
            cleaned_json = clean_json_content(json_content)

            if cleaned_json:
                
                parsed_json = json.loads(cleaned_json)  

                
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(parsed_json, file, indent=4)  

                print(f"Cleaned and saved: {file_name}")
            else:
                print(f"No valid JSON found in: {file_name}")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

print("JSON cleaning complete!")