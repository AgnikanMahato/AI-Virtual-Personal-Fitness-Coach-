#!/usr/bin/env python3
"""
Simple test script for PoseDetector class
"""

import numpy as np
from pose_detector import PoseDetector

def test_angle_calculation():
    """Test angle calculation function"""
    print("🧮 Testing angle calculation...")
    
    detector = PoseDetector()
    
    # Test with simple coordinates
    a = np.array([0, 0])
    b = np.array([1, 0])
    c = np.array([1, 1])
    
    angle = detector.calculate_angle(a, b, c)
    expected = 90.0
    
    print(f"   Test 1: Angle between (0,0), (1,0), (1,1) = {angle:.1f}° (expected: {expected}°)")
    assert abs(angle - expected) < 0.1, f"Angle calculation failed: got {angle}, expected {expected}"
    
    # Test with different coordinates
    a = np.array([0, 0])
    b = np.array([0, 0])
    c = np.array([1, 0])
    
    angle = detector.calculate_angle(a, b, c)
    print(f"   Test 2: Angle between (0,0), (0,0), (1,0) = {angle:.1f}°")
    
    print("✅ Angle calculation tests passed!")

def test_pose_detector_initialization():
    """Test PoseDetector initialization"""
    print("🔧 Testing PoseDetector initialization...")
    
    try:
        detector = PoseDetector()
        print(f"   ✅ PoseDetector initialized successfully")
        print(f"   ✅ Exercise type: {detector.exercise_type}")
        print(f"   ✅ Rep count: {detector.rep_count}")
        print(f"   ✅ Exercise state: {detector.exercise_state}")
        print(f"   ✅ Angle thresholds: {detector.angle_thresholds}")
    except Exception as e:
        print(f"   ❌ Initialization failed: {e}")
        return False
    
    return True

def test_exercise_thresholds():
    """Test exercise threshold configurations"""
    print("📏 Testing exercise thresholds...")
    
    detector = PoseDetector()
    
    # Test pushup thresholds
    pushup_thresholds = detector.angle_thresholds["pushup"]
    assert "down" in pushup_thresholds, "Pushup down threshold missing"
    assert "up" in pushup_thresholds, "Pushup up threshold missing"
    assert pushup_thresholds["down"] < pushup_thresholds["up"], "Pushup thresholds invalid"
    
    print(f"   ✅ Pushup thresholds: down={pushup_thresholds['down']}°, up={pushup_thresholds['up']}°")
    
    # Test squat thresholds
    squat_thresholds = detector.angle_thresholds["squat"]
    assert "down" in squat_thresholds, "Squat down threshold missing"
    assert "up" in squat_thresholds, "Squat up threshold missing"
    assert squat_thresholds["down"] < squat_thresholds["up"], "Squat thresholds invalid"
    
    print(f"   ✅ Squat thresholds: down={squat_thresholds['down']}°, up={squat_thresholds['up']}°")
    
    print("✅ Exercise threshold tests passed!")

def test_reset_functionality():
    """Test reset functionality"""
    print("🔄 Testing reset functionality...")
    
    detector = PoseDetector()
    
    # Modify some values
    detector.rep_count = 10
    detector.exercise_state = "down"
    
    print(f"   Before reset: reps={detector.rep_count}, state={detector.exercise_state}")
    
    # Reset
    detector.reset_counter()
    
    print(f"   After reset: reps={detector.rep_count}, state={detector.exercise_state}")
    
    assert detector.rep_count == 0, "Rep count not reset to 0"
    assert detector.exercise_state == "rest", "Exercise state not reset to rest"
    
    print("✅ Reset functionality tests passed!")

def test_form_assessment():
    """Test form assessment functionality"""
    print("🎯 Testing form assessment...")
    
    detector = PoseDetector()
    
    # Test with no landmarks
    form_data = detector.assess_form(None)
    
    assert form_data["score"] == 0, "Form score should be 0 with no landmarks"
    assert "No person detected" in form_data["issues"], "Should detect no person issue"
    
    print("   ✅ Form assessment with no landmarks works")
    
    # Test form assessment structure
    required_keys = ["score", "issues", "tips"]
    for key in required_keys:
        assert key in form_data, f"Form data missing key: {key}"
    
    print("   ✅ Form assessment structure correct")
    
    print("✅ Form assessment tests passed!")

def main():
    """Run all tests"""
    print("🧪 Running PoseDetector tests...")
    print("=" * 50)
    
    tests = [
        test_angle_calculation,
        test_pose_detector_initialization,
        test_exercise_thresholds,
        test_reset_functionality,
        test_form_assessment
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Test {test.__name__} failed")
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! PoseDetector is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    main() 