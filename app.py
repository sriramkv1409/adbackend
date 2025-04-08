from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from deepface import DeepFace

app = Flask(__name__)
CORS(app)

@app.route("/predict-age-gender", methods=["POST"])
def predict_age_gender():
    if "image" not in request.files:
        return jsonify({"error": "No image file found"}), 400

    file = request.files["image"]
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    try:
        result = DeepFace.analyze(img, actions=["age", "gender"], enforce_detection=False)[0]
        age = result.get("age", 0)
        
        # Safely extract gender
        gender_data = result.get("gender", "")
        if isinstance(gender_data, dict):
            # DeepFace might return probability dict like {"Man": 60.0, "Woman": 40.0}
            gender = max(gender_data, key=gender_data.get)
        else:
            gender = str(gender_data)

        # Categorize age
        if age <= 12:
            age_group = "Child (0-12)"
        elif age <= 19:
            age_group = "Teenager (13-19)"
        elif age <= 34:
            age_group = "Young Adult (20-34)"
        elif age <= 49:
            age_group = "Middle-aged Adult (35-49)"
        else:
            age_group = "Senior (50+)"

        return jsonify({
            "age_group": age_group,
            "gender": gender
        })

    except Exception as e:
        return jsonify({"error": f"Error detecting age or gender: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
