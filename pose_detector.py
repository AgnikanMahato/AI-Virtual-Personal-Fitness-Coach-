import cv2
import mediapipe as mp
import numpy as np
import math
from typing import Tuple, List, Dict
import time

class PoseDetector:
    def detect_plank(self, landmarks) -> dict:
        """Detect plank pose and count hold time as reps"""
        if not landmarks:
            return {"state": "no_detection", "angle": 0, "reps": self.rep_count, "form": self.assess_form(landmarks)}
        # Use shoulder-hip-ankle angle for plank
        left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
        left_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]
        angle = self.calculate_angle(left_shoulder, left_hip, left_ankle)
        thresholds = self.angle_thresholds["plank"]
        current_time = time.time()
        if angle > thresholds["down"]:
            if self.exercise_state != "hold":
                self.exercise_state = "hold"
                self.last_rep_time = current_time
            # Count seconds held as reps
            self.rep_count = int(current_time - self.last_rep_time)
        else:
            self.exercise_state = "rest"
            self.rep_count = 0
        return {"state": self.exercise_state, "angle": angle, "reps": self.rep_count, "form": self.assess_form(landmarks)}

    def detect_lunge(self, landmarks) -> dict:
        """Detect lunge pose and count reps"""
        if not landmarks:
            return {"state": "no_detection", "angle": 0, "reps": self.rep_count, "form": self.assess_form(landmarks)}
        # Use knee angle for lunge
        left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
        left_knee = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_KNEE]
        left_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]
        angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        thresholds = self.angle_thresholds["lunge"]
        current_time = time.time()
        if angle < thresholds["down"]:
            if self.exercise_state != "down":
                self.exercise_state = "down"
        elif angle > thresholds["up"]:
            if self.exercise_state == "down":
                if current_time - self.last_rep_time > self.rep_cooldown:
                    self.rep_count += 1
                    self.last_rep_time = current_time
                self.exercise_state = "up"
        return {"state": self.exercise_state, "angle": angle, "reps": self.rep_count, "form": self.assess_form(landmarks)}

    def detect_burpee(self, landmarks) -> dict:
        """Detect burpee pose and count reps (simple squat logic)"""
        # For demo, use squat logic
        return self.detect_squat(landmarks)

    def detect_downward_dog(self, landmarks) -> dict:
        """Detect downward dog yoga pose and count hold time as reps"""
        if not landmarks:
            return {"state": "no_detection", "angle": 0, "reps": self.rep_count, "form": self.assess_form(landmarks)}
        # Use hip angle for downward dog
        left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
        left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
        left_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]
        angle = self.calculate_angle(left_wrist, left_hip, left_ankle)
        thresholds = self.angle_thresholds["downward dog"]
        current_time = time.time()
        if angle > thresholds["down"]:
            if self.exercise_state != "hold":
                self.exercise_state = "hold"
                self.last_rep_time = current_time
            self.rep_count = int(current_time - self.last_rep_time)
        else:
            self.exercise_state = "rest"
            self.rep_count = 0
        return {"state": self.exercise_state, "angle": angle, "reps": self.rep_count, "form": self.assess_form(landmarks)}
    def __init__(self):
        """Initialize MediaPipe Pose detection"""
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Exercise state tracking
        self.exercise_state = "rest"  # rest, down, up
        self.rep_count = 0
        self.last_rep_time = time.time()
        self.rep_cooldown = 1.0  # seconds between reps
        
        # Exercise configuration
        self.exercise_type = "pushup"  # pushup, squat, plank, etc.
        self.angle_thresholds = {
            "pushup": {"down": 90, "up": 160},
            "squat": {"down": 70, "up": 160},
            "plank": {"down": 160, "up": 180},
            "lunge": {"down": 80, "up": 160},
            "burpee": {"down": 60, "up": 160},
            "mountain climber": {"down": 60, "up": 160},
            "jumping jack": {"down": 60, "up": 160},
            "crunch": {"down": 60, "up": 160},
            "bicep curl": {"down": 40, "up": 160},
            "tricep dip": {"down": 60, "up": 160},
            "shoulder press": {"down": 60, "up": 160},
            # Yoga poses (use up/down as placeholders)
            "downward dog": {"down": 120, "up": 180},
            "warrior I": {"down": 120, "up": 180},
            "warrior II": {"down": 120, "up": 180},
            "tree pose": {"down": 120, "up": 180},
            "cobra pose": {"down": 120, "up": 180},
            "child's pose": {"down": 120, "up": 180},
            "cat-cow": {"down": 120, "up": 180},
            "bridge pose": {"down": 120, "up": 180},
            "seated twist": {"down": 120, "up": 180},
            "triangle pose": {"down": 120, "up": 180}
        }
    def detect_stub(self, landmarks) -> dict:
        """Stub for exercises/yoga not yet implemented"""
        return {
            "state": "not_implemented",
            "angle": 0,
            "reps": self.rep_count,
            "form": {"score": 0, "issues": ["Detection not implemented for this exercise."], "tips": []}
        }
        
    def calculate_angle(self, a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
        """Calculate angle between three points"""
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
                 np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle
    
    def detect_pushup(self, landmarks) -> Dict:
        """Detect pushup pose and count reps"""
        if not landmarks:
            return {"state": "no_detection", "angle": 0, "reps": self.rep_count}
        
        # Get key points for pushup
        left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
        left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
        
        right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
        
        # Calculate angles
        left_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
        
        # Use average angle
        avg_angle = (left_angle + right_angle) / 2
        
        # Determine state
        thresholds = self.angle_thresholds["pushup"]
        current_time = time.time()
        
        if avg_angle < thresholds["down"]:
            if self.exercise_state != "down":
                self.exercise_state = "down"
        elif avg_angle > thresholds["up"]:
            if self.exercise_state == "down":
                # Complete rep detected
                if current_time - self.last_rep_time > self.rep_cooldown:
                    self.rep_count += 1
                    self.last_rep_time = current_time
                self.exercise_state = "up"
        
        return {
            "state": self.exercise_state,
            "angle": avg_angle,
            "reps": self.rep_count,
            "form": self.assess_form(landmarks)
        }
    
    def detect_squat(self, landmarks) -> Dict:
        """Detect squat pose and count reps"""
        if not landmarks:
            return {"state": "no_detection", "angle": 0, "reps": self.rep_count}
        
        # Get key points for squat
        left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
        left_knee = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_KNEE]
        left_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]
        
        right_hip = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
        right_knee = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_KNEE]
        right_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
        
        # Calculate angles
        left_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        right_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
        
        avg_angle = (left_angle + right_angle) / 2
        
        # Determine state
        thresholds = self.angle_thresholds["squat"]
        current_time = time.time()
        
        if avg_angle < thresholds["down"]:
            if self.exercise_state != "down":
                self.exercise_state = "down"
        elif avg_angle > thresholds["up"]:
            if self.exercise_state == "down":
                if current_time - self.last_rep_time > self.rep_cooldown:
                    self.rep_count += 1
                    self.last_rep_time = current_time
                self.exercise_state = "up"
        
        return {
            "state": self.exercise_state,
            "angle": avg_angle,
            "reps": self.rep_count,
            "form": self.assess_form(landmarks)
        }
    
    def assess_form(self, landmarks) -> Dict:
        """Assess exercise form quality"""
        form_feedback = {
            "score": 100,
            "issues": [],
            "tips": []
        }
        
        # Check if person is visible
        if not landmarks:
            form_feedback["score"] = 0
            form_feedback["issues"].append("No person detected")
            return form_feedback
        
        # Check posture alignment for pushup
        if self.exercise_type == "pushup":
            # Check if body is straight
            left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
            left_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]
            
            # Calculate body alignment
            shoulder_hip_angle = self.calculate_angle(
                landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW],
                left_shoulder,
                left_hip
            )
            
            if shoulder_hip_angle < 160:
                form_feedback["score"] -= 20
                form_feedback["issues"].append("Keep your body straight")
                form_feedback["tips"].append("Engage your core and maintain a straight line from head to heels")
        
        return form_feedback
    
    def process_frame(self, frame: np.ndarray, exercise_type: str = "pushup") -> Tuple[np.ndarray, Dict]:
        """Process a single frame and return annotated frame with exercise data"""
        self.exercise_type = exercise_type
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        # Initialize exercise data
        exercise_data = {
            "state": "no_detection",
            "angle": 0,
            "reps": self.rep_count,
            "form": {"score": 0, "issues": [], "tips": []}
        }
        
        if results.pose_landmarks:
            # Draw pose landmarks
            annotated_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
            # Detect exercise based on type
            if exercise_type == "pushup":
                exercise_data = self.detect_pushup(results.pose_landmarks)
            elif exercise_type == "squat":
                exercise_data = self.detect_squat(results.pose_landmarks)
            elif exercise_type == "plank":
                exercise_data = self.detect_plank(results.pose_landmarks)
            elif exercise_type == "lunge":
                exercise_data = self.detect_lunge(results.pose_landmarks)
            elif exercise_type == "burpee":
                exercise_data = self.detect_burpee(results.pose_landmarks)
            elif exercise_type == "downward dog":
                exercise_data = self.detect_downward_dog(results.pose_landmarks)
            else:
                exercise_data = self.detect_stub(results.pose_landmarks)
            # Add visual feedback
            annotated_frame = self.add_visual_feedback(annotated_frame, exercise_data)
        else:
            annotated_frame = frame.copy()
        return annotated_frame, exercise_data
    
    def add_visual_feedback(self, frame: np.ndarray, exercise_data: Dict) -> np.ndarray:
        """Add visual feedback to the frame"""
        # Add rep counter
        cv2.putText(frame, f"Reps: {exercise_data['reps']}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Add state
        state_color = (0, 255, 0) if exercise_data['state'] == 'up' else (0, 165, 255)
        cv2.putText(frame, f"State: {exercise_data['state'].upper()}", (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, state_color, 2)
        
        # Add angle
        cv2.putText(frame, f"Angle: {exercise_data['angle']:.1f}°", (10, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Add form score
        form_score = exercise_data['form']['score']
        score_color = (0, 255, 0) if form_score >= 80 else (0, 165, 255) if form_score >= 60 else (0, 0, 255)
        cv2.putText(frame, f"Form Score: {form_score}", (10, 150),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, score_color, 2)
        
        return frame
    
    def reset_counter(self):
        """Reset the rep counter"""
        self.rep_count = 0
        self.exercise_state = "rest"
        self.last_rep_time = time.time()
    
    def get_exercise_stats(self) -> Dict:
        """Get current exercise statistics"""
        return {
            "reps": self.rep_count,
            "state": self.exercise_state,
            "exercise_type": self.exercise_type
        } 