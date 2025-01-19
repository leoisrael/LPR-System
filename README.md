# LPR-System

## Introduction

The LPR-System is a system designed for vehicle license plate recognition using modern computer vision and deep learning techniques. It was developed based on the YOLOv8 model (You Only Look Once, version 8), one of the most advanced frameworks for real-time object detection. This project aims to provide a complete pipeline that includes plate detection in images and cropping the detected areas for further processing.

## Methodology

### Model Architecture

YOLOv8 is an object detection model that combines accuracy and efficiency. It works by dividing the image into a grid, where each cell is responsible for predicting bounding boxes and their respective probabilities for each class. In this project, the model was configured to detect only one class: vehicle license plates.

### Training

The model was trained using a custom dataset of vehicle license plates. The dataset was pre-annotated in YOLO format, containing images with bounding boxes that delimit the plate areas. The training process used the following key configurations:

- **Base Model:** YOLOv8 Nano (lightweight version for better efficiency)
- **Image Size:** 640x640 pixels
- **Epochs:** 50
- **Initial Learning Rate:** 0.01
- **Data Split:** 80% for training and 20% for validation

### Evaluation Metrics

During training, the following metrics were monitored:

- **Precision:** Measures the proportion of correct predictions among all predictions made.
- **Recall:** Measures the proportion of true objects detected by the model.
- **mAP@50:** Mean Average Precision with an IoU (Intersection over Union) threshold of 50%.
- **mAP@50-95:** Mean Average Precision across multiple IoU thresholds (50% to 95%).

### Training Results

The graphs below, generated during training, illustrate the evolution of the metrics:

- **Loss:** Indicates the reduction of error throughout the training epochs.
- **Precision and Recall:** Show the model's ability to make correct detections.
- **mAP:** Demonstrates the overall precision of the model across multiple IoU thresholds.

![Image](https://github.com/user-attachments/assets/1bd990b2-3e4d-440c-b553-4498b115e420)

The results indicated solid performance, with **Precision** and **Recall** values exceeding 95% and a mAP@50 of approximately 94%.

## Pipeline Structure

1. **Preprocessing:** Images are resized to 640x640 pixels to ensure compatibility with the model.
2. **Inference:** YOLOv8 detects license plates in the uploaded images.
3. **Post-processing:** Bounding boxes are drawn on the original images, and regions of interest (ROIs) are cropped and stored for further analysis.

## Installation Requirements

To run the project, follow the steps below:

### 1. Install Python
Ensure Python 3.8 or later is installed on your machine.

### 2. Create a Virtual Environment
Create and activate a virtual environment to manage dependencies:

- **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- **Linux/Mac**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
With the virtual environment activated, install the dependencies:

```bash
pip install -r requirements.txt
```

### 4. Install PyTorch
Install PyTorch compatible with your machine:

- For CPU:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
  ```

- For GPU (check [PyTorch](https://pytorch.org/get-started/locally/) for specific configurations):
  ```bash
  pip install torch torchvision torchaudio
  ```

### 5. Run the Server
Start the Flask server to run the system:

```bash
python app.py
```

The system will be available at: [http://127.0.0.1:5000](http://127.0.0.1:5000).

