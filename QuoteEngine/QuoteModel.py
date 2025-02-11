import abc
import pprint
import re
import docx
import pandas as pd
import fitz 

class QuoteModel:
    """
    A model representing a quote along with its author.
    """

    def __init__(self, quote: str, author: str):
        """
        Initializes a QuoteModel instance.

        Args:
            quote (str): The quote text.
            author (str): The author of the quote.
        """
        self.quote = quote
        self.author = author

    def __repr__(self):
        """
        Provides a string representation of the QuoteModel instance.

        Returns:
            str: A string representing the quote and its author.
        """
        return f'"{self.quote}" - {self.author}'


class IngestorInterface(abc.ABC):
    """
    Abstract interface defining the structure for different file ingestors.
    """

    @classmethod
    def can_ingest(cls, source: str) -> bool:
        """
        Checks if the file extension can be processed.

        Args:
            source (str): The file source to check.

        Returns:
            bool: Returns True if the file extension is accepted, otherwise False.
        """
        print(cls.input_extension(source))
        return cls.input_extension(source) in cls.allowed_extensions

    @classmethod
    @abc.abstractmethod
    def parse(cls, source: str) -> list[QuoteModel]:
        """
        Abstract method that must be implemented by subclasses to process the file.

        Args:
            source (str): The source to the file to process.
        """
        pass

    @classmethod
    def input_extension(cls, source: str) -> str:
        """
        Extracts the file extension from the file source.

        Args:
            source (str): The file source to extract the extension from.

        Returns:
            str: The file extension in lowercase.
        """
        return source.split('.')[-1].lower()

    @classmethod
    def clean_data(cls, text: str) -> str:
        """
        Cleans the text by removing unwanted characters.

        Args:
            text (str): The text to clean.

        Returns:
            str: The cleaned text.
        """
        remove_chars = r"[()\"#/@;<>{}`+=~|.!?,]"
        return ''.join(filter(str.isprintable, re.sub(remove_chars, "", text).strip()))


class DocxIngestor(IngestorInterface):
    """
    Handles DOC files to extract quotes and authors.
    """
    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, source: str):
        """
        Processes a DOCX file to extract quotes and authors.

        Args:
            source (str): The source to the DOCX file.

        Returns:
            list: A list of QuoteModel instances containing the extracted quotes.
        """
        if not cls.can_ingest(source):
            raise ValueError(f"File not processed - {source}")

        try:
            document = docx.Document(source)
            return [
                QuoteModel(
                    quote=cls.clean_data(paragraph.text.split("-")[0]),
                    author=cls.clean_data(paragraph.text.split("-")[1])
                )
                for paragraph in document.paragraphs if paragraph.text
            ]
        except Exception as e:
            raise ValueError(f"Error while processing DOCX: {e}")


class CSVIngestor(IngestorInterface):
    """
    Handles CSV files to extract quotes and authors.
    """
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, source: str):
        """
        Processes a CSV file to extract quotes and authors.

        Args:
            source (str): The source to the CSV file.

        Returns:
            list: A list of QuoteModel instances.
        """
        if not cls.can_ingest(source):
            raise ValueError(f"File not processed - {source}")

        try:
            df = pd.read_csv(source)
            return list(df.apply(lambda row: QuoteModel(quote=row.body, author=row.author), axis=1))
        except Exception as e:
            raise ValueError(f"Error while processing CSV: {e}")


class PDFIngestor(IngestorInterface):
    """
    Handles PDF files to extract quotes and authors.
    """
    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, source: str):
        """
        Processes a PDF file.

        Args:
            source (str): The source to the PDF file.

        Returns:
            list: A list of QuoteModel instances.

        Raises:
            ValueError: If there is an error processing the PDF file.
        """
        if cls.can_ingest(source) is False:
            raise ValueError(f"File not processed: {source}")

        extracted_quotes = []

        try:
            with fitz.open(source) as document:
                for page in document:
                    for line in page.get_text("text").split("\n"):
                        elements = line.strip().split("-")
                        if len(elements) < 2:
                            continue
                        extracted_quotes.append(
                            QuoteModel(quote=cls.clean_data(elements[0]), author=cls.clean_data(elements[1]))
                        )

            return extracted_quotes

        except Exception as error:
            raise ValueError(f"Error occurred while processing PDF: {error}")


class TextIngestor(IngestorInterface):
    """
    Handles TXT files to extract quotes and authors.
    """
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, source: str):
        """
        Processes a TXT file.

        Args:
            source (str): The source to the TXT file.

        Returns:
            list: A list of QuoteModel instances.
        """
        if cls.can_ingest(source) is False:
            raise ValueError(f"File not processed: {source}")

        extracted_quotes = []

        try:
            with open(source, 'r', encoding="utf-8-sig") as file:
                for line in file:
                    cleaned_line = cls.clean_data(line)
                    if not cleaned_line:
                        continue

                    elements = cleaned_line.split("-")
                    if len(elements) < 2:
                        continue

                    extracted_quotes.append(
                        QuoteModel(quote=cls.clean_data(elements[0]), author=cls.clean_data(elements[1]))
                    )

            return extracted_quotes
        except Exception as e:
            raise ValueError(f"Error while processing TXT: {e}")


class Ingestor(IngestorInterface):
    """
    Main ingestor class that determines which ingestor to use.
    """
    @classmethod
    def parse(cls, source: str):
        """
        Determines which ingestor class to use based on the file extension.

        Args:
            source (str): The source to the file to process.

        Returns:
            list: A list of QuoteModel instances.

        Raises:
            Exception: If no suitable ingestor is found.
        """
        extension = cls.input_extension(source)

        if extension == 'csv':
            ingestor = CSVIngestor
        elif extension == 'docx':
            ingestor = DocxIngestor
        elif extension == 'txt':
            ingestor = TextIngestor
        elif extension == 'pdf':
            ingestor = PDFIngestor
        else:
            raise Exception('Incorrect extension. Only CSV, DOCX, TXT and PDF.')

        print(f'Selected {ingestor}')
        return ingestor.parse(source)


if __name__ == '__main__':
    """
    Main execution block for parsing.
    """
    archivos = [
        'DogQuotesCSV.csv',
        'DogQuotesTXT.txt',
        'DogQuotesPDF.pdf',
        'DogQuotesDOCX.docx'
    ]

    ingestor = Ingestor()
    for archivo in archivos:
        try:
            quotes = ingestor.parse(f'_data/DogQuotes/{archivo}')
            pprint.pprint(quotes)
        except ValueError as e:
            print(f"Error processing file {archivo}: {e}")
        except Exception as e:
            print(f"Unexpected error with file {archivo}: {e}")

