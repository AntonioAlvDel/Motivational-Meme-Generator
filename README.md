# Meme Generator 🐶

Meme Generator is a final project for the **Intermediate Python Nanodegree** program at Udacity. This project applies advanced Python techniques, including object-oriented programming and modular development, to create an application that allows users to generate memes by overlaying text onto images. It also implements best practices in module creation and dependency management, as covered in the course's "Building Modules" section.

## Features

- **Quote Extraction:** Extracts quotes from `.txt`, `.csv`, `.docx`, and `.pdf` files.
- **Meme Generation:** Dynamically positions and formats text on images.
- **Random Selection:** Selects quotes and images randomly if no specific input is provided.
- **Web Interface:** Built with Flask for user-friendly meme generation.
- **Command-Line Tool:** Allows meme creation with specified inputs.

## Prerequisites

- Python 3.8+
- Pip

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd meme-generator
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web Interface
To start the web application, run:
```bash
python app.py
```
Then, open `http://127.0.0.1:5000/` in your browser to generate memes interactively.

### Command-Line Tool
Generate a meme by specifying the image path, quote, and author:
```bash
python meme.py --path <image_path> --quote "Your Quote Here" --author "Author Name"
```

## Project Structure

- **MemeEngine:** Handles image processing and text overlay.
- **QuoteEngine:** Ingests and models quotes from various file formats.

## Autor
Antonio Alvarez Delgado
* [Linkedin](https://www.linkedin.com/in/antonio-alvarez-delgado-0b46451b3/)
