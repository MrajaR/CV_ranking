from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

class Config:
    # ChromaDB configurations
    CHROMADB_DIRECTORY = 'CV_CHROMADB'
    CHROMA_COLLECTION_NAME = 'cv_collection'
    CHROMA_COLLECTION_METADATA = {'hnsw:space': 'cosine'}

    # Model configurations
    LLM_API_KEY_ENV = os.getenv('GROQ_API_KEY')
    LLM_MODEL_NAME = 'Llama-3.1-70b-Versatile'
    EMBEDDING_MODEL_NAME = 'sentence-transformers/all-MiniLM-L12-v2'

    # Prompt template
    PROMPT_TEMPLATE_MESSAGES = [  
        ('system',
         'You are an assistant that is very proficient at highlighting key qualifications, education, skills, certifications, and estimating the applicant\'s years of experience. Also, determine if they are already graduated or not. Ensure the summary is brief, focusing on relevant qualifications based on the provided CV.'
        ),
        ('human', "This is the curriculum vitae text:\n\n{text}")
    ]
    
    # Folder
    CV_CANDIDATE_DIRECTORY = 'user_cv_pdf'

    # JSON file to store candidate summaries
    JSON_FILE_NAME = 'FOR_BM25/cv_summary.json'

    @classmethod
    def get_prompt_template(cls):
        """
        Returns a ChatPromptTemplate object based on the PROMPT_TEMPLATE_MESSAGES
        class attribute.

        Returns:
            ChatPromptTemplate: A ChatPromptTemplate object.

        Raises:
            Exception: If there is an error initializing the ChatPromptTemplate.
        """
        try:
            return ChatPromptTemplate.from_messages(cls.PROMPT_TEMPLATE_MESSAGES)
        except Exception as e:
            print(f"Error creating prompt template: {str(e)}")
            raise

    @classmethod
    def get_llm(cls):
        """
        Returns a ChatGroq object initialized with the API key and model name
        specified in the class attributes.

        Returns:
            ChatGroq: An instance of the ChatGroq class.

        Raises:
            Exception: If there is an error initializing the ChatGroq object.
        """
        try:
            if cls.LLM_API_KEY_ENV is None:
                raise ValueError("GROQ_API_KEY is not set in environment variables.")
            return ChatGroq(api_key=cls.LLM_API_KEY_ENV, model=cls.LLM_MODEL_NAME)
        except ValueError as ve:
            print(f"Configuration error: {str(ve)}")
            raise
        except Exception as e:
            print(f"Error initializing language model: {str(e)}")
            raise
