import os
import fitz  # PyMuPDF
from pix2text import Pix2Text

def run_pix2text(img_fp, page_number):
    p2t = Pix2Text.from_config(device="cpu")
    kwargs = {
        "resized_shape": 1280,
        "mfr_batch_size": 1,
        "embed_sep": (" $", "$ "),
        "isolated_sep": ("$$", "$$"),
        "line_sep": "\n",
        "auto_line_break": True,
        "det_text_bbox_max_width_expand_ratio": 0.3,
        "det_text_bbox_max_height_expand_ratio": 0.2,
        "embed_ratio_threshold": 0.6,
        "table_as_image": True,
        "formula_rec_kwargs": {}
    }
    try:
        page = p2t.recognize_page(img_fp, page_number=page_number, **kwargs)
        return page
    except Exception as e:
        print(f"Error processing page {page_number}: {e}")
        return None

def save_pix2text_output(page, page_number, output_page_dir):
    os.makedirs(output_page_dir, exist_ok=True)
    output_md_path = os.path.join(output_page_dir, f'page_{page_number}.md')
    try:
        page.to_markdown(output_md_path)
        print(f"Saved Markdown to {output_md_path}")
    except Exception as e:
        print(f"Error saving Markdown for page {page_number}: {e}")

    if hasattr(page, 'images') and page.images:
        for img_name, img_data in page.images.items():
            output_img_path = os.path.join(output_page_dir, f'{page_number}_img_{img_name}')
            try:
                with open(output_img_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Saved image to {output_img_path}")
            except Exception as e:
                print(f"Error saving image {img_name} for page {page_number}: {e}")

def process_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        pdf_output_dir = os.path.join(output_dir, os.path.splitext(pdf_file)[0])
        os.makedirs(pdf_output_dir, exist_ok=True)

        doc = fitz.open(pdf_path)
        for page_number in range(len(doc)):
            page = doc.load_page(page_number)
            img_fp = os.path.join(pdf_output_dir, f'page_{page_number + 1}.png')
            pix = page.get_pixmap()
            pix.save(img_fp)

            result = run_pix2text(img_fp, page_number + 1)
            if result:
                save_pix2text_output(result, page_number + 1, pdf_output_dir)

        doc.close()
        print(f"Completed processing {pdf_file}")

input_dir = 'Input Folder Path'
output_dir = 'Output Folder Path'
process_pdfs(input_dir, output_dir)
