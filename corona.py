import cv2
import numpy as np
import argparse
import tensorflow as tf
from tensorflow.keras.models import load_model

def test(img_path):
    model_path = 'covid19.h5'  # Ensure this matches the correct format
    
    # Try loading the model safely
    try:
        model = load_model(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        exit(1)

    # Load the image
    img = cv2.imread(img_path)
    if img is None:
        print("Error: Unable to load image. Check the file path.")
        exit(1)
    
    img = cv2.resize(img, (224, 224))
    img_array = np.reshape(img, [1, 224, 224, 3])
    img_array = img_array / 255.0  # Normalize the image if the model expects it

    # Predict the class of the image
    prediction = model.predict(img_array)
    result = np.argmax(prediction, axis=-1)[0]
    confidence = np.max(prediction) * 100

    # Interpret the result
    if result == 1:
        prediction_text = f'Normal ({confidence:.2f}% confidence)'
        color = (0, 255, 0)  # Green
    else:
        prediction_text = f'Pneumonia ({confidence:.2f}% confidence)'
        color = (0, 0, 255)  # Red

    print(f"Result: {prediction_text}")

    # Prepare the image for displaying the result
    result_img = cv2.resize(img, (600, 600))
    cv2.putText(result_img, prediction_text, (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    
    return result_img

if __name__ == '__main__':
    # Parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="Path to the X-ray image")
    args = vars(ap.parse_args())

    # Run the prediction
    result_img = test(args["image"])

    # Display the result
    cv2.imshow("Result", result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
