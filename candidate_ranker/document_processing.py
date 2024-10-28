from PyPDF2 import PdfReader
from langchain_core.documents import Document
import json


class DocumentProcessing:
    def __init__(self, prompt_template, llm):
        """
        Initializes the DocumentProcessing object.

        Args:
            prompt_template (ChatPromptTemplate): The prompt template to use for generating summaries.
            llm (ChatLLM): The large language model to use for generating summaries.

        Raises:
            Exception: If there is an error initializing the DocumentProcessing object.
        """
        try:
            self.prompt_template = prompt_template
            self.llm = llm
        except Exception as e:
            print(f"Error initializing DocumentProcessing: {str(e)}")

    def read_pdf(self, file_path):
        """
        Reads a PDF file and extracts all the text from it.

        Args:
            file_path (str): The path to the PDF file to be read.

        Returns:
            str: The extracted text if the file is read successfully, otherwise an empty string.

        Raises:
            FileNotFoundError: If the file is not found.
            Exception: If there is an error reading or processing the PDF file.
        """
        all_text = ""

        try:
            with open(file_path, 'rb') as pdf_file:
                # Create a PDF reader object
                try:
                    pdf_reader = PdfReader(pdf_file)
                except Exception as e:
                    print(f"Error reading the PDF file: {str(e)}")
                    return ""

                # Loop through all the pages
                for page_num in range(len(pdf_reader.pages)):
                    try:
                        # Extract text from each page
                        page = pdf_reader.pages[page_num]
                        all_text += page.extract_text()
                    except Exception as e:
                        print(f"Error extracting text from page {page_num}: {str(e)}")

            # Generate a summary after successfully reading the text
            summary = self.create_summary(all_text)
            return summary

        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return ""
        except Exception as e:
            print(f"Error opening or processing the PDF file: {str(e)}")
            return ""

    def create_summary(self, text):
        """
        Generates a summary of the provided text.

        The summary is generated using the LLM and prompt template provided to the
        DocumentProcessing object. The summary is returned as a string.

        Args:
            text (str): The text to be summarized.

        Returns:
            str: A summary of the provided text. If there is an error during summary
                 generation, an empty string is returned.

        Raises:
            Exception: If there is an error during summary generation.
        """
        try:
            summary = self.prompt_template | self.llm
            return summary.invoke({"text": text}).content
        except Exception as e:
            print(f"Error creating summary: {str(e)}")
            return ""