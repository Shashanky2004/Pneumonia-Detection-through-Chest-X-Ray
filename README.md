# COVID-19 Detection through Chest X-Ray Analysis

## Overview
A web-based application that utilizes deep learning to detect COVID-19 from chest X-ray images. This system provides medical professionals and researchers with a user-friendly interface for rapid COVID-19 screening through chest X-ray analysis.

## Features
- Real-time COVID-19 detection from chest X-rays
- Interactive web interface with drag-and-drop functionality
- Progress tracking during analysis
- Confidence score generation
- Responsive design for all devices
- Comprehensive error handling and validation

## Tech Stack
### Frontend
- React.js
- TypeScript
- React Router
- CSS3 for styling and animations

# Screeshot of the project
<img width="1470" alt="Screenshot 2025-04-01 at 11 46 02 PM" src="https://github.com/user-attachments/assets/f7659731-168f-449d-8772-876deb0ee4f3" />
![image](https://github.com/user-attachments/assets/b38d0a96-60d2-44ed-9267-ae9228d583f6)
![image](https://github.com/user-attachments/assets/008f952a-75fd-48c3-b781-241f1d32ccf8)
![image](https://github.com/user-attachments/assets/e8945c2f-cc62-499d-a7da-8fcbf9202f30)

### Backend
- Django
- Django REST Framework
- TensorFlow/Keras
- Python 3.x

## Prerequisites
- Python 3.8 or higher
- Node.js 14.x or higher
- npm 6.x or higher

## Installation

### Backend Setup
1. Navigate to the backend directory:
```bash
cd frontend/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend Server
```bash
cd frontend/backend
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
python manage.py runserver
```
The backend will be available at http://localhost:8000

### Start the Frontend Server
```bash
cd frontend
npm start
```
The application will open automatically at http://localhost:3000

## Usage
1. Access the application through your web browser at http://localhost:3000
2. Click "Start Analysis" on the landing page
3. Upload a chest X-ray image using drag-and-drop or file browser
4. Click "Analyze Image" to process the X-ray
5. View the results with confidence scores
6. Use "Try Another Image" to analyze more X-rays

## Project Structure
