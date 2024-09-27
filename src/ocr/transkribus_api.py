import requests
import os
import json
import time
import argparse
from src.utils.logging_utils import log_info, log_error, log_success, log_warning

class TranskribusAPIError(Exception):
    """Custom exception for Transkribus API errors"""
    pass

def login(username, password):
    log_info("Logging in to Transkribus", "key")
    login_url = "https://transkribus.eu/TrpServer/rest/auth/login"
    try:
        response = requests.post(login_url, data={'user': username, 'pw': password})
        response.raise_for_status()
        log_success("Login successful", "white_check_mark")
        return response.cookies.get('JSESSIONID')
    except requests.RequestException as e:
        log_error(f"Login failed: {str(e)}", "x")
        raise TranskribusAPIError("Login failed") from e

def upload_image(session_id, collection_id, image_path):
    log_info(f"Uploading image: {image_path}", "arrow_up")
    upload_url = f"https://transkribus.eu/TrpServer/rest/uploads?collId={collection_id}"
    headers = {'Cookie': f'JSESSIONID={session_id}'}
    try:
        with open(image_path, 'rb') as image_file:
            files = {'img': (os.path.basename(image_path), image_file)}
            response = requests.post(upload_url, headers=headers, files=files)
        response.raise_for_status()
        log_success("Image uploaded successfully", "white_check_mark")
        return response.json()['uploadId']
    except (requests.RequestException, IOError) as e:
        log_error(f"Image upload failed: {str(e)}", "x")
        raise TranskribusAPIError("Image upload failed") from e

def process_image(session_id, collection_id, document_id, page_nr, model):
    log_info(f"Processing image with model: {model}", "gear")
    process_url = f"https://transkribus.eu/TrpServer/rest/recognition/{collection_id}/{model}/htrCITlab"
    headers = {'Cookie': f'JSESSIONID={session_id}'}
    data = {'id': document_id, 'pages': str(page_nr)}
    try:
        response = requests.post(process_url, headers=headers, data=data)
        response.raise_for_status()
        log_success("Image processing started", "white_check_mark")
        return response.json()['jobId']
    except requests.RequestException as e:
        log_error(f"Image processing failed to start: {str(e)}", "x")
        raise TranskribusAPIError("Image processing failed to start") from e

def get_job_status(session_id, job_id):
    status_url = f"https://transkribus.eu/TrpServer/rest/jobs/{job_id}"
    headers = {'Cookie': f'JSESSIONID={session_id}'}
    try:
        response = requests.get(status_url, headers=headers)
        response.raise_for_status()
        return response.json()['state']
    except requests.RequestException as e:
        log_error(f"Failed to get job status: {str(e)}", "x")
        raise TranskribusAPIError("Failed to get job status") from e

def get_text_result(session_id, collection_id, document_id, page_nr):
    text_url = f"https://transkribus.eu/TrpServer/rest/collections/{collection_id}/{document_id}/{page_nr}/text"
    headers = {'Cookie': f'JSESSIONID={session_id}'}
    try:
        response = requests.get(text_url, headers=headers)
        response.raise_for_status()
        log_success("Text result retrieved successfully", "white_check_mark")
        return response.json()['text']
    except requests.RequestException as e:
        log_error(f"Failed to retrieve text result: {str(e)}", "x")
        raise TranskribusAPIError("Failed to retrieve text result") from e

def process_with_transkribus(input_dir, config, model):
    log_info(f"Processing images in {input_dir} with Transkribus", "magnifying_glass_tilted_left")
    try:
        session_id = login(config['username'], config['password'])
        collection_id = config['collection_id']

        for image_file in os.listdir(input_dir):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(input_dir, image_file)
                upload_id = upload_image(session_id, collection_id, image_path)
                document_id = upload_id  # In this case, upload_id is the same as document_id
                job_id = process_image(session_id, collection_id, document_id, 1, model)

                # Wait for job to complete
                max_attempts = 30  # Maximum number of attempts (5 minutes)
                for attempt in range(max_attempts):
                    status = get_job_status(session_id, job_id)
                    if status == 'FINISHED':
                        break
                    elif status in ['FAILED', 'CANCELED']:
                        log_error(f"Job failed or was canceled for {image_file}", "x")
                        break
                    if attempt == max_attempts - 1:
                        log_warning(f"Job timed out for {image_file}", "hourglass")
                        break
                    time.sleep(10)  # Wait for 10 seconds before checking again

                if status == 'FINISHED':
                    text_result = get_text_result(session_id, collection_id, document_id, 1)
                    output_file = os.path.join(config['output_dir'], f"{os.path.splitext(image_file)[0]}_ocr.txt")
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(text_result)
                    log_success(f"OCR result saved to {output_file}", "floppy_disk")

        log_success("Transkribus processing completed", "checkmark")
    except TranskribusAPIError as e:
        log_error(f"Transkribus processing failed: {str(e)}", "x")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process images with Transkribus OCR")
    parser.add_argument("input_dir", help="Directory containing input images")
    parser.add_argument("--model", default="Mittelalterliche_Schriften_M2.4", 
                        help="Transkribus HTR model to use (default: %(default)s)")
    parser.add_argument("--config", default="config/config.yaml", 
                        help="Path to the configuration file (default: %(default)s)")
    args = parser.parse_args()

    from src.config import load_config
    config = load_config(args.config)
    process_with_transkribus(args.input_dir, config['transkribus'], args.model)