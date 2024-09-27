import argparse
import base64
import os
from typing import Dict, List, Union
from openai import OpenAI
from jinja2 import Environment, FileSystemLoader
from src.utils.logging_utils import log_info, log_error, log_success, log_warning
from src.models import OCRResult, FolioResponse
from src.config import load_config

def load_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def process_single_image(image_path: str, transkribus_text: str, context: str, config: Dict, model: str, client: OpenAI, template) -> FolioResponse:
    log_info(f"Processing single image: {image_path}", "page_facing_up")
    image_data = load_image(image_path)
    
    with open(config['example_output_path'], 'r') as file:
        example_output = file.read()
    example_image_data = load_image(config['example_image_path'])
    
    prompt = template.render(
        context=context,
        example_output=example_output,
        image_data_1=example_image_data,
        image_data_2=image_data,
        transkribus_text=transkribus_text
    )
    
    messages = [
        {"role": "system", "content": "You are an expert in medieval manuscripts OCR."},
        {"role": "user", "content": prompt}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"}
    )
    
    return FolioResponse.parse_raw(response.choices[0].message.content)

def process_with_openai(transkribus_results: Dict[str, str], config: Dict, model: str, context: str) -> OCRResult:
    log_info(f"Processing with OpenAI using model: {model}", "brain")
    client = OpenAI(api_key=config['api_key'])
    template_env = Environment(loader=FileSystemLoader('prompts'))
    template = template_env.get_template('ocr_cot_prompt.j2')
    
    results = []
    batch_size = 20  # Adjust this based on your needs and API limits
    
    items = list(transkribus_results.items())
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        
        try:
            for image_path, transkribus_text in batch:
                folio_response = process_single_image(image_path, transkribus_text, context, config, model, client, template)
                results.append(folio_response)
                log_success(f"Successfully processed {image_path}", "check_mark")
        
        except Exception as e:
            log_error(f"Error processing batch: {str(e)}", "x")
    
    return OCRResult(folios=results)

def main(input_path: str, model: str, config_path: str, context: str):
    config = load_config(config_path)
    
    if os.path.isfile(input_path):
        # Single file processing
        with open(input_path, 'r', encoding='utf-8') as f:
            transkribus_text = f.read()
        transkribus_results = {input_path: transkribus_text}
    else:
        # Directory processing
        transkribus_results = {}
        for filename in os.listdir(input_path):
            if filename.endswith('_ocr.txt'):
                image_path = os.path.join(input_path, filename.replace('_ocr.txt', '.jpg'))  # Assuming .jpg, adjust if needed
                with open(os.path.join(input_path, filename), 'r', encoding='utf-8') as f:
                    transkribus_results[image_path] = f.read()
    
    results = process_with_openai(transkribus_results, config['openai'], model, context)
    log_info(f"Processed {len(results.folios)} folios", "tada")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process images with OpenAI OCR")
    parser.add_argument("input_path", help="Path to input Transkribus OCR result file or directory containing OCR result files")
    parser.add_argument("--model", choices=["gpt-4o", "gpt-4o-mini"], default="gpt-4o", 
                        help="OpenAI model to use (default: %(default)s)")
    parser.add_argument("--config", default="config/config.yaml", 
                        help="Path to the configuration file (default: %(default)s)")
    parser.add_argument("--context", default="", help="Context information about the book/manuscript")
    args = parser.parse_args()

    main(args.input_path, args.model, args.config, args.context)