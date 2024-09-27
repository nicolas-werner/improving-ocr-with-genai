import logging
from src.config import load_config
from src.preprocessing.page_splitter import split_pages
from src.ocr.transkribus_api import process_with_transkribus
from src.ocr.openai_ocr import process_with_openai
from src.utils.logging_utils import setup_logging, log_info, log_error, log_success
from src.models import OCRResult

def run_pipeline():
    setup_logging()
    config = load_config()

    try:
        log_info("Starting pipeline", "rocket")
        
        # Step 1: Preprocessing - Split pages
        split_pages(config['input_pdf'], config['output_dir'])
        log_info("Pages split", "check")
        # Step 2: Transkribus OCR
        transkribus_results = process_with_transkribus(config['output_dir'], config['transkribus'])
        log_info("Transkribus OCR completed", "check")
        # Step 3: OpenAI OCR
        final_results: OCRResult = process_with_openai(transkribus_results, config['openai'])
        log_info("OpenAI OCR completed", "check")
        log_success("Pipeline completed successfully", "checkmark")
        return final_results
    
    except Exception as e:
        log_error(f"Pipeline failed: {str(e)}", "cross_mark")
        raise

if __name__ == "__main__":
    run_pipeline()