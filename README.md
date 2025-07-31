# Advanced Topic Modeling and Clustering

A comprehensive pipeline for extracting, preprocessing, and clustering PDF documents with automated topic modeling using machine learning techniques.

## Overview

This project provides tools to:
- Convert PDF documents to structured text format
- Extract and process document content
- Perform intelligent document clustering
- Generate topic representations using AI models

## Project Structure

```
├── input/                    # Place your PDF files here
├── output/                   # Generated files will be saved here
├── pixImple.py              # PDF to text conversion
├── combine_markdowns.py     # Markdown file consolidation
├── convert_markdown_to_json.py  # Markdown to JSON conversion
├── json_cleaner.py          # JSON formatting cleanup (optional)
├── preprocessing_to_json.ipynb  # Complete preprocessing pipeline
├── clustering_topic_rep.ipynb   # Clustering and topic modeling
├── Topic_Modeling_Clustering.ipynb  # End-to-end pipeline
└── README.md
```

## Prerequisites

- Python 3.7+
- Jupyter Notebook
- Required Python packages (install via `pip install -r requirements.txt`)

## Quick Start

### Option 1: Full Automated Pipeline (Recommended for quick results with less control)

Run the complete end-to-end notebook:
```bash
jupyter notebook Topic_Modeling_Clustering.ipynb
```

This notebook handles the entire pipeline from PDF processing to final clustering results.

### Option 2: Step-by-Step Process (More control)

#### Step 1: Setup Directories
```bash
mkdir input output
```
- Place your PDF files in the `input/` folder
- The `output/` folder will store all generated files

#### Step 2: Data Extraction and Preprocessing

**Method A: Using Individual Scripts**
```bash
# Convert PDFs to markdown files (one per page)
python pixImple.py

# Combine page markdowns into single files per PDF
python combine_markdowns.py

# Convert markdown files to JSON format
python convert_markdown_to_json.py

# Optional: Clean JSON formatting issues
python json_cleaner.py
```

**Method B: Using Preprocessing Notebook**
```bash
jupyter notebook preprocessing_to_json.ipynb
```
This notebook combines steps in Method A above into a single workflow.

#### Step 3: Clustering and Topic Modeling
```bash
jupyter notebook clustering_topic_rep.ipynb
```

This notebook will:
- Define document clusters using machine learning algorithms
- Generate topic representations using Gemini AI
- Display clustering and topic representation results

## Workflow Details

### Data Processing Pipeline

1. **PDF Extraction** (`pixImple.py`)
   - Converts PDF files to markdown format
   - Extracts text content and images
   - Creates one `.md` file per PDF page

2. **Content Consolidation** (`combine_markdowns.py`)
   - Merges individual page markdowns
   - Creates a single markdown file per original PDF

3. **JSON Conversion** (`convert_markdown_to_json.py`)
   - Transforms markdown to structured JSON format
   - Prepares data for machine learning processing

4. **Data Cleaning** (`json_cleaner.py`) - Optional
   - Fixes formatting inconsistencies
   - Handles edge cases in generated JSON files

### Machine Learning Pipeline

5. **Document Clustering** (`clustering_topic_rep.ipynb`)
   - Applies clustering algorithms to group similar documents
   - Uses advanced NLP techniques for document similarity
   - Integrates with Gemini AI for topic refinement

## Output Files

After running the pipeline, you'll find:
- `output/*.md` - Markdown files for each PDF
- `output/*.json` - Structured JSON data
- Topic modeling results and cluster assignments in notebook outputs

## Troubleshooting

### Common Issues

**PDF Conversion Errors**
- Ensure PDFs are not password-protected
- Check that input files are valid PDF format

**JSON Formatting Issues**
- Run `json_cleaner.py` to fix common formatting problems
- Manually inspect problematic JSON files

**Clustering Performance**
- For large document sets, consider processing in batches
- Adjust clustering parameters based on your dataset size

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter issues or have questions:
1. Check the troubleshooting section above
2. Review existing GitHub issues
3. Create a new issue with detailed information about your problem

## Acknowledgments

- Built with Python ecosystem tools
- Utilizes Gemini AI for advanced topic modeling
- Inspired by modern document analysis workflows
