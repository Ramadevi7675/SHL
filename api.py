from flask import Flask, request, jsonify
import pandas as pd
from matching_engine import recommend_assessments

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the SHL Assessment Recommender API. Use the '/recommend' endpoint to get assessment recommendations."

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    jd_text = data.get('job_description', '')

    if not jd_text:
        return jsonify({'error': 'Job description is required'}), 400

    recommendations = recommend_assessments(jd_text, csv_path="shl_sample_assessments.csv")

    if recommendations.empty:
        return jsonify({'message': 'No matching assessments found'}), 404

    recommendations_list = recommendations.to_dict(orient='records')
    return jsonify(recommendations_list)

@app.route('/query', methods=['GET'])
def query():
    text = request.args.get('text', '')

    if not text:
        return jsonify({'error': 'Query text is required'}), 400

    results = recommend_assessments(text, csv_path="shl_sample_assessments.csv")

    if results.empty:
        return jsonify({'message': 'No matching assessments found'}), 404

    results_list = results.to_dict(orient='records')
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=True)
