from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_core.documents import Document

class RetrieverManager:
    def __init__(self, vector_store, keyword_retriever_k=2, ensemble_weights=[0.5, 0.5]):
        """
        Initializes the RetrieverManager with a vector store, keyword retriever, and ensemble weights.

        Args:
            vector_store: The vector store for semantic search.
            keyword_retriever_k (int, optional): The number of keyword search results to retrieve. Defaults to 2.
            ensemble_weights (list, optional): Weights to balance the keyword and semantic retrievers in the ensemble. Defaults to [0.5, 0.5].

        Raises:
            Exception: If there is an error initializing the RetrieverManager.
        """
        try:
            self.vector_store = vector_store
            self.keyword_retriever_k = keyword_retriever_k
            self.ensemble_weights = ensemble_weights
            self.retriever = None
        except Exception as e:
            print(f"Error initializing RetrieverManager: {str(e)}")

    def keyword_retriever(self, cv_summary):
        """
        Creates a BM25 keyword retriever from the given CV summaries.

        Args:
            cv_summary (dict): Dictionary containing CV summaries as values and filenames as keys.

        Returns:
            BM25Retriever: The BM25 retriever for keyword search, or None if an error occurs.
        """
        try:
            bm25_retriever = BM25Retriever.from_documents(
                [Document(page_content=value, metadata={"filename": key}) for key, value in cv_summary.items()]
            )
            print('BM25 retriever created')
            bm25_retriever.k = self.keyword_retriever_k
            return bm25_retriever
        except Exception as e:
            print(f"Error creating BM25 retriever: {str(e)}")
            return None

    def hybrid_search(self, cv_summary):
        """
        Initializes an ensemble retriever combining keyword and semantic searches.

        This method creates a BM25 keyword retriever from the provided CV summaries
        and a semantic retriever from the vector store. It then combines these
        retrievers into an EnsembleRetriever using specified weights.

        Args:
            cv_summary (dict): Dictionary containing CV summaries as values and filenames as keys.

        Raises:
            ValueError: If the keyword retriever initialization fails.
            Exception: If there is an error during the hybrid search initialization.
        """
        try:
            keyword_search = self.keyword_retriever(cv_summary)
            if keyword_search is None:
                raise ValueError("Keyword retriever initialization failed.")

            semantic_search = self.vector_store.as_retriever(search_kwargs={"k": self.keyword_retriever_k})
            print('Semantic and keyword search ready')
            
            self.retriever = EnsembleRetriever(
                retrievers=[keyword_search, semantic_search], 
                weights=self.ensemble_weights
            )
            print('Ensemble retriever ready')
        except ValueError as ve:
            print(f"ValueError during hybrid search: {str(ve)}")
        except Exception as e:
            print(f"Error during hybrid search: {str(e)}")

    def search(self, query):
        """
        Searches for relevant documents based on a query.

        This method takes a query string as input and uses the ensemble retriever (initialized
        by hybrid_search) to retrieve the most relevant documents based on keyword and semantic
        search. If the retriever is not initialized, a ValueError is raised.

        Args:
            query (str): The query string to search for relevant documents.

        Returns:
            list: A list of documents with relevance scores. If there is an error during the search,
                  an empty list is returned.

        Raises:
            ValueError: If the retriever is not initialized.
        """
        if not self.retriever:
            raise ValueError("Retriever not initialized. Call hybrid_search first.")
        
        try:
            print('Trying to get relevant documents')
            return self.retriever.invoke(query)
        except Exception as e:
            print(f"An error occurred during search: {e}")
            return []
