from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
from ranking import CVRanking
import pandas as pd

app =  Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': '*'}})

processor = CVRanking()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-uploaded_cv', methods=['POST'])
def process_uploaded_cv():
    if 'file' not in request.files:
        return jsonify({'botResponse': 'Tolong upload file PDF'}), 400

    file = request.files['file']
    
    # Store file in a user-specific directory
    user_cv_pdf = "user_cv_pdf"
    os.makedirs(user_cv_pdf, exist_ok=True)

    user_cv_pdf_path = os.path.join(user_cv_pdf, file.filename)

    if not os.path.exists(user_cv_pdf_path):
        file.save(user_cv_pdf_path)
    else:
        return jsonify({'response' : "Anda sudah mengupload CV anda"})


    processor.extract_cv(user_cv_pdf_path, file.filename)

    return jsonify({'response' : 'Your CV sucessfully uploaded'})

@app.route('/rank-applicants', methods=['POST'])
def rank_applicants():
    job_description = request.form['job_description']

    try:
        candidate_ranking = processor.rank_candidate(job_description)
        print(candidate_ranking)
        # Convert the ranked candidates to a DataFrame
        ranked_df = pd.DataFrame(candidate_ranking)# Transpose for better formatting

        # Convert the DataFrame to HTML
        ranking_table_html = ranked_df.to_html(index=False, border=1)

        ranking_table_html = ranking_table_html.replace('<th>', '<th style="text-align: center; padding: 10px; background-color: #f2f2f2;">')

        return jsonify({'response': ranking_table_html})
    
    except:
        return jsonify({'error':'error in ranking the candidates'})

    

if __name__ == "__main__":
    app.run(debug=True, port=5000)