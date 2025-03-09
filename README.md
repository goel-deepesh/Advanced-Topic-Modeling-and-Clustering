# Data Extraction and Preprocessing

1. Create your input folder which has the pdfs that you have to model/cluster.
2. Create an output folder (initially empty).
3. Run pixImple.py to convert .pdf files to text files (and extract images). You will get .md files for each page.
4. Run combine_markdowns.py to combine these markdowns into a single markdown for each pdf.
5. Run convert_markdown_to_json.py to convert each markdown to JSON.

Optional -

1. Run json_cleaner.py (after copying the JSONs to a separate folder) to clean the created JSONs in case of any formatting issues.

