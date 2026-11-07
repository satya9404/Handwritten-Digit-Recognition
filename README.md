# Handwritten Digit Recognition System

An AI-based handwritten digit recognition web application using a
Convolutional Neural Network (CNN), TensorFlow/Keras, OpenCV, and Flask.
Users can upload an image or draw one digit (0--9) in the browser.

## Features

-   CNN classification of handwritten digits 0--9.
-   Upload PNG, JPG, or JPEG images.
-   Draw a digit using an HTML canvas.
-   Preprocess images to 28 × 28 grayscale format.
-   Display the predicted digit and confidence score.
-   Flask backend with `/predict` and `/health` routes.

## Technology stack

Python, TensorFlow/Keras, NumPy, OpenCV, Flask, HTML, CSS, JavaScript,
and MNIST.

## Project structure

``` text
Handwritten_Digit_Recognition/
├── app.py
├── preprocessing.py
├── requirements.txt
├── README.md
├── models/digit_model.keras
├── notebooks/
│   ├── mnist_exploration.ipynb
│   ├── image_preprocessing.ipynb
│   └── model_training.ipynb
├── templates/index.html
└── static/
    ├── css/style.css
    ├── js/script.js
    └── uploads/
```

## CNN architecture

Input (28×28×1) → Conv2D(32, 3×3, ReLU) → MaxPooling(2×2) → Conv2D(64,
3×3, ReLU) → MaxPooling(2×2) → Flatten → Dense(128, ReLU) → Dropout(0.3)
→ Dense(10, Softmax).

## Setup (Windows)

``` bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in your browser. The trained model must be
present at `models/digit_model.keras`.

Health check: `http://127.0.0.1:5000/health`.

## Usage

**Upload:** Choose a PNG/JPG/JPEG image containing one digit and click
the upload prediction button.

**Draw:** Draw one digit on the canvas and click the drawing prediction
button. Use Clear to reset the canvas.

For best results, use one clear, dark digit on a plain, light
background.

## Image preprocessing

The application reads the image, converts it to grayscale, improves
contrast/lighting, thresholds the handwriting, removes small noise,
crops the digit, adds padding, resizes while preserving aspect ratio,
places it on a 28×28 canvas, normalizes pixel values to 0--1, and
reshapes it to `(1, 28, 28, 1)`.

## Training and evaluation

The training notebook loads MNIST, preprocesses the data, trains the
CNN, evaluates it on the test set, and creates accuracy/loss plots and a
confusion matrix. Enter the final metrics from your latest notebook run
in the report. MNIST test accuracy does not guarantee equal accuracy on
external photographs.

## Main files

-   `app.py`: Flask server and prediction endpoint.
-   `preprocessing.py`: image preprocessing for user inputs.
-   `models/digit_model.keras`: trained CNN model.
-   `templates/index.html`: web page.
-   `static/css/style.css`: styling.
-   `static/js/script.js`: upload, drawing, and prediction logic.
-   `notebooks/`: exploration, preprocessing, training, and evaluation.

## Limitations

The system is designed for a single digit. Images with complex
backgrounds, poor lighting, unusual handwriting, or multiple digits may
reduce accuracy. Confidence is the model's highest output probability,
not a guarantee of correctness.

## Author

Name: Kondru Satyanarayana
Programme: B.Tech -- Computer Science and Engineering
Institution: National Institute of Technology Nagaland
