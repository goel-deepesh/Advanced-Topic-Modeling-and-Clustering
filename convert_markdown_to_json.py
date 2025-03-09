import re
import os
import google.generativeai as genai

genai.configure(api_key="enter key")

# Load the JSON schema
with open("json_schema.txt", "r") as file:
    json_schema = file.read()

# Function to clean response and remove markdown formatting
def clean_json_output(response_text):
    # Remove Markdown-style code blocks (```json ... ```)
    clean_text = re.sub(r"```json\s*(.*?)\s*```", r"\1", response_text, flags=re.DOTALL)
    return clean_text.strip()

# Function to process a single Markdown file
def process_markdown_file(md_file_path):
    with open(md_file_path, "r") as file:
        markdown_content = file.read()
    
    # Prepare the prompt
    prompt = f"""
    Based on the following JSON schema, extract the information from the provided Markdown content and generate a JSON output:

    JSON Schema:
    {json_schema}

    Markdown Content:
    {markdown_content}

    Please produce a JSON output which exactly follows the provided schema.
    """

    # Call the Gemini API
    model = genai.GenerativeModel('gemini-2.0-pro-exp') 
    response = model.generate_content(prompt)

    # Get the generated JSON
    generated_json = clean_json_output(response.text)

    # Save JSON file in the same folder as the Markdown file
    output_file_path = os.path.splitext(md_file_path)[0] + ".json"
    with open(output_file_path, "w") as file:
        file.write(generated_json)
    
    print(f"JSON output saved to {output_file_path}")

# Process each Markdown file
root_dir = "/Users/deepesh/Documents/BDS_SP25/Clustering_HW_1/output"
target_subdirs = ['3543', '3594', '3556', '3436', '3387'] #Batch processing to evade quota limit issues

for subdir in target_subdirs:
    subdir_path = os.path.join(root_dir, subdir)
    
    for file in os.listdir(subdir_path):
        if file.endswith(".md") and os.path.isfile(os.path.join(subdir_path, file)):
            md_file_path = os.path.join(subdir_path, file)
            
            # Check if the .md file is directly in the target subdirectory (not in a nested subdirectory)
            if os.path.dirname(md_file_path) == subdir_path:
                print(f"Processing {md_file_path}...")
                process_markdown_file(md_file_path)

print("Processing complete.")
