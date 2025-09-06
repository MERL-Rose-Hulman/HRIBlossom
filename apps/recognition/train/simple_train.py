#!/usr/bin/env python3
"""
Simple MediaPipe gesture training script.
Follows the official MediaPipe approach exactly.
"""

import os
import sys
from mediapipe_model_maker import gesture_recognizer

def train_gesture_model(data_dir="/workspace/data", output_dir="/workspace/output", model_name="gesture_model"):
    """Train gesture model using MediaPipe Model Maker."""
    
    print(f"Training with data from: {data_dir}")
    print(f"Output directory: {output_dir}")
    
    # Check if data directory exists
    if not os.path.exists(data_dir):
        print(f"Error: Data directory {data_dir} not found")
        return False
    
    # List available gestures
    gestures = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    print(f"Found gestures: {gestures}")
    
    if "none" not in gestures:
        print("Warning: 'none' gesture not found. This is required by MediaPipe.")
    
    try:
        # Load dataset (MediaPipe will extract hand landmarks from images)
        print("Loading dataset...")
        data = gesture_recognizer.Dataset.from_folder(
            dirname=data_dir,
            hparams=gesture_recognizer.HandDataPreprocessingParams()
        )
        
        # Split dataset
        train_data, rest_data = data.split(0.8)
        validation_data, test_data = rest_data.split(0.5)
        
        print(f"Training samples: {len(train_data)}")
        print(f"Validation samples: {len(validation_data)}")
        print(f"Test samples: {len(test_data)}")
        
        # Configure training
        hparams = gesture_recognizer.HParams(
            export_dir=output_dir,
            epochs=10,
            batch_size=8,
            learning_rate=0.001
        )
        options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)
        
        # Train model
        print("Training model...")
        model = gesture_recognizer.GestureRecognizer.create(
            train_data=train_data,
            validation_data=validation_data,
            options=options
        )
        
        # Evaluate
        print("Evaluating model...")
        loss, accuracy = model.evaluate(test_data, batch_size=1)
        print(f"Test loss: {loss}, Test accuracy: {accuracy}")
        
        # Export model
        print("Exporting model...")
        model.export_model()
        
        # Rename the output file
        default_model_path = os.path.join(output_dir, "gesture_recognizer.task")
        custom_model_path = os.path.join(output_dir, f"{model_name}.task")
        
        if os.path.exists(default_model_path) and default_model_path != custom_model_path:
            os.rename(default_model_path, custom_model_path)
        
        print(f"Model saved to: {custom_model_path}")
        return True
        
    except Exception as e:
        print(f"Training failed: {e}")
        return False

if __name__ == "__main__":
    # Parse command line arguments
    data_dir = "/workspace/data"
    output_dir = "/workspace/output" 
    model_name = "gesture_model"
    
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    if len(sys.argv) > 3:
        model_name = sys.argv[3]
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Train model
    success = train_gesture_model(data_dir, output_dir, model_name)
    
    if success:
        print("Training completed successfully!")
    else:
        print("Training failed!")
        sys.exit(1)
