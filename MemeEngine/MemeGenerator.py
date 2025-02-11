import random
import tempfile
import pprint
import numpy as np
from pathlib import Path
from typing import Tuple
from PIL import Image, ImageDraw, ImageOps
from PIL.ImageFont import FreeTypeFont

class MemeGenerator:
    """
    A class that generates memes by adding quotes and author text onto images.
    """

    def __init__(self, output_folder: str = './output', input_img_source: str = None,
                 quote: str = '', author: str = '', output_width: int = None,
                 perc_text_width: float = 0.7, font_source: str = 'MemeEngine/fonts/FiraSans-Medium.ttf',
                 font_size: int = 10):
        """
        Initializes MemeGenerator with the provided image and text properties.

        Args:
            output_folder: Directory to save the meme images.
            input_img_source: Path to the input image.
            quote: Text of the quote to add.
            author: Name of the quote's author.
            output_width: Desired width of the output image.
            perc_text_width: The width percentage to which the quote text should scale.
            font_source: Path to the font file.
            font_size: Initial font size for the quote.
        """
        self.output_folder = Path(output_folder)
        self.input_img_source = input_img_source
        self.quote = quote
        self.author = author
        self.output_width = output_width
        self.perc_text_width = perc_text_width
        self.font_source = font_source
        self.font_size = font_size
        self.image = None
        self.font_quote = None
        self.font_author = None
        if self.input_img_source:
            self.load_image(self.input_img_source)

    @property
    def author(self) -> str:
        """
        Returns the formatted author text, prefixed with a dash.
        """
        return f'- {self._author}'

    @author.setter
    def author(self, value: str):
        """
        Sets the author of the quote.
        """
        self._author = value

    def load_image(self, img_source: str):
        """
        Loads an image from the specified path.

        Args:
            img_source: Path to the image to load.
        """
        try:
            self.image = Image.open(img_source)
        except Exception as e:
            raise ValueError(f"Failed to load image from {img_source}: {e}")

    def resize_image(self, output_width: int = None):
        """
        Resizes and crops the image to maintain aspect ratio based on the specified width.

        Args:
            output_width: Desired width for the resized image.

        Raises:
            ValueError: If no output width is provided.
            AttributeError: If the image is not loaded.
        """
        try:
            width = output_width or self.output_width
            if not width:
                raise ValueError("An output width must be specified.")
            
            scale_factor = width / self.image.width
            new_size = (int(self.image.width * scale_factor), int(self.image.height * scale_factor))
            self.image = ImageOps.fit(self.image, new_size)
        except AttributeError as e:
            raise AttributeError("Image must be loaded before resizing.") from e
        except Exception as e:
            raise ValueError(f"Failed to resize image: {e}")

    def set_fonts(self, size: int, author_size_decrease: float = 0.20):
        """
        Sets the font sizes.

        Args:
            size: Font size for the text.
            author_size_decrease: Percentage to reduce the font size of the author text.

        Raises:
            ValueError: If the author_size_decrease is out of range.
        """
        try:
            if not (0.1 <= author_size_decrease <= 0.9):
                raise ValueError("author_size_decrease must be between 0.10 and 0.90.")

            self.font_quote = FreeTypeFont(self.font_source, size)
            self.font_author = FreeTypeFont(self.font_source, int(size * (1 - author_size_decrease)))
        except Exception as e:
            raise ValueError(f"Failed to set font sizes: {e}")

    def adjust_font_size_based_on_text(self):
        """
        Adjusts the font size dynamically based on the width of the text.

        This method ensures that the text will not exceed the desired width on the image.
        """
        try:
            self.set_fonts(self.font_size)
            while self.font_quote.getlength(self.quote) < self.image.width * self.perc_text_width:
                self.set_fonts(self.font_quote.size + 1)
        except Exception as e:
            raise ValueError(f"Failed to adjust font size: {e}")

    def generate_random_position(self) -> Tuple[int, int]:
        """
        Generates a random position for the text placement.

        Returns:
            Tuple: A random (x, y) coordinate within the image bounds.
        """
        try:
            box_padding = np.append(self.font_quote.getbbox(self.quote, anchor='rb')[:2],
                                     np.array(self.font_author.getbbox(self.author, anchor='rt')[2:])) * -1
            x_min, y_min, x_max, y_max = tuple(np.array(((0, 0), self.image.size)).flatten() + box_padding)
            return random.randint(x_min, x_max), random.randint(y_min, y_max)
        except Exception as e:
            raise ValueError(f"Failed to generate random position: {e}")

    def add_text_to_image(self, position: Tuple[int, int] = None, output_width: int = None,
                          scale_text: bool = True, random_position: bool = True):
        """
        Adds the quote and author text to the image at a specified position.

        Args:
            position: Position to place the text.
            output_width: The width to resize the image.
            scale_text: Whether to scale the text to fit the image.
            random_position: Whether to generate a random position for the text.

        Raises:
            ValueError: If neither position nor random_position is provided.
        """
        try:
            if not position and not random_position:
                raise ValueError("You must define a position or set random_position to True.")
            if position and random_position:
                raise ValueError("Cannot specify both position and random_position.")

            if scale_text:
                self.adjust_font_size_based_on_text()
            if random_position:
                position = self.generate_random_position()
            if output_width:
                self.resize_image(output_width=output_width)

            draw = ImageDraw.Draw(self.image)
            draw.text(position, self.quote, font=self.font_quote, anchor='rb', fill=(250, 240, 255))
            draw.text(position, self.author, font=self.font_author, anchor='rt', 
                      fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        except Exception as e:
            raise ValueError(f"Failed to add text to image: {e}")

    def save_meme(self) -> str:
        """
        Saves the generated meme image to the output folder.

        Returns:
            str: Path to the saved meme image.
        """
        try:
            self.output_folder.mkdir(parents=True, exist_ok=True)
            output_file = tempfile.NamedTemporaryFile(dir=self.output_folder.name, prefix='meme_', suffix='.jpg').name
            self.image.save(output_file)
            return str(self.output_folder / Path(output_file).name)
        except Exception as e:
            raise ValueError(f"Failed to save meme image: {e}")

    def make_meme(self, img_source: str, quote_text: str, quote_author: str, width: int = 500) -> str:
        """
        Creates a meme by overlaying a quote and author on an image and saving it.

        Args:
            img_source: Path to the image to use.
            quote_text: Quote text to add to the image.
            quote_author: Author of the quote.
            width: Desired width of the output image.

        Returns:
            str: Path to the saved meme.
        """
        try:
            self.load_image(img_source)
            self.quote = quote_text
            self.author = quote_author

            self.add_text_to_image(output_width=width, scale_text=True)
            return self.save_meme()
        except Exception as e:
            raise ValueError(f"Failed to create meme: {e}")


if __name__ == '__main__':
    try:
        meme_url = MemeGenerator().make_meme(r'_data/photos/dog/xander_3.jpg', 
                                                quote_text='Example Quote', 
                                                quote_author='Author Text')
        pprint.pprint(meme_url)
        print('Meme created successfully.')
    except Exception as e:
        print(f"Error creating meme: {e}")
