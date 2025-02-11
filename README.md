# Meme Generator

## Overview
Meme Generator is a Python-based application that allows users to create memes by overlaying text onto images. It supports multiple file formats for quote extraction, including `.txt`, `.csv`, `.docx`, and `.pdf`. The application provides a command-line interface and a web-based front end using Flask.

## Features
- Extract quotes from `.txt`, `.csv`, `.docx`, and `.pdf` files.
- Generate memes with dynamically positioned and formatted text.
- Randomly select quotes and images if not provided.
- Web-based interface for user-generated memes.
- Command-line tool to generate memes from specified inputs.

## Setup & Installation

### Prerequisites
- Python 3.8+
- Pip

### Dependencies
To install the required dependencies, run:
```bash
pip install -r requirements.txt
```

### Running the Application
To run the web-based application:
```bash
python app.py
```

To generate a meme using the command-line tool:
```bash
python meme.py --path <image_path> --quote "Your Quote Here" --author "Author Name"
```

## Sub-Modules
### MemeEngine
- **MemeGenerator**: Handles image processing, text formatting, and meme creation.
  - `make_meme(img_path, quote_text, quote_author, width=500)`: Generates a meme image with the given text and author.

### QuoteEngine
- **QuoteModel**: Represents a quote with text and an author.
- **Ingestor**: Abstract base class for different file parsers.
  - **IngestorTXT**: Handles `.txt` files.
  - **IngestorCSV**: Handles `.csv` files.
  - **IngestorDOC**: Handles `.docx` files.
  - **IngestorPDF**: Handles `.pdf` files using `PyMuPDF`.

### Web Interface
- Built with Flask.
- Provides a random meme generator.
- Allows users to create custom memes.

## Example Usage
### Command-Line Example
```bash
python meme.py --path "./_data/photos/dog/xander_1.jpg" --quote "Life is beautiful" --author "Anonymous"
```

### Web-Based Example
1. Run `python app.py`
2. Open `http://127.0.0.1:5000/` in your browser.
3. Generate a random meme or create a custom one using the form.

## License
This project is licensed under the MIT License.

