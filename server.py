from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from candidate_ranker import CandidateRanker
from config import Config
import logging
import os

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': '*'}})
app.logger.setLevel(logging.ERROR)

processor = CandidateRanker()

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return jsonify({'error': f'Failed to load index page: {str(e)}'}), 500

@app.route('/process-uploaded_cv', methods=['POST'])
def process_uploaded_cv():
    try:
        if 'file' not in request.files:
            return jsonify({'botResponse': 'Tolong upload file PDF'}), 400

        file = request.files['file']
        file_path = os.path.join(Config.CV_CANDIDATE_DIRECTORY, file.filename)

        if file.filename in os.listdir(Config.CV_CANDIDATE_DIRECTORY):
            return jsonify({'Response': 'File already exists'}), 400

        file.save(file_path)
        processor.process_cv(file_path, file.filename)


        return jsonify({'Response': 'File uploaded and processed'}), 200

    except FileNotFoundError:
        return jsonify({'error': 'Directory not found for saving the file'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to process uploaded CV: {str(e)}'}), 500

@app.route('/rank-applicants', methods=['POST'])
def rank_applicants():
    try:
        user_prompt = request.json.get('userMessage')
        print(user_prompt)
        result = processor.search_candidate(user_prompt)
        print(result)

        # Convert Document objects to a serializable format
        serializable_results = []
        for doc in result:
            serializable_results.append({
                'page_content': doc.page_content,  # Include content or any other relevant fields
                'metadata': doc.metadata
            })

        return jsonify({'Response': serializable_results}), 200

    except KeyError:
        return jsonify({'error': 'User message not provided in request'}), 400
    except Exception as e:
        return jsonify({'error': f'Error in ranking the candidates: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
