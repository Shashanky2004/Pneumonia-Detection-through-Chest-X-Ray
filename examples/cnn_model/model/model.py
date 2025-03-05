import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.optimizers import Adam

def create_pneumonia_detection_model(input_shape=(224, 224, 3)):
    """
    Creates a CNN model for pneumonia detection using transfer learning with ResNet50V2
    
    Args:
        input_shape: Tuple of (height, width, channels) for input images
        
    Returns:
        model: Compiled Keras model
    """
    # Load the pretrained ResNet50V2 model without the top layer
    base_model = ResNet50V2(
        include_top=False,
        weights='imagenet',
        input_shape=input_shape,
        pooling='avg'
    )
    
    # Freeze the base model layers
    base_model.trainable = False
    
    # Create the model
    model = models.Sequential([
        # Base ResNet50V2 model
        base_model,
        
        # Add custom layers for pneumonia detection
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.BatchNormalization(),
        
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.BatchNormalization(),
        
        # Output layer with sigmoid activation for binary classification
        layers.Dense(1, activation='sigmoid')
    ])
    
    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='binary_crossentropy',
        metrics=[
            'accuracy',
            tf.keras.metrics.AUC(name='auc'),
            tf.keras.metrics.Precision(name='precision'),
            tf.keras.metrics.Recall(name='recall')
        ]
    )
    
    return model

def create_data_augmentation():
    """
    Creates a data augmentation pipeline for training
    
    Returns:
        data_augmentation: Sequential model for data augmentation
    """
    data_augmentation = models.Sequential([
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
        layers.RandomFlip("horizontal"),
        layers.RandomBrightness(0.2),
        layers.RandomContrast(0.2),
    ])
    
    return data_augmentation 