# Improved OCR with Transkribus and OpenAI

This project aims to enhance the OCR capabilities of the Transkribus model by combining it with an OpenAI model. It leverages the strengths of both systems to create more accurate transcriptions of historical documents.

## Project Overview

The project consists of a pipeline with the following main steps:
1. Preprocessing of document pages
2. OCR processing with Transkribus
3. Improvement of OCR results with OpenAI

## Prerequisites

- Python 3.8 or higher
- uv (recommended) or pip
- Transkribus account
- OpenAI API key
- Poppler (for PDF to image conversion)

## Installation

1. Install Poppler:
   - On Ubuntu or Debian:
     ```
     sudo apt-get install poppler-utils
     ```
   - On macOS with Homebrew:
     ```
     brew install poppler
     ```
   - On Windows:
     Download the Poppler binaries and add the path to the PATH environment variable.

2. Clone the repository:
   ```
   https://github.com/nicolas-werner/improving-ocr-with-genai
   cd improving-ocr-with-genai
   ```

3. Set up the virtual environment with uv:
   ```
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. Install dependencies:
   ```
   uv pip install -r requirements.txt
   ```

   Alternatively, if you want to use pip:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the example configuration file:
   ```
   cp config/config_template.yaml config/config.yaml
   ```

2. Edit `config/config.yaml` and add your Transkribus and OpenAI credentials. You can use `config_template.yaml` as a reference for the structure and required fields.

Note: The `config.yaml` file is listed in `.gitignore` to prevent sensitive information from being accidentally uploaded to the repository.

## Usage

1. Run the entire pipeline:

   ```
   python main.py
   ```

   This executes all steps of the pipeline, including preprocessing, Transkribus OCR, and OpenAI improvement.

2. Run only the Transkribus OCR part:

   ```
   python -m src.ocr.transkribus_api /path/to/input/images --model Medieval_Scripts_M2.4
   ```

   Optional arguments:
   - `--model`: Specifies the Transkribus HTR model to use (default: Medieval_Scripts_M2.4)
   - `--config`: Path to the configuration file (default: config/config.yaml)

   Example with all options:
   ```
   python -m src.ocr.transkribus_api /path/to/input/images --model CustomModel --config /path/to/custom/config.yaml
   ```

This flexibility allows you to either run the entire OCR pipeline or just the Transkribus part for specific tasks or tests.

## Project Structure

The project is structured as follows:
```
src/
├── config/ # Configuration files
│   └── config.yaml
├── prompts/ # Prompt templates
│   └── ocr_cot_prompt.j2
├── notebooks/ # Jupyter Notebooks
│   └── experiments.ipynb
├── main.py # Main entry point
├── models.py # Pydantic models
├── ocr_pipeline.py # OCR pipeline
├── requirements.txt # Dependencies
└── README.md
```


