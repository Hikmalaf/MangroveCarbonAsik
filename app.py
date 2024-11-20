import os
from io import BytesIO
from PIL import Image, ImageDraw
import base64
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from ultralytics import YOLO
import numpy as np

# Inisialisasi aplikasi Flask
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["*","http://localhost:5173"]}})


# Konfigurasi
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load YOLO model
model = YOLO('best.pt')  # Path to your YOLOv8 model

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Convert image to base64 string for frontend
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Function to make predictions using YOLOv8
def predict_species(image):
    results = model(image)  # Run the YOLOv8 model on the image
    if results[0].boxes:
        species_class = results[0].boxes[0].cls.int().item()  # Get the class index
        species_name = results[0].names[species_class]  # Get the species name
        confidence = results[0].boxes[0].conf.item()  # Get the confidence score
        return species_name, confidence, results
    return None, None, None

# Function to draw bounding boxes and species labels
def draw_prediction(image, results):
    image_array = np.array(image)  # Convert PIL image to NumPy array
    for result in results[0].boxes:
        x1, y1, x2, y2 = result.xyxy[0].tolist()
        species_class = result.cls.int().item()
        species_name = results[0].names[species_class]
        image_pil = Image.fromarray(image_array)  # Convert NumPy array back to PIL
        draw = ImageDraw.Draw(image_pil)
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        draw.text((x1, y1 - 10), species_name, fill="red")
    return image_pil

# Route to root URL
@app.route('/')
def home():
    return "Welcome to the Mangrove Biomass & Carbon Calculator!"

# Prediction endpoint
@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    
    if not allowed_file(image_file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        image = Image.open(image_file.stream)
    except Exception as e:
        return jsonify({'error': 'Invalid image file'}), 400
    
    species_name, confidence, results = predict_species(image)
    if not species_name:
        return jsonify({'error': 'No species detected in the image'}), 400
    
    # Draw bounding boxes on the image
    image_with_bboxes = draw_prediction(image, results)
    image_base64 = image_to_base64(image_with_bboxes)

    return jsonify({
        'species_name': species_name,
        'confidence': confidence,  # Send confidence to the frontend
        'image_base64': image_base64
    })

# Run the Flask app
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))  # Gunakan $PORT atau default 8080
    app.run(host='0.0.0.0', port=port)
