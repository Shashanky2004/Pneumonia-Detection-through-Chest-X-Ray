from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import io
from PIL import Image
import os
import requests

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_model(url, save_path):
    """Download the model file from the given URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save the file
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading model: {e}")
        return False

# Load the model at startup
model = None
try:
    model_path = os.path.join(os.path.dirname(__file__), 'pneumonia_detection.h5')
    model = load_model(model_path)
    print(f"Model loaded successfully from: {model_path}")
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 