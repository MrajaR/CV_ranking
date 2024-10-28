from .document_processing import DocumentProcessing
from .retriever_manager import RetrieverManager
from .vector_store_manager import VectorStoreManager

import chromadb
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import json
import sys
import os

# Add the path to the parent directory containing the config module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config

class CandidateRanker:
    def __init__(self):
        """
        Initializes the CandidateRanker object.

        Retrieves the LLM and prompt template from the Config module, creates a DocumentProcessing object, a VectorStoreManager object, and a RetrieverManager object. The VectorStoreManager object is initialized with the embeddings model specified in the Config module.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: If there is an error initializing the CandidateRanker object.
        """
        try:
            self.client = chromadb.PersistentClient(path=Config.CHROMADB_DIRECTORY)
            self.embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL_NAME)
            self.document_processor = DocumentProcessing(llm=Config.get_llm(), prompt_template=Config.get_prompt_template())
            self.vector_store_manager = VectorStoreManager(embeddings=self.embeddings)
            self.retriever_manager = RetrieverManager(vector_store=self.vector_store_manager.vector_store)
        except Exception as e:
            print(f"Error initializing CandidateRanker: {str(e)}")

    def process_cv(self, file_path, file_name):
        """
        Processes a CV by reading, summarizing, storing the summary, and adding it to a vector store.

        Args:
            file_path (str): The path to the CV file to be processed.
            file_name (str): The name of the CV file being processed.

        This method reads a CV from the specified file path, generates a summary of the CV text,
        and creates a document object with the summary and metadata. The summary is saved to a
        JSON file, and the document is added to a vector store for further retrieval operations.

        Exceptions are handled to manage file reading/writing errors and issues during document
        addition to the vector store.
        """
        try:
            # Read and process the CV
            cv_text = self.document_processor.read_pdf(file_path)
            candidate_summary = self.document_processor.create_summary(cv_text)
            documents = Document(page_content=candidate_summary, metadata={'filename': file_name})

            print('Document created')

            # Save summary to JSON file
            try:
                with open(Config.JSON_FILE_NAME, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {}  # If file is empty or invalid, start with an empty dictionary

                    # Update the dictionary with the new entry
                    data[documents.metadata['filename']] = candidate_summary

                    # Move the pointer to the beginning to overwrite with updated data
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()  # Remove any leftover content if the new JSON is smaller

            except (FileNotFoundError, IOError) as e:
                print(f"Error with JSON file handling: {str(e)}")

            # Add the processed document to the vector store
            try:
                self.vector_store_manager.add_documents([documents])
                print('Document added to vector store')
            except Exception as e:
                print(f"Error adding document to vector store: {str(e)}")

        except Exception as e:
            print(f"Error processing CV: {str(e)}")

    def search_candidate(self, query):
        """
        Searches for candidates based on a query.

        This method reads the CV summaries from a JSON file, performs a hybrid search using
        both keyword and semantic search, and returns the search results.

        Args:
            query (str): The query text to search the candidates with.

        Returns:
            list: A list of candidate matches with their relevance score. If there is an error
                  during the search, an empty list is returned.

        Raises:
            FileNotFoundError: If the JSON file containing the CV summaries does not exist.
            IOError: If there is an error reading the JSON file.
            Exception: If there is an error during the search.
        """
        try:
            # Load cv_summary from the JSON file
            with open(Config.JSON_FILE_NAME, 'r', encoding='utf-8') as f:
                try:
                    cv_summary = json.load(f)
                except json.JSONDecodeError:
                    print("Error reading JSON file, it might be empty or invalid.")
                    return []

            print(cv_summary)
            print(type(cv_summary))

            # Perform hybrid search
            try:
                self.retriever_manager.hybrid_search(cv_summary)
                results = self.retriever_manager.search(query)
                return results
            except Exception as e:
                print(f"Error during candidate search: {str(e)}")
                return []

        except (FileNotFoundError, IOError) as e:
            print(f"Error loading JSON file: {str(e)}")
            return []
