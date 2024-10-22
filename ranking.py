from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import pytesseract
import requests
from dotenv import load_dotenv
import os
from pdf2image import convert_from_path
import concurrent.futures
import numpy as np
from numpy.linalg import norm

load_dotenv()

class CVRanking:
    def __init__(self):
        self.model_id = "sentence-transformers/all-mpnet-base-v2"
        self.hf_token = os.getenv('HF_API_KEY')

        self.groq_model_id = "llama-3.1-70b-versatile"
        self.groq_token = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(groq_api_key=self.groq_token, model_name=self.groq_model_id)

        self.generate_summary_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an assistant skilled at summarizing CVs by highlighting key qualifications, education, skiils, and estimating the applicant's years of experience. Ensure the summary is brief, focusing on relevant qualifications based on the provided CV."
            ),
            (
                "human", 
                "{source}\nPlease summarize the applicant's qualifications, skills, education, and estimate their years of experience"
            )
        ]
        )
        
        self.generate_summary_chain = self.generate_summary_template | self.llm

        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{self.model_id}"
        self.headers = {"Authorization": f"Bearer {self.hf_token}"}

        self.user_txt_folder = 'cv_candicates_text'
        os.makedirs(self.user_txt_folder, exist_ok=True)

    def generate_embeddings(self, texts):
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": texts, "options":{"wait_for_model":True}})
        return response.json()
    
    def ocr_page(self, page):
        return pytesseract.image_to_string(page)

    def extract_cv(self, document_path, filename):
        pdf_pages = convert_from_path(document_path, dpi=350)

        text_file_path = os.path.join(self.user_txt_folder, f'{filename}.txt')

                    # Use concurrent futures for parallel processing
        with concurrent.futures.ThreadPoolExecutor() as executor:
                        # Process pages in parallel and get OCR text for each page
            results = executor.map(self.ocr_page, pdf_pages)

            # Write the extracted text to a file
            # with open(text_file_path, 'a', encoding='utf-8') as f:
            #     for text in results:
            #         f.write(text + "\n")
            extracted_cv_string = ""

            for text in results:
                extracted_cv_string+=text+'\n'

            cv_summary = self.generate_summary_chain.invoke({"source":extracted_cv_string}).content
            print('berhasil generate summary dari CV')
            with open(text_file_path, 'w') as f:
                f.write(cv_summary)

    def calculate_cosine_similarity(self, applicant_resume, expected_competency):
        # Hitung norm dari kedua vektor
        applicant_norm = norm(applicant_resume)
        competency_norm = norm(expected_competency)

        # Cek jika norm salah satu vektor adalah nol untuk menghindari pembagian dengan nol
        if applicant_norm == 0 or competency_norm == 0:
            print("Error: Salah satu vektor memiliki norm 0, cosine similarity tidak dapat dihitung.")
            return 0  # Atau nilai lain sesuai kebutuhan

        # Hitung cosine similarity
        cosine = np.dot(applicant_resume, expected_competency) / (applicant_norm * competency_norm)
        return cosine


    def rank_candidate(self, expected_competency):
        scores = {}

        # Generate embedding for the expected competency text
        expected_competency_embedding = self.generate_embeddings(expected_competency)

        try:
            # Loop through all candidate CV files, generate embeddings, and calculate cosine similarity
            for cv_candidate in os.listdir(self.user_txt_folder):
                cv_candidate_file_path = os.path.join(self.user_txt_folder, cv_candidate)
                with open(cv_candidate_file_path, 'r') as f:
                    candidate_desc = f.read()

                # Generate embedding for the candidate's resume text
                candidate_desc_embedding = self.generate_embeddings(candidate_desc)
                print("berhasil generate embedding")
                print(candidate_desc_embedding)

                score = self.calculate_cosine_similarity(candidate_desc_embedding, expected_competency_embedding)
                print("berhasil mendapatkan score")
                score =  round(score * 100, 2)
                print(f'Cosine similarity score for applicant named {cv_candidate} is {score}')
                scores[cv_candidate] = f"{score}%"


        except Exception as e:
            print(f'Error in calculating cosine similarity: {e}')

        # Sort candidates by score (descending) to rank them
        sorted_candidates = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        # Create a dictionary to represent DataFrame-like structure
        ranked_candidates_dict = {
            'Ranking': [rank + 1 for rank in range(len(sorted_candidates))],
            'Candidate': [candidate for candidate, score in sorted_candidates],
            'Score': [score for candidate, score in sorted_candidates]
        }

        return ranked_candidates_dict