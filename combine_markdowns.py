import os

def combine_output_markdowns(output_dir):
    for folder in os.listdir(output_dir):
        folder_path = os.path.join(output_dir, folder)
        if os.path.isdir(folder_path):
            combined_md_path = os.path.join(folder_path, f'{folder}_combined.md')
            with open(combined_md_path, 'w', encoding='utf-8') as combined_file:
                markdown_found = False
                # Traverse subdirectories to find output.md
                for subdir in os.listdir(folder_path):
                    subdir_path = os.path.join(folder_path, subdir)
                    if os.path.isdir(subdir_path):
                        output_md_path = os.path.join(subdir_path, 'output.md')
                        if os.path.isfile(output_md_path):
                            with open(output_md_path, 'r', encoding='utf-8') as md_file:
                                content = md_file.read().strip()
                                if content:
                                    combined_file.write(f'# {subdir}\n\n')  # Subdir name as header
                                    combined_file.write(content + '\n\n')
                                    markdown_found = True
                
                if not markdown_found:
                    print(f"No output.md files found in {folder_path}, combined file will be empty.")
                else:
                    print(f"Combined markdown saved to {combined_md_path}")

output_dir = '/Users/deepesh/Documents/BDS_SP25/Clustering_HW_1/output'
combine_output_markdowns(output_dir)
