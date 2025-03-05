import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import sys

# Add the parent directory to the path to import the model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import create_pneumonia_detection_model, create_data_augmentation

def load_and_preprocess_data(data_dir, img_size=(224, 224)):
    """
    Load and preprocess the dataset
    
    Args:
        data_dir: Directory containing 'NORMAL' and 'PNEUMONIA' subdirectories
        img_size: Tuple of (height, width) for resizing images
    
    Returns:
        X: Image data
        y: Labels
    """
    X = []
    y = []
    
    # Load normal cases
    normal_dir = os.path.join(data_dir, 'NORMAL')
    for img_name in os.listdir(normal_dir):
        if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(normal_dir, img_name)
            img = tf.keras.preprocessing.image.load_img(
                img_path, 
                target_size=img_size,
                color_mode='rgb'
            )
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            X.append(img_array)
            y.append(0)  # 0 for normal
    
    # Load pneumonia cases
    pneumonia_dir = os.path.join(data_dir, 'PNEUMONIA')
    for img_name in os.listdir(pneumonia_dir):
        if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(pneumonia_dir, img_name)
            img = tf.keras.preprocessing.image.load_img(
                img_path, 
                target_size=img_size,
                color_mode='rgb'
            )
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            X.append(img_array)
            y.append(1)  # 1 for pneumonia
    
    return np.array(X), np.array(y)

def plot_training_history(history):
    """
    Plot training history
    
    Args:
        history: Training history from model.fit()
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    
    # Plot loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.close()

def main():
    # Set random seed for reproducibility
    tf.random.set_seed(42)
    np.random.seed(42)
    
    # Configuration
    DATA_DIR = 'path/to/your/dataset'  # Update this path
    IMG_SIZE = (224, 224)
    BATCH_SIZE = 32
    EPOCHS = 20
    
    # Load and preprocess data
    print("Loading and preprocessing data...")
    X, y = load_and_preprocess_data(DATA_DIR, IMG_SIZE)
    
    # Split the data
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42, 
        stratify=y
    )
    
    # Normalize the data
    X_train = X_train / 255.0
    X_val = X_val / 255.0
    
    # Create data augmentation
    data_augmentation = create_data_augmentation()
    
    # Create the model
    print("Creating model...")
    model = create_pneumonia_detection_model(input_shape=(*IMG_SIZE, 3))
    
    # Create callbacks
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            'best_model.h5',
            monitor='val_accuracy',
            mode='max',
            save_best_only=True,
            verbose=1
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=3,
            min_lr=1e-6,
            verbose=1
        )
    ]
    
    # Train the model
    print("Training model...")
    history = model.fit(
        data_augmentation(X_train),
        y_train,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(X_val, y_val),
        callbacks=callbacks
    )
    
    # Plot training history
    print("Plotting training history...")
    plot_training_history(history)
    
    # Save the final model
    print("Saving model...")
    model.save('pneumonia_detection.h5')
    
    # Evaluate the model
    print("\nEvaluating model on validation set:")
    evaluation = model.evaluate(X_val, y_val, verbose=0)
    metrics = dict(zip(model.metrics_names, evaluation))
    
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

if __name__ == "__main__":
    main() 