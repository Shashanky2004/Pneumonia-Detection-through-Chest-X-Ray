from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import io
from PIL import Image
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model at startup
model = None
try:
    # Get the absolute path to the model file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(os.path.dirname(current_dir), 'pneumonia_detection.h5')
    model = load_model(model_path)
    print(f"Model loaded successfully from {model_path}!")
except Exception as e:
    print(f"Error loading model: {e}")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read the image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return {"error": "Invalid image file"}
        
        # Preprocess the image
        img = cv2.resize(img, (224, 224))
        img_array = np.reshape(img, [1, 224, 224, 3])
        img_array = img_array / 255.0
        
        # Make prediction
        prediction = model.predict(img_array)
        result = np.argmax(prediction, axis=-1)[0]
        confidence = float(np.max(prediction) * 100)
        
        # Format the response
        if result == 1:
            prediction_text = f"Normal (Confidence: {confidence:.2f}%)"
        else:
            prediction_text = f"Pneumonia Detected (Confidence: {confidence:.2f}%)"
        
        return {"prediction": prediction_text}
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return {"error": "Error processing image"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_type": "Pneumonia Detection Model"
    } 