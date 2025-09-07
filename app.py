import streamlit as st
import cv2
import numpy as np
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from pose_detector import PoseDetector
from workout_logger import WorkoutLogger

# Page configuration
st.set_page_config(
    page_title="AI Fitness Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'pose_detector' not in st.session_state:
    st.session_state.pose_detector = PoseDetector()
if 'workout_logger' not in st.session_state:
    st.session_state.workout_logger = WorkoutLogger()
if 'workout_start_time' not in st.session_state:
    st.session_state.workout_start_time = None
if 'is_workout_active' not in st.session_state:
    st.session_state.is_workout_active = False
if 'current_exercise' not in st.session_state:
    st.session_state.current_exercise = "pushup"

# Initialize camera
cap = cv2.VideoCapture(0)

def main():
    # Header
    st.title("💪 AI Virtual Personal Fitness Coach")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🏋️ Exercise Settings")
        # Expanded exercise and yoga list
        EXERCISE_LIST = [
            "pushup", "squat", "plank", "lunge", "burpee", "mountain climber",
            "jumping jack", "crunch", "bicep curl", "tricep dip", "shoulder press",
            # Yoga poses
            "downward dog", "warrior I", "warrior II", "tree pose", "cobra pose",
            "child's pose", "cat-cow", "bridge pose", "seated twist", "triangle pose"
        ]
        if st.session_state.current_exercise not in EXERCISE_LIST:
            st.session_state.current_exercise = EXERCISE_LIST[0]
        exercise_type = st.selectbox(
            "Choose Exercise or Yoga Pose:",
            EXERCISE_LIST,
            index=EXERCISE_LIST.index(st.session_state.current_exercise)
        )
        if exercise_type != st.session_state.current_exercise:
            st.session_state.current_exercise = exercise_type
            st.session_state.pose_detector.reset_counter()
        
        st.markdown("---")
        st.header("📊 Workout Stats")
        
        # Display current stats
        stats = st.session_state.pose_detector.get_exercise_stats()
        st.metric("Current Reps", stats["reps"])
        st.metric("Exercise State", stats["state"].upper())
        
        # Workout controls
        st.markdown("---")
        st.header("⏱️ Workout Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Start Workout", type="primary"):
                start_workout()
        
        with col2:
            if st.button("Stop Workout"):
                stop_workout()
        
        if st.button("Reset Counter"):
            st.session_state.pose_detector.reset_counter()
            st.rerun()
        
        # Display workout timer
        if st.session_state.is_workout_active and st.session_state.workout_start_time:
            elapsed_time = time.time() - st.session_state.workout_start_time
            st.metric("Workout Time", f"{elapsed_time:.0f}s")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎥 Live Pose Detection")
        
        # Camera input
        camera_input = st.camera_input("Take a photo for pose detection")
        
        if camera_input is not None:
            # Convert to OpenCV format
            bytes_data = camera_input.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            # Process frame
            processed_frame, exercise_data = st.session_state.pose_detector.process_frame(
                cv2_img, st.session_state.current_exercise
            )
            
            # Convert back to display format
            processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            st.image(processed_frame_rgb, caption="Processed Frame with Pose Detection", use_column_width=True)
            
            # Display exercise data
            st.subheader("📈 Exercise Data")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("Reps", exercise_data["reps"])
            with col_b:
                st.metric("State", exercise_data["state"].upper())
            with col_c:
                st.metric("Angle", f"{exercise_data['angle']:.1f}°")
            
            # Form feedback
            st.subheader("🎯 Form Assessment")
            form_score = exercise_data["form"]["score"]
            
            if form_score >= 80:
                st.success(f"Excellent form! Score: {form_score}/100")
            elif form_score >= 60:
                st.warning(f"Good form, but room for improvement. Score: {form_score}/100")
            else:
                st.error(f"Form needs work. Score: {form_score}/100")
            
            if exercise_data["form"]["issues"]:
                st.error("Issues detected:")
                for issue in exercise_data["form"]["issues"]:
                    st.write(f"• {issue}")
            
            if exercise_data["form"]["tips"]:
                st.info("Tips for improvement:")
                for tip in exercise_data["form"]["tips"]:
                    st.write(f"• {tip}")
    
    with col2:
        st.header("📊 Progress Dashboard")
        
        # Weekly summary
        weekly_summary = st.session_state.workout_logger.get_weekly_summary()
        st.subheader("📅 This Week")
        st.metric("Workouts", weekly_summary["workouts_this_week"])
        st.metric("Total Reps", weekly_summary["total_reps_this_week"])
        st.metric("Duration", f"{weekly_summary['total_duration_this_week']} min")
        st.metric("Avg Form", f"{weekly_summary['avg_form_score_this_week']}/100")
        
        # Recent workouts
        st.subheader("🕒 Recent Workouts")
        recent_workouts = st.session_state.workout_logger.get_recent_workouts(days=7)
        
        if recent_workouts:
            for workout in recent_workouts[-5:]:  # Show last 5
                workout_date = datetime.fromisoformat(workout["timestamp"]).strftime("%m/%d")
                st.write(f"**{workout_date}**: {workout['exercise_type'].title()} - {workout['reps']} reps")
        else:
            st.info("No recent workouts")
    
    # Progress charts
    st.markdown("---")
    st.header("📈 Progress Charts")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Reps Progress (Last 30 Days)")
        progress_data = st.session_state.workout_logger.get_progress_data(
            st.session_state.current_exercise, days=30
        )
        
        if progress_data:
            dates = list(progress_data.keys())
            reps = [progress_data[date]["reps"] for date in dates]
            
            fig = px.line(
                x=dates, 
                y=reps,
                title=f"{st.session_state.current_exercise.title()} Reps Over Time"
            )
            fig.update_layout(xaxis_title="Date", yaxis_title="Reps")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No progress data available")
    
    with col_chart2:
        st.subheader("Form Score Progress (Last 30 Days)")
        if progress_data:
            form_scores = [progress_data[date]["form_score"] for date in dates]
            
            fig = px.line(
                x=dates, 
                y=form_scores,
                title=f"{st.session_state.current_exercise.title()} Form Score Over Time"
            )
            fig.update_layout(xaxis_title="Date", yaxis_title="Form Score")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No progress data available")
    
    # Workout history table
    st.markdown("---")
    st.header("📋 Workout History")
    
    if st.button("Export to CSV"):
        filename = st.session_state.workout_logger.export_to_csv()
        st.success(f"Workout data exported to {filename}")
    
    # Display workout history
    all_workouts = st.session_state.workout_logger.logs
    
    if all_workouts:
        # Convert to DataFrame for better display
        df = pd.DataFrame(all_workouts)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        
        # Reorder columns for better display
        display_df = df[['date', 'exercise_type', 'reps', 'duration_minutes', 'form_score', 'calories_estimate']]
        display_df.columns = ['Date', 'Exercise', 'Reps', 'Duration (min)', 'Form Score', 'Calories']
        
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No workout history available")

def start_workout():
    """Start a new workout session"""
    st.session_state.workout_start_time = time.time()
    st.session_state.is_workout_active = True
    st.session_state.pose_detector.reset_counter()
    st.rerun()

def stop_workout():
    """Stop the current workout and log it"""
    if st.session_state.is_workout_active and st.session_state.workout_start_time:
        # Calculate workout duration
        duration = time.time() - st.session_state.workout_start_time
        
        # Get final stats
        stats = st.session_state.pose_detector.get_exercise_stats()
        
        # Log the workout
        workout_entry = st.session_state.workout_logger.log_workout(
            exercise_type=st.session_state.current_exercise,
            reps=stats["reps"],
            duration=duration,
            form_score=100,  # Placeholder - could be improved
            calories_estimate=stats["reps"] * 5  # Rough estimate
        )
        
        # Reset workout state
        st.session_state.is_workout_active = False
        st.session_state.workout_start_time = None
        
        st.success(f"Workout completed! {stats['reps']} reps in {duration/60:.1f} minutes")
        st.rerun()

if __name__ == "__main__":
    main()