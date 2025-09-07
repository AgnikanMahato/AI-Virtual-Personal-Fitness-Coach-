#!/usr/bin/env python3
"""
Quick Start Script for AI Fitness Coach
Provides easy access to all main features
"""

import os
import sys
import subprocess
import webbrowser
import time

def print_banner():
    """Print the application banner"""
    print("=" * 60)
    print("💪 AI Virtual Personal Fitness Coach")
    print("=" * 60)
    print("Your intelligent workout companion powered by AI")
    print("=" * 60)

def check_dependencies():
    """Check if required packages are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'opencv-python',
        'mediapipe', 
        'streamlit',
        'numpy',
        'pandas',
        'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def run_streamlit_app(app_type="photo"):
    """Run the Streamlit application"""
    app_file = "app.py" if app_type == "photo" else "realtime_app.py"
    app_name = "Photo-based" if app_type == "photo" else "Real-time"
    
    print(f"🚀 Starting {app_name} AI Fitness Coach...")
    print(f"📱 Opening browser automatically...")
    
    # Start Streamlit in background
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", app_file,
            "--server.port", "8501",
            "--server.headless", "true"
        ])
        
        # Wait a moment for Streamlit to start
        time.sleep(3)
        
        # Open browser
        webbrowser.open("http://localhost:8501")
        
        print(f"✅ {app_name} app is running!")
        print("🌐 App URL: http://localhost:8501")
        print("🔄 Press Ctrl+C to stop the application")
        
        # Keep the script running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping application...")
            process.terminate()
            process.wait()
            print("✅ Application stopped.")
        
    except Exception as e:
        print(f"❌ Failed to start {app_name} app: {e}")

def run_demo():
    """Run the demo script"""
    print("🎮 Starting demo mode...")
    
    try:
        subprocess.run([sys.executable, "demo.py"])
    except Exception as e:
        print(f"❌ Failed to run demo: {e}")

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    
    try:
        subprocess.run([sys.executable, "test_pose_detector.py"])
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")

def show_menu():
    """Show the main menu"""
    while True:
        print("\n🎯 Choose an option:")
        print("1. 📸 Photo-based AI Fitness Coach (Recommended for beginners)")
        print("2. 🎥 Real-time AI Fitness Coach (Live video processing)")
        print("3. 🎮 Demo Mode (Test functionality)")
        print("4. 🧪 Run Tests (Verify installation)")
        print("5. 📦 Install Dependencies")
        print("6. 📚 View README")
        print("7. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            run_streamlit_app("photo")
        elif choice == '2':
            run_streamlit_app("realtime")
        elif choice == '3':
            run_demo()
        elif choice == '4':
            run_tests()
        elif choice == '5':
            if install_dependencies():
                print("✅ Dependencies installed! You can now run the apps.")
            else:
                print("❌ Failed to install dependencies. Please check your Python environment.")
        elif choice == '6':
            if os.path.exists("README.md"):
                try:
                    with open("README.md", 'r') as f:
                        print("\n" + "="*60)
                        print("📚 README.md")
                        print("="*60)
                        print(f.read())
                        print("="*60)
                except Exception as e:
                    print(f"❌ Error reading README: {e}")
            else:
                print("❌ README.md not found")
        elif choice == '7':
            print("👋 Thanks for using AI Fitness Coach!")
            print("💪 Stay fit and healthy!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def main():
    """Main function"""
    print_banner()
    
    # Check if we're in the right directory
    if not os.path.exists("pose_detector.py"):
        print("❌ Error: pose_detector.py not found!")
        print("Please run this script from the AI_Fitness_Coach directory.")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 Would you like to install the missing dependencies? (y/n)")
        install_choice = input().strip().lower()
        
        if install_choice == 'y':
            if not install_dependencies():
                print("❌ Failed to install dependencies. Please install them manually.")
                return
        else:
            print("⚠️  Some features may not work without the required dependencies.")
    
    print("\n🎉 AI Fitness Coach is ready to use!")
    
    # Show main menu
    show_menu()

if __name__ == "__main__":
    main() 