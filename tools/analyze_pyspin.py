#!/usr/bin/env python3
"""
Comprehensive PySpin Analysis Tool
Check what's available in the PySpin module and fix camera detection
"""

import sys

def analyze_pyspin():
    """Analyze PySpin module to understand available attributes"""
    print("🔍 Analyzing PySpin module...")
    
    try:
        import PySpin
        print("✅ PySpin imported successfully")
        
        # Check version
        version = getattr(PySpin, '__version__', 'Unknown')
        print(f"📋 PySpin version: {version}")
        
        # List all available attributes
        print("\n📋 Available PySpin attributes:")
        attributes = [attr for attr in dir(PySpin) if not attr.startswith('_')]
        
        # Group attributes by type
        classes = []
        functions = []
        constants = []
        other = []
        
        for attr in attributes:
            obj = getattr(PySpin, attr)
            if isinstance(obj, type):
                classes.append(attr)
            elif callable(obj):
                functions.append(attr)
            elif isinstance(obj, (int, float, str)):
                constants.append(attr)
            else:
                other.append(attr)
        
        print(f"\n🏗️  Classes ({len(classes)}):")
        for cls in sorted(classes)[:10]:  # Show first 10
            print(f"  - {cls}")
        if len(classes) > 10:
            print(f"  ... and {len(classes) - 10} more")
        
        print(f"\n⚙️  Functions ({len(functions)}):")
        for func in sorted(functions):
            print(f"  - {func}")
        
        print(f"\n🔢 Constants ({len(constants)}):")
        for const in sorted(constants)[:10]:  # Show first 10
            print(f"  - {const}")
        if len(constants) > 10:
            print(f"  ... and {len(constants) - 10} more")
        
        print(f"\n📦 Other ({len(other)}):")
        for item in sorted(other):
            print(f"  - {item}")
        
        # Check specifically for System
        print(f"\n🎯 System-related attributes:")
        system_attrs = [attr for attr in attributes if 'System' in attr.lower()]
        for attr in system_attrs:
            print(f"  - {attr}")
            obj = getattr(PySpin, attr)
            print(f"    Type: {type(obj)}")
            if hasattr(obj, '__doc__') and obj.__doc__:
                print(f"    Doc: {obj.__doc__[:100]}...")
        
        # Try to find camera-related classes
        print(f"\n📷 Camera-related classes:")
        camera_classes = [attr for attr in classes if 'Camera' in attr]
        for cls in camera_classes:
            print(f"  - {cls}")
        
        return True
        
    except ImportError as e:
        print(f"❌ PySpin import failed: {e}")
        return False

def test_camera_detection_alternatives():
    """Test alternative methods for camera detection"""
    print("\n🔧 Testing alternative camera detection methods...")
    
    try:
        import PySpin
        
        # Method 1: Try direct System class instantiation
        print("\n1️⃣ Testing direct System instantiation:")
        try:
            system = PySpin.System()
            print("✅ PySpin.System() works")
            
            # Try to get cameras
            try:
                cameras = system.GetCameras()
                print(f"✅ Found {cameras.GetSize()} cameras")
                cameras.Clear()
                return True
            except Exception as e:
                print(f"❌ GetCameras failed: {e}")
                
        except Exception as e:
            print(f"❌ PySpin.System() failed: {e}")
        
        # Method 2: Try System singleton pattern
        print("\n2️⃣ Testing System singleton pattern:")
        try:
            if hasattr(PySpin, 'SystemInstance'):
                system = PySpin.SystemInstance()
                print("✅ PySpin.SystemInstance() works")
            elif hasattr(PySpin, 'GetSystemInstance'):
                system = PySpin.GetSystemInstance()
                print("✅ PySpin.GetSystemInstance() works")
            else:
                print("❌ No System instance method found")
                return False
                
            # Try to get cameras
            try:
                cameras = system.GetCameras()
                print(f"✅ Found {cameras.GetSize()} cameras")
                cameras.Clear()
                return True
            except Exception as e:
                print(f"❌ GetCameras failed: {e}")
                
        except Exception as e:
            print(f"❌ System singleton failed: {e}")
        
        # Method 3: Try camera enumeration
        print("\n3️⃣ Testing camera enumeration:")
        try:
            # Look for camera list or enumeration
            if hasattr(PySpin, 'CameraList'):
                cameras = PySpin.CameraList()
                print("✅ PySpin.CameraList() works")
            elif hasattr(PySpin, 'GetCameraList'):
                cameras = PySpin.GetCameraList()
                print("✅ PySpin.GetCameraList() works")
            else:
                print("❌ No camera list method found")
                
        except Exception as e:
            print(f"❌ Camera enumeration failed: {e}")
        
        return False
        
    except Exception as e:
        print(f"❌ Alternative testing failed: {e}")
        return False

def main():
    """Main analysis function"""
    print("🚀 PySpin Comprehensive Analysis Tool")
    print("=" * 60)
    
    # Analyze PySpin
    if not analyze_pyspin():
        print("\n❌ Cannot proceed without PySpin")
        return False
    
    # Test alternatives
    if test_camera_detection_alternatives():
        print("\n✅ Found working camera detection method!")
        return True
    else:
        print("\n❌ No working camera detection method found")
        print("\n🔧 Possible solutions:")
        print("1. Check FLIR Spinnaker SDK installation")
        print("2. Ensure Python bindings are properly installed")
        print("3. Try different PySpin version")
        print("4. Check camera connections")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
