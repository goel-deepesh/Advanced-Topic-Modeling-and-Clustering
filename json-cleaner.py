import os
import re
import json

json_folder = "enter folder path"  

def clean_json_content(json_text):
    # Remove markdown code blocks if present
    json_text = re.sub(r"```json\s*(.*?)\s*```", r"\1", json_text, flags=re.DOTALL)

    # Extract JSON object
    match = re.search(r"\{.*\}", json_text, re.DOTALL)
    json_str = match.group(0) if match else None
    
    if not json_str:
        return None
        
    # Fix invalid escape sequences
    json_str = re.sub(r'\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', json_str)
    
    # Fix unterminated strings by identifying and closing unclosed quotes
    try:
        # Test if it can be parsed after fixing escapes
        json.loads(json_str)
        return json_str
    except json.JSONDecodeError as e:
        error_msg = str(e)
        
        if "Unterminated string starting at" in error_msg:
            # Get position of error
            position_match = re.search(r'char (\d+)', error_msg)
            if position_match:
                pos = int(position_match.group(1))
                
                # Find the opening quote before the error position
                in_string = False
                escaped = False
                quote_positions = []
                
                for i, char in enumerate(json_str[:pos+1]):
                    if char == '\\' and not escaped:
                        escaped = True
                        continue
                    
                    if (char == '"' or char == "'") and not escaped:
                        in_string = not in_string
                        quote_positions.append(i)
                    
                    escaped = False
                
                # If we have an odd number of quotes, we have unclosed quotes
                if len(quote_positions) % 2 == 1:
                    last_quote_pos = quote_positions[-1]
                    
                    # Find a good position to close the quote
                    # Look for comma, colon, closing bracket after the position
                    search_area = json_str[last_quote_pos+1:min(last_quote_pos+500, len(json_str))]
                    end_markers = [',', ':', '}', ']']
                    
                    for marker in end_markers:
                        marker_pos = search_area.find(marker)
                        if marker_pos != -1:
                            # Insert closing quote before the marker
                            json_str = (
                                json_str[:last_quote_pos+1+marker_pos] +
                                '"' +
                                json_str[last_quote_pos+1+marker_pos:]
                            )
                            break
                    
                    # If no marker found, just append a quote at the end of the string segment
                    if all(search_area.find(marker) == -1 for marker in end_markers):
                        json_str = json_str[:pos] + '"' + json_str[pos:]
        
        # Try additional fixes for other escape sequence issues
        elif "Invalid \\escape" in error_msg:
            # Replace all single backslashes with double backslashes
            json_str = json_str.replace('\\', '\\\\')
            # Then fix the valid escape sequences that were just doubled
            json_str = json_str.replace('\\\\n', '\\n')
            json_str = json_str.replace('\\\\r', '\\r')
            json_str = json_str.replace('\\\\t', '\\t')
            json_str = json_str.replace('\\\\b', '\\b')
            json_str = json_str.replace('\\\\f', '\\f')
            json_str = json_str.replace('\\\\"', '\\"')
            json_str = json_str.replace('\\\\/', '\\/')
            # Fix any double escaped unicode
            json_str = re.sub(r'\\\\u([0-9a-fA-F]{4})', r'\\u\1', json_str)
            
        # For severely corrupted JSON, a regex-based approach
        try:
            # See if fixes worked
            json.loads(json_str)
        except json.JSONDecodeError:
            # Brute force approach: balance all quotes and brackets            
            # Count opening and closing braces/brackets
            open_braces = json_str.count('{')
            close_braces = json_str.count('}')
            open_brackets = json_str.count('[')
            close_brackets = json_str.count(']')
            
            # Balance braces and brackets
            if open_braces > close_braces:
                json_str += '}' * (open_braces - close_braces)
            if open_brackets > close_brackets:
                json_str += ']' * (open_brackets - close_brackets)
                
            # Balance quotes i.e. replace odd quotes with escaped quotes
            in_string = False
            escaped = False
            balanced_json = ""
            
            for char in json_str:
                if char == '\\' and not escaped:
                    escaped = True
                    balanced_json += char
                    continue
                
                if char == '"' and not escaped:
                    in_string = not in_string
                
                balanced_json += char
                escaped = False
            
            # If still in a string at the end, add closing quote
            if in_string:
                balanced_json += '"'
                
            json_str = balanced_json
            
    # Validate again
    try:
        json.loads(json_str)
        return json_str
    except json.JSONDecodeError as e:
        print(f"Advanced fixes failed: {e}")
        return None

def process_json_file(file_path):
    try:
        # Read the file
        with open(file_path, "r", encoding="utf-8") as file:
            json_content = file.read()

        # Clean the JSON
        cleaned_json = clean_json_content(json_content)

        if cleaned_json:
            try:
                # Parse the JSON
                parsed_json = json.loads(cleaned_json)  

                # Write back to file
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(parsed_json, file, indent=4)  

                return True, f"Cleaned and saved successfully"
            except json.JSONDecodeError as e:
                error_position = e.pos
                context_start = max(0, error_position-30)
                error_context = cleaned_json[context_start:min(len(cleaned_json), error_position+30)]
                return False, f"Failed to parse: {e}\nError context: '...{error_context}...'"
        else:
            return False, "No valid JSON found"

    except Exception as e:
        return False, f"Error processing file: {str(e)}"

for file_name in os.listdir(json_folder):
    if file_name.endswith("_combined.json"):  
        file_path = os.path.join(json_folder, file_name)
        print(f"\nProcessing: {file_name}")
        
        success, message = process_json_file(file_path)
        
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
            
            # For persistently problematic files, more manual approach
            print("Attempting manual recovery...")
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                
                # Find the actual JSON object start and end
                json_pattern = re.compile(r'(\{(?:[^{}]|(?1))*\})', re.DOTALL)
                matches = json_pattern.findall(content)
                
                if matches:
                    largest_match = max(matches, key=len)
                    
                    # Try to parse with relaxed parsing
                    try:
                        # Use a more permissive parser if available
                        import demjson3
                        parsed = demjson3.decode(largest_match)
                        with open(file_path, "w", encoding="utf-8") as file:
                            json.dump(parsed, file, indent=4)
                        print(f"Recovered using demjson3 parser!")
                    except (ImportError, Exception):
                        # Fallback to direct file writing of the matched pattern
                        with open(file_path, "w", encoding="utf-8") as file:
                            file.write(largest_match)
                        print(f"Wrote largest valid JSON-like structure to file")
                else:
                    print("No valid JSON structure found")
            except Exception as e:
                print(f"Manual recovery failed: {e}")

print("\nJSON cleaning complete!")
