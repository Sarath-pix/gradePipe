from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data or 'marks' not in data:
                return jsonify({"error": "Invalid payload. 'marks' list is required."}), 400
            
            marks = data['marks']
            if not isinstance(marks, list) or len(marks) == 0:
                return jsonify({"error": "'marks' must be a non-empty list of numbers."}), 400
            
            if not all(isinstance(m, (int, float)) for m in marks):
                return jsonify({"error": "All marks must be numerical values."}), 400

            total = sum(marks)
            average = total / len(marks)

            # Evaluate grades based on computed average score values
            if average >= 90:
                grade = 'A'
            elif average >= 80:
                grade = 'B'
            elif average >= 70:
                grade = 'C'
            elif average >= 60:
                grade = 'D'
            else:
                grade = 'F'

            return jsonify({
                "total": total,
                "average": average,
                "grade": grade,
                "message": "Grade calculated successfully using Push 2 logic!"
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({
        "application": "Student Grade Calculator API",
        "version": "2.0.0",
        "instructions": "Send a POST request to this endpoint with a JSON body like {'marks': [85, 90, 78]}"
    }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
