import argparse
import os
import random
from MemeEngine.MemeGenerator import MemeGenerator
from QuoteEngine import QuoteModel


def generate_meme(path=None, quote=None, author=None):
    """Generate a meme given a path and a quote."""
    img = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, _, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]
            print(imgs)

        img = random.choice(imgs)
        print(f'Selected image: {img}')
    else:
        img = path
        print(f'Selected image: {img}')

    if quote is None:
        quote_files = [
            './_data/DogQuotes/DogQuotesTXT.txt',
            './_data/DogQuotes/DogQuotesDOCX.docx',
            './_data/DogQuotes/DogQuotesPDF.pdf',
            './_data/DogQuotes/DogQuotesCSV.csv'
        ]
        quotes = []
        for f in quote_files:
            quotes.extend(QuoteModel.Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author is required')
        quote = QuoteModel.QuoteModel(quote, author)

    meme = MemeGenerator()
    meme_path = meme.make_meme(img, quote.quote, quote.author)
    return meme_path


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Meme script.')
    parser.add_argument('--path', type=str, help='Path to an image file.')
    parser.add_argument('--quote', type=str, help='Quote body to add to the image.')
    parser.add_argument('--author', type=str, help='Quote author to add to the image.')
    args = parser.parse_args()

    try:
        meme_path = generate_meme(args.path, args.quote, args.author)
        print(f'Meme successfully created at: {meme_path}')
    except Exception as e:
        print(f'Error: {e}')
