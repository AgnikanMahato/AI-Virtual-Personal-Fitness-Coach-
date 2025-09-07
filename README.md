# 💪 AI Virtual Personal Fitness Coach

An intelligent fitness application that uses computer vision to detect workout poses, count repetitions, and provide real-time form feedback using MediaPipe and OpenCV.

## 🎯 Features

- **Real-time Pose Detection**: Uses MediaPipe to detect body landmarks and track movement
- **Exercise Recognition**: Supports pushups and squats with accurate rep counting
- **Form Assessment**: Provides real-time feedback on exercise form and technique
- **Workout Tracking**: Logs workout sessions with detailed statistics
- **Progress Visualization**: Interactive charts showing progress over time
- **Multiple Interfaces**: Both photo-based and real-time video processing options

## 🛠️ Technology Stack

- **Python 3.8+**
- **OpenCV**: Computer vision and image processing
- **MediaPipe**: Pose detection and body landmark tracking
- **Streamlit**: Web application framework
- **Streamlit-WebRTC**: Real-time video processing
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Webcam for real-time functionality
- Modern web browser

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI_Fitness_Coach
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Option 1: Photo-based Pose Detection (Recommended for beginners)

Run the main application:
```bash
streamlit run e:/PROJECTS/.AI_Fitness_Coach/realtime_app.py
```

This version allows you to:
- Take photos for pose analysis
- Get instant feedback on form
- Track reps and workout progress
- View detailed statistics and charts

### Option 2: Real-time Video Processing

For continuous pose detection:
```bash
streamlit run realtime_app.py
```

This version provides:
- Live video feed with real-time pose detection
- Continuous rep counting during workouts
- Instant form feedback
- Seamless workout tracking

## 🏋️ Supported Exercises

### Pushups
- **Detection**: Tracks elbow angles and body alignment
- **Form Check**: Ensures straight body line and proper depth
- **Rep Counting**: Counts complete up-down cycles

### Squats
- **Detection**: Monitors knee angles and hip movement
- **Form Check**: Verifies proper depth and knee alignment
- **Rep Counting**: Tracks squat depth and return to standing

## 📊 Features Overview

### Real-time Pose Detection
- Body landmark identification using MediaPipe
- Joint angle calculations for exercise analysis
- Movement state tracking (rest, down, up)

### Form Assessment
- Posture alignment verification
- Exercise depth monitoring
- Real-time feedback and tips
- Form scoring system (0-100)

### Workout Tracking
- Session duration monitoring
- Rep counting with cooldown protection
- Calorie estimation
- Progress tracking over time

### Data Management
- Automatic workout logging
- CSV export functionality
- Progress visualization charts
- Weekly and monthly summaries

## 🎮 How to Use

1. **Choose Exercise**: Select between pushups or squats
2. **Start Workout**: Click "Start Workout" to begin tracking
3. **Perform Exercise**: Follow the on-screen guidance
4. **Monitor Progress**: Watch real-time stats and form feedback
5. **Complete Session**: Click "Stop Workout" to log your session
6. **Review Progress**: Check charts and statistics

## 📈 Understanding the Metrics

### Form Score (0-100)
- **80-100**: Excellent form
- **60-79**: Good form with room for improvement
- **Below 60**: Form needs work

### Exercise States
- **Rest**: Starting position
- **Down**: Exercise bottom position
- **Up**: Exercise top position

### Rep Counting
- Counts complete exercise cycles
- Includes cooldown to prevent double-counting
- Tracks total reps per session

## 🔧 Configuration

### Exercise Thresholds
You can adjust exercise detection sensitivity by modifying the angle thresholds in `pose_detector.py`:

```python
self.angle_thresholds = {
    "pushup": {"down": 90, "up": 160},
    "squat": {"down": 70, "up": 160},
    "plank": {"down": 160, "up": 180}
}
```

### Rep Cooldown
Adjust the time between rep counts to prevent false positives:
```python
self.rep_cooldown = 1.0  # seconds between reps
```

## 📁 Project Structure

```
AI_Fitness_Coach/
├── app.py                 # Main photo-based application
├── realtime_app.py        # Real-time video processing app
├── pose_detector.py       # Core pose detection logic
├── workout_logger.py      # Workout tracking and logging
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── workout_logs.json     # Workout data storage (auto-generated)
```

## 🚨 Troubleshooting

### Common Issues

1. **Camera not working**
   - Ensure camera permissions are granted
   - Check if another application is using the camera
   - Try refreshing the browser page

2. **Pose detection not accurate**
   - Ensure good lighting conditions
   - Position yourself clearly in the camera view
   - Maintain proper distance from camera

3. **Rep counting issues**
   - Perform exercises with clear, deliberate movements
   - Ensure full range of motion
   - Check exercise type selection

### Performance Tips

- Use the photo-based version for initial testing
- Ensure stable internet connection for real-time version
- Close unnecessary browser tabs for better performance
- Use modern browsers (Chrome, Firefox, Safari)

## 🔮 Future Enhancements

- [ ] Additional exercise types (planks, lunges, burpees)
- [ ] Advanced form analysis with machine learning
- [ ] Personalized workout recommendations
- [ ] Social features and challenges
- [ ] Mobile app version
- [ ] Integration with fitness trackers
- [ ] Voice feedback and coaching

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- MediaPipe team for pose detection technology
- Streamlit for the web application framework
- OpenCV community for computer vision tools
- All contributors and users of this project

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Open an issue on the project repository
4. Check the MediaPipe and Streamlit documentation

---

**Happy Training! 💪 Stay fit and healthy! 🏃‍♂️** 