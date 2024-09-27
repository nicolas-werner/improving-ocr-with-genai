import os
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from src.utils.logging_utils import log_info, log_success, log_error

def convert_pdf_to_jpeg(pdf_path, output_path, dpi=300):
    log_info(f"Converting PDF to JPEG: {pdf_path}", "art")
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
        images[0].save(output_path, 'JPEG')
        log_success(f"Saved JPEG image: {output_path}", "frame_with_picture")
    except Exception as e:
        log_error(f"Error converting PDF to JPEG: {str(e)}", "x")
        raise

def split_pages(input_pdf, output_dir):
    log_info(f"Splitting pages from {input_pdf} into {output_dir}", "page_facing_up")
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Open the PDF file
        with open(input_pdf, 'rb') as file:
            pdf = PdfReader(file)
            total_pages = len(pdf.pages)

            # Iterate through each page
            for page_num in range(total_pages):
                # Create a new PDF writer object
                pdf_writer = PdfWriter()
                
                # Add the page to the writer
                pdf_writer.add_page(pdf.pages[page_num])
                
                # Generate output filenames
                pdf_output_filename = f'page_{page_num + 1}.pdf'
                jpeg_output_filename = f'page_{page_num + 1}.jpg'
                pdf_output_path = os.path.join(output_dir, pdf_output_filename)
                jpeg_output_path = os.path.join(output_dir, jpeg_output_filename)
                
                # Write the individual page to a PDF file
                with open(pdf_output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                
                log_info(f"Saved PDF page {page_num + 1} to {pdf_output_filename}", "page_with_curl")

                # Convert the PDF page to JPEG
                convert_pdf_to_jpeg(pdf_output_path, jpeg_output_path)

        log_success(f"Successfully split and converted {total_pages} pages from {input_pdf}", "sparkles")
    
    except Exception as e:
        log_error(f"Error splitting pages: {str(e)}", "x")
        raise