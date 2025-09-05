from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from utils import initialize_metta, execute_simple_list, execute_query, get_explanations, user_exists, add_new_user
from parser import parse_question_to_json, map_json_to_metta


load_dotenv()

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")


metta_file_path = os.getenv("METTA_FILE_PATH", "recommendation.metta")
metta = initialize_metta(metta_file_path)

@app.route('/')
def index():
    print("Serving index.html")
    return render_template('index.html')

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    user = data.get('user')
    print(f"Received get-recommendations request for user: {user}")
    if not user:
        return jsonify({"error": "User is required"}), 400
    try:
        rec_list = execute_simple_list(metta, f'!(recommend-to {user} $movie)')
        print(f"Raw recommendations for {user}: {rec_list}")
        final_recs = execute_query(metta, f'!(recommend-to {user} $movie)')
        explanations = get_explanations(metta, user, final_recs)
        similar_users = execute_simple_list(metta, f'!(similar-users {user} $user)')
        watched = execute_query(metta, f'!(watched {user} $movie)')
        response = {
            "recommendations": final_recs,
            "explanations": explanations,
            "similar_users": similar_users,
            "watched": watched if watched else [{"id": "none", "title": "No movies watched"}]
        }
        print(f"get-recommendations response: {response}")
        return jsonify(response)
    except Exception as e:
        print(f"Error in get-recommendations: {str(e)}")
        return jsonify({"error": f"Error fetching recommendations: {str(e)}"}), 500

@app.route('/parse-query', methods=['POST'])
def parse_query():
    data = request.json
    question = data.get('question')
    assumed_subject = data.get('user', 'Alice')
    print(f"Received parse-query request: question='{question}', user='{assumed_subject}'")
    if not question:
        return jsonify({"error": "Question is required"}), 400
    try:
        parsed_json = parse_question_to_json(question, assumed_subject)
        print(f"Parsed question '{question}' to: {parsed_json}")
        metta_query = map_json_to_metta(parsed_json)
        results = execute_simple_list(metta, metta_query)
      
        if parsed_json['relation'] == "Likes" and parsed_json.get('target_attribute'):
            recommendations = [{"id": parsed_json['target_attribute']['value'], "title": parsed_json['target_attribute']['value'].replace("-", " ").title()}] if results else []
        else:
            recommendations = execute_query(metta, metta_query)
        explanations = get_explanations(metta, parsed_json['subject'], recommendations) if parsed_json['relation'] != "Likes" else [results or ["No preference found"]]
        response = {
            "parsed_query": parsed_json,
            "recommendations": recommendations,
            "explanations": explanations
        }
        print(f"parse-query response: {response}")
        return jsonify(response)
    except Exception as e:
        print(f"Error in parse-query: {str(e)}")
        return jsonify({"error": f"Error parsing query: {str(e)}"}), 500




@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    print(f"Received add-user request: {data}")
    username = data.get('username', '').strip().lower()
    if not username:
        print("Error: Username is empty or missing")
        return jsonify({"error": "Username is required"}), 400
    query = f'!(match &self (user {username}) $x)'
    results = execute_simple_list(query)
    print(f"Check user query: {query}, results: {results}")
    if results:
        print(f"Error: User '{username}' already exists")
        return jsonify({"error": f"User '{username}' already exists"}), 409
    add_metta_atom(f'(user {username})')
    print(f"Added user: {username}")
    return jsonify({"message": f"User '{username}' added successfully"}), 201

@app.route('/update-preferences', methods=['POST'])
def update_preferences():
    data = request.json
    user = data.get('user')
    new_genre = data.get('new_genre')
    print(f"Received update-preferences request: user={user}, genre={new_genre}")
    if not user or not new_genre:
        return jsonify({"error": "User and genre are required"}), 400
    try:
        if not user_exists(metta, user):
            add_new_user(metta, user)
        metta.run(f'(preference {user} {new_genre})')
        return jsonify({"message": f"Genre preference '{new_genre}' added for {user}"})
    except Exception as e:
        print(f"Error in update-preferences: {str(e)}")
        return jsonify({"error": f"Error updating preferences: {str(e)}"}), 500

@app.route('/get-users', methods=['GET'])
def get_users():
    try:
        print("Received get-users request")
        results = execute_simple_list(metta, '!(match &self (watched $user $movie) $user)')
        response = {"users": results}
        print(f"get-users response: {response}")
        if not results:
            print("No users found in MeTTa knowledge base")
        return jsonify(response)
    except Exception as e:
        print(f"Error fetching users: {str(e)}")
        return jsonify({"error": f"Error fetching users: {str(e)}"}), 500

@app.route('/add-rating', methods=['POST'])
def add_rating():
    data = request.json
    user = data.get('user')
    movie = data.get('movie')
    rating = data.get('rating')
    print(f"Received add-rating request: user={user}, movie={movie}, rating={rating}")
    if not user or not movie or not rating:
        return jsonify({"error": "User, movie, and rating required"}), 400
    try:
        metta.run(f'(user-rating {user} {movie} {rating})')
        return jsonify({"message": f"Rating {rating} added for {movie} by {user}"})
    except Exception as e:
        print(f"Error in add-rating: {str(e)}")
        return jsonify({"error": f"Error adding rating: {str(e)}"}), 500

@app.route('/get-movies', methods=['GET'])
def get_movies():
    try:
        print("Received get-movies request")
        results = execute_simple_list(metta, '!(match &self (movie $id $title $genre $director $rating) $id)')
        response = {"movies": results}
        print(f"get-movies response: {response}")
        return jsonify(response)
    except Exception as e:
        print(f"Error fetching movies: {str(e)}")
        return jsonify({"error": f"Error fetching movies: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    print(f"Starting Flask server on port {port}, debug={debug}")
    app.run(debug=debug, host='0.0.0.0', port=port)