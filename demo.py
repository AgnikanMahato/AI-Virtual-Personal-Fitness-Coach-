#!/usr/bin/env python3
"""
Demo script for AI Fitness Coach
Tests pose detection functionality with webcam or sample images
"""

import cv2
import numpy as np
import time
from pose_detector import PoseDetector

def test_webcam():
    """Test pose detection with webcam feed"""
    print("🎥 Testing webcam pose detection...")
    print("Press 'q' to quit, 'r' to reset counter")
    
    # Initialize pose detector
    detector = PoseDetector()
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam")
        return
    
    print("✅ Webcam opened successfully")
    print("📱 Position yourself in front of the camera")
    print("🏋️ Try doing some pushups or squats")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read frame")
            break
        
        # Process frame
        processed_frame, exercise_data = detector.process_frame(frame, "pushup")
        
        # Display frame
        cv2.imshow('AI Fitness Coach - Demo', processed_frame)
        
        # Print exercise data
        print(f"\rReps: {exercise_data['reps']} | State: {exercise_data['state']} | Angle: {exercise_data['angle']:.1f}°", end='')
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            detector.reset_counter()
            print("\n🔄 Counter reset!")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ Demo completed!")

def test_image_processing():
    """Test pose detection with a sample image"""
    print("🖼️ Testing image processing...")
    
    # Initialize pose detector
    detector = PoseDetector()
    
    # Create a simple test image (you can replace this with a real image path)
    print("📸 Please provide an image path or press Enter to use webcam")
    image_path = input("Image path (or press Enter for webcam): ").strip()
    
    if image_path:
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                print(f"❌ Error: Could not load image from {image_path}")
                return
            
            print(f"✅ Image loaded: {image.shape}")
            
            # Process image
            processed_image, exercise_data = detector.process_frame(image, "pushup")
            
            # Display results
            print(f"📊 Exercise Data:")
            print(f"   Reps: {exercise_data['reps']}")
            print(f"   State: {exercise_data['state']}")
            print(f"   Angle: {exercise_data['angle']:.1f}°")
            print(f"   Form Score: {exercise_data['form']['score']}/100")
            
            if exercise_data['form']['issues']:
                print(f"   Issues: {', '.join(exercise_data['form']['issues'])}")
            
            if exercise_data['form']['tips']:
                print(f"   Tips: {', '.join(exercise_data['form']['tips'])}")
            
            # Save processed image
            output_path = "processed_image.jpg"
            cv2.imwrite(output_path, processed_image)
            print(f"💾 Processed image saved to {output_path}")
            
            # Display image
            cv2.imshow('Original Image', image)
            cv2.imshow('Processed Image', processed_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        except Exception as e:
            print(f"❌ Error processing image: {e}")
    else:
        print("🔄 Switching to webcam mode...")
        test_webcam()

def test_exercise_detection():
    """Test different exercise types"""
    print("🏋️ Testing exercise detection...")
    
    detector = PoseDetector()
    
    exercises = ["pushup", "squat"]
    
    for exercise in exercises:
        print(f"\n📝 Testing {exercise.upper()} detection:")
        print(f"   Down threshold: {detector.angle_thresholds[exercise]['down']}°")
        print(f"   Up threshold: {detector.angle_thresholds[exercise]['up']}°")
        
        # Test angle calculation
        test_angles = [45, 90, 135, 180]
        for angle in test_angles:
            if angle < detector.angle_thresholds[exercise]['down']:
                state = "down"
            elif angle > detector.angle_thresholds[exercise]['up']:
                state = "up"
            else:
                state = "transition"
            
            print(f"   Angle {angle}° → State: {state}")

def main():
    """Main demo function"""
    print("💪 AI Fitness Coach - Demo Mode")
    print("=" * 40)
    
    while True:
        print("\n🎯 Choose demo option:")
        print("1. Webcam pose detection")
        print("2. Image processing")
        print("3. Exercise detection test")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            test_webcam()
        elif choice == '2':
            test_image_processing()
        elif choice == '3':
            test_exercise_detection()
        elif choice == '4':
            print("👋 Thanks for trying AI Fitness Coach!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 