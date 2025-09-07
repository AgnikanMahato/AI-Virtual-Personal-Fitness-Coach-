"""
Configuration file for AI Fitness Coach
Customize settings here for your preferences
"""

# Exercise Detection Settings
EXERCISE_CONFIG = {
    "pushup": {
        "down_threshold": 90,      # Angle threshold for down position
        "up_threshold": 160,       # Angle threshold for up position
        "rep_cooldown": 1.0,       # Seconds between rep counts
        "form_weight": 1.0         # Weight for form scoring
    },
    "squat": {
        "down_threshold": 70,      # Angle threshold for down position
        "up_threshold": 160,       # Angle threshold for up position
        "rep_cooldown": 1.0,       # Seconds between rep counts
        "form_weight": 1.0         # Weight for form scoring
    },
    "plank": {
        "down_threshold": 160,     # Angle threshold for down position
        "up_threshold": 180,       # Angle threshold for up position
        "rep_cooldown": 2.0,       # Seconds between rep counts
        "form_weight": 1.2         # Weight for form scoring (planks are harder)
    }
}

# MediaPipe Settings
MEDIAPIPE_CONFIG = {
    "min_detection_confidence": 0.5,    # Minimum confidence for pose detection
    "min_tracking_confidence": 0.5,     # Minimum confidence for pose tracking
    "model_complexity": 1,              # Model complexity (0, 1, or 2)
    "smooth_landmarks": True,           # Smooth landmark detection
    "enable_segmentation": False,       # Enable body segmentation
    "smooth_segmentation": True         # Smooth segmentation results
}

# Form Assessment Settings
FORM_CONFIG = {
    "posture_threshold": 160,           # Minimum angle for good posture
    "depth_threshold": 0.8,             # Minimum depth for exercise completion
    "stability_threshold": 0.1,         # Maximum movement variance for stability
    "score_weights": {
        "posture": 0.4,                 # Weight for posture scoring
        "depth": 0.3,                   # Weight for depth scoring
        "stability": 0.2,               # Weight for stability scoring
        "range": 0.1                    # Weight for range of motion scoring
    }
}

# Workout Tracking Settings
WORKOUT_CONFIG = {
    "auto_save": True,                  # Automatically save workout data
    "save_interval": 30,                # Save data every N seconds
    "max_workout_duration": 7200,       # Maximum workout duration in seconds (2 hours)
    "calorie_estimation": {
        "pushup": 5,                    # Calories per pushup
        "squat": 3,                     # Calories per squat
        "plank": 2                      # Calories per second of plank
    }
}

# UI Settings
UI_CONFIG = {
    "theme": "light",                   # UI theme (light/dark)
    "sidebar_state": "expanded",        # Sidebar initial state
    "page_title": "AI Fitness Coach",   # Page title
    "page_icon": "💪",                  # Page icon
    "layout": "wide",                   # Page layout
    "auto_refresh": True,               # Auto-refresh data
    "refresh_interval": 5               # Refresh interval in seconds
}

# Camera Settings
CAMERA_CONFIG = {
    "default_resolution": (640, 480),   # Default camera resolution
    "fps": 30,                         # Target frames per second
    "flip_horizontal": False,           # Flip camera horizontally
    "brightness": 0,                    # Camera brightness adjustment
    "contrast": 0                       # Camera contrast adjustment
}

# Data Storage Settings
STORAGE_CONFIG = {
    "log_file": "workout_logs.json",    # Workout log file name
    "backup_interval": 7,               # Backup data every N days
    "max_log_entries": 10000,           # Maximum log entries to keep
    "export_formats": ["csv", "json"],  # Supported export formats
    "auto_cleanup": True                # Automatically clean old data
}

# Performance Settings
PERFORMANCE_CONFIG = {
    "max_fps": 30,                      # Maximum processing FPS
    "frame_skip": 1,                    # Process every Nth frame
    "landmark_smoothing": True,         # Enable landmark smoothing
    "cache_size": 100,                  # Cache size for processed frames
    "parallel_processing": False        # Enable parallel processing
}

# Notification Settings
NOTIFICATION_CONFIG = {
    "enable_sound": True,               # Enable sound notifications
    "enable_visual": True,              # Enable visual notifications
    "workout_complete": True,           # Notify when workout is complete
    "milestone_reached": True,          # Notify when milestones are reached
    "form_warning": True                # Notify when form issues are detected
}

def get_config(section, key=None):
    """Get configuration value(s)"""
    if key is None:
        return globals().get(f"{section.upper()}_CONFIG", {})
    else:
        config = globals().get(f"{section.upper()}_CONFIG", {})
        return config.get(key)

def update_config(section, key, value):
    """Update configuration value"""
    config_name = f"{section.upper()}_CONFIG"
    if config_name in globals():
        globals()[config_name][key] = value
        return True
    return False

def reset_config():
    """Reset all configurations to defaults"""
    # This would reload the file or reset to hardcoded defaults
    pass 