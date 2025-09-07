import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

class WorkoutLogger:
    def __init__(self, log_file: str = "workout_logs.json"):
        """Initialize workout logger"""
        self.log_file = log_file
        self.logs = self.load_logs()
        
    def load_logs(self) -> List[Dict]:
        """Load existing workout logs from file"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_logs(self):
        """Save workout logs to file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2)
    
    def log_workout(self, exercise_type: str, reps: int, duration: float, 
                   form_score: float, calories_estimate: float = 0):
        """Log a completed workout session"""
        workout_entry = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "exercise_type": exercise_type,
            "reps": reps,
            "duration_minutes": round(duration / 60, 2),
            "form_score": form_score,
            "calories_estimate": calories_estimate
        }
        
        self.logs.append(workout_entry)
        self.save_logs()
        
        return workout_entry
    
    def get_recent_workouts(self, days: int = 7) -> List[Dict]:
        """Get workouts from the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_workouts = []
        
        for workout in self.logs:
            workout_date = datetime.fromisoformat(workout["timestamp"])
            if workout_date >= cutoff_date:
                recent_workouts.append(workout)
        
        return recent_workouts
    
    def get_exercise_stats(self, exercise_type: str = None, days: int = 30) -> Dict:
        """Get statistics for exercises"""
        cutoff_date = datetime.now() - timedelta(days=days)
        filtered_workouts = []
        
        for workout in self.logs:
            workout_date = datetime.fromisoformat(workout["timestamp"])
            if workout_date >= cutoff_date:
                if exercise_type is None or workout["exercise_type"] == exercise_type:
                    filtered_workouts.append(workout)
        
        if not filtered_workouts:
            return {
                "total_workouts": 0,
                "total_reps": 0,
                "total_duration": 0,
                "avg_form_score": 0,
                "best_form_score": 0,
                "total_calories": 0
            }
        
        total_reps = sum(w["reps"] for w in filtered_workouts)
        total_duration = sum(w["duration_minutes"] for w in filtered_workouts)
        form_scores = [w["form_score"] for w in filtered_workouts]
        total_calories = sum(w["calories_estimate"] for w in filtered_workouts)
        
        return {
            "total_workouts": len(filtered_workouts),
            "total_reps": total_reps,
            "total_duration": round(total_duration, 2),
            "avg_form_score": round(sum(form_scores) / len(form_scores), 1),
            "best_form_score": max(form_scores),
            "total_calories": round(total_calories, 1)
        }
    
    def get_progress_data(self, exercise_type: str, days: int = 30) -> Dict:
        """Get progress data for plotting"""
        cutoff_date = datetime.now() - timedelta(days=days)
        progress_data = {}
        
        for workout in self.logs:
            workout_date = datetime.fromisoformat(workout["timestamp"])
            if workout_date >= cutoff_date and workout["exercise_type"] == exercise_type:
                date_str = workout["date"]
                if date_str not in progress_data:
                    progress_data[date_str] = {
                        "reps": 0,
                        "duration": 0,
                        "form_score": 0,
                        "count": 0
                    }
                
                progress_data[date_str]["reps"] += workout["reps"]
                progress_data[date_str]["duration"] += workout["duration_minutes"]
                progress_data[date_str]["form_score"] += workout["form_score"]
                progress_data[date_str]["count"] += 1
        
        # Calculate averages
        for date_str in progress_data:
            count = progress_data[date_str]["count"]
            progress_data[date_str]["form_score"] = round(
                progress_data[date_str]["form_score"] / count, 1
            )
        
        return progress_data
    
    def export_to_csv(self, filename: str = None):
        """Export workout logs to CSV"""
        if filename is None:
            filename = f"workout_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df = pd.DataFrame(self.logs)
        df.to_csv(filename, index=False)
        return filename
    
    def get_weekly_summary(self) -> Dict:
        """Get summary of current week's workouts"""
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        
        weekly_workouts = []
        for workout in self.logs:
            workout_date = datetime.fromisoformat(workout["timestamp"])
            if workout_date >= start_of_week:
                weekly_workouts.append(workout)
        
        if not weekly_workouts:
            return {
                "workouts_this_week": 0,
                "total_reps_this_week": 0,
                "total_duration_this_week": 0,
                "avg_form_score_this_week": 0
            }
        
        total_reps = sum(w["reps"] for w in weekly_workouts)
        total_duration = sum(w["duration_minutes"] for w in weekly_workouts)
        form_scores = [w["form_score"] for w in weekly_workouts]
        
        return {
            "workouts_this_week": len(weekly_workouts),
            "total_reps_this_week": total_reps,
            "total_duration_this_week": round(total_duration, 2),
            "avg_form_score_this_week": round(sum(form_scores) / len(form_scores), 1)
        }
    
    def clear_logs(self):
        """Clear all workout logs"""
        self.logs = []
        self.save_logs() 