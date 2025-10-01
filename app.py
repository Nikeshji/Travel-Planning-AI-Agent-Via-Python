from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_api import get_travel_recommendations
from models.user_input import UserInput

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/travel-plans', methods=['POST'])
def travel_plans():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_input = UserInput(data)

        if not user_input.is_valid():
            try:
                user_input.validate()
            except ValueError as e:
                return jsonify({'error': str(e)}), 400

        recommendations = get_travel_recommendations(user_input)
        return jsonify(recommendations)
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Travel Planner API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
