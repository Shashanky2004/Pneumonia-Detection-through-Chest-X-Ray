# Example CNN Model for Pneumonia Detection

This is an example implementation of a Convolutional Neural Network (CNN) model for pneumonia detection using chest X-ray images. This implementation serves as a reference and is not part of the main project.

## Model Architecture

The model uses transfer learning with ResNet50V2 as the base model and includes:
- Pre-trained ResNet50V2 base (weights from ImageNet)
- Custom dense layers with dropout and batch normalization
- Binary classification output (Normal vs Pneumonia)

## Directory Structure
```
cnn_model/
├── model/
│   ├── model.py             # Model architecture definition
│   └── training/
│       └── train.py         # Training script
└── requirements.txt         # Python dependencies
```

## Features
- Transfer Learning with ResNet50V2
- Data Augmentation Pipeline
- Training with Early Stopping
- Model Checkpointing
- Learning Rate Scheduling
- Training History Visualization

## Dataset Structure
The training script expects data in the following structure:
```
dataset/
├── NORMAL/
│   └── [normal chest X-ray images]
└── PNEUMONIA/
    └── [pneumonia chest X-ray images]
```

## Usage
This is an example implementation and is not connected to the main project. To experiment with this model:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Update the dataset path in `model/training/train.py`

3. Run training:
```bash
python model/training/train.py
```

## Note
This is a reference implementation only. The main project uses its own model and implementation. This example is provided for educational purposes and future reference. 