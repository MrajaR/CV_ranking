from langchain_chroma import Chroma
from uuid import uuid4

class VectorStoreManager:
    def __init__(self, embeddings):
        """
        Initializes the VectorStoreManager with the given embeddings.

        Args:
            embeddings (HuggingFaceEmbeddings): The embeddings model to use for the vector store.

        Raises:
            Exception: If there is an error initializing the VectorStoreManager.
        """
        try:
            self._vector_store = self.init_vector_store(embeddings)
        except Exception as e:
            print(f"Error initializing VectorStoreManager: {str(e)}")

    def init_vector_store(self, embeddings):
        """
        Initializes the vector store with the given embeddings.

        Args:
            embeddings (HuggingFaceEmbeddings): The embeddings model to use for the vector store.

        Returns:
            Chroma: The initialized vector store.

        Raises:
            Exception: If there is an error initializing the vector store.
        """
        try:
            return Chroma(
                persist_directory='CV_CHROMADB',
                collection_name='cv_collection',
                embedding_function=embeddings,
                collection_metadata={'hnsw:space': 'cosine'}
            )
        except Exception as e:
            print(f"Error initializing vector store: {str(e)}")
            return None

    @property
    def vector_store(self):
        """
        The vector store that is used for storing and retrieving documents.

        Returns:
            Chroma: The vector store.

        Raises:
            ValueError: If the vector store is not initialized.
        """

        if self._vector_store is None:
            raise ValueError("Vector store not initialized.")
        return self._vector_store

    def add_documents(self, document):
        """
        Adds the given documents to the vector store.

        Args:
            document (list): A list of Document objects to be added to the vector store.

        Raises:
            Exception: If there is an error adding the documents to the vector store.
        """
        try:
            uuids = [str(uuid4()) for _ in range(len(document))]
            self._vector_store.add_documents(documents=document, ids=uuids)
            print('Documents successfully added to vector store.')
        except Exception as e:
            print(f"Failed to add documents to vector store: {str(e)}")
