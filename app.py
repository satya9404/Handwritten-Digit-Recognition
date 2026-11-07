from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template
from preprocessing import preprocess_image

import os
import uuid
import numpy as np


# Initialize Flask application
app = Flask(__name__)


# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR, "models", "digit_model.keras"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR, "static", "uploads"
)


# Create upload folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Upload configuration
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


# Load trained CNN model
model = load_model(MODEL_PATH)

print("CNN model loaded successfully!")


# Check allowed file extensions
def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# Home route
@app.route("/")
def home():

    return render_template("index.html")

@app.route("/health")
def health():

    return jsonify({
        "status": "success",
        "message": "Handwritten Digit Recognition API is running"
    })
# Prediction route
@app.route("/predict", methods=["POST"])
def predict():

    # Check whether image is uploaded
    if "file" not in request.files:

        return jsonify({
            "error": "No image uploaded"
        }), 400

    file = request.files["file"]

    # Check empty filename
    if file.filename == "":

        return jsonify({
            "error": "Please select an image"
        }), 400

    # Validate file type
    if not allowed_file(file.filename):

        return jsonify({
            "error": "Only PNG, JPG and JPEG images are allowed"
        }), 400

    # Generate safe unique filename
    filename = secure_filename(file.filename)

    unique_filename = str(uuid.uuid4()) + "_" + filename

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )

    try:

        # Save uploaded image
        file.save(image_path)

        # Preprocess image
        processed_image = preprocess_image(image_path)

        # Predict digit
        prediction = model.predict(
            processed_image,
            verbose=0
        )

        # Find predicted digit
        predicted_digit = int(np.argmax(prediction))

        # Calculate confidence
        confidence = float(np.max(prediction) * 100)

        return jsonify({

            "success": True,
            "predicted_digit": predicted_digit,
            "confidence": round(confidence, 2)

        })

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

    except Exception as error:

        app.logger.exception("Prediction failed")

        return jsonify({
            "error": "Unable to process image"
        }), 500

    finally:

        # Delete temporary uploaded image
        if os.path.exists(image_path):
            os.remove(image_path)


# Run application
if __name__ == "__main__":

    app.run(debug=True)