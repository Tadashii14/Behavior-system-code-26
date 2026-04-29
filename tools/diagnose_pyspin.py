#!/usr/bin/env python3
"""
PySpin Installation Diagnostic Tool
Check PySpin installation and provide fix recommendations
"""

import sys
import os
import importlib.util

def check_pyspin_file():
    """Check the actual PySpin file location and content"""
    print("🔍 Checking PySpin file location...")
    
    try:
        import PySpin
        spec = importlib.util.find_spec("PySpin")
        if spec and spec.origin:
            print(f"📁 PySpin location: {spec.origin}")
            
            # Check file size
            if os.path.exists(spec.origin):
                size = os.path.getsize(spec.origin)
                print(f"📏 File size: {size} bytes")
                
                if size < 1000:  # Less than 1KB suggests incomplete installation
                    print("⚠️  PySpin file is very small - incomplete installation")
                    return False
                elif size < 10000:  # Less than 10KB suggests stub file
                    print("⚠️  PySpin file is small - might be a stub file")
                    return False
                else:
                    print("✅ PySpin file size looks reasonable")
                    return True
            else:
                print("❌ PySpin file not found")
                return False
        else:
            print("❌ Could not find PySpin spec")
            return False
            
    except Exception as e:
        print(f"❌ Error checking PySpin file: {e}")
        return False

def check_pyspin_content():
    """Check PySpin module content"""
    print("\n🔍 Checking PySpin module content...")
    
    try:
        import PySpin
        
        # Check if it's a stub or real module
        module_content = dir(PySpin)
        print(f"📋 Total attributes: {len(module_content)}")
        
        if len(module_content) < 10:
            print("⚠️  Very few attributes - likely incomplete installation")
            
            # Show what we have
            print("Available attributes:")
            for attr in module_content:
                if not attr.startswith('_'):
                    print(f"  - {attr}")
            return False
        else:
            print("✅ Good number of attributes")
            
            # Check for key FLIR classes
            key_classes = ['System', 'Camera', 'Image', 'PixelFormat']
            found_classes = []
            for cls in key_classes:
                if hasattr(PySpin, cls):
                    found_classes.append(cls)
            
            print(f"📷 Found key classes: {found_classes}")
            return len(found_classes) > 0
            
    except Exception as e:
        print(f"❌ Error checking PySpin content: {e}")
        return False

def check_flir_installation_paths():
    """Check FLIR installation paths"""
    print("\n🔍 Checking FLIR installation paths...")
    
    possible_paths = [
        r"C:\Program Files\FLIR Systems\Spinnaker",
        r"C:\Program Files (x86)\FLIR Systems\Spinnaker",
        r"C:\FLIR Systems\Spinnaker",
    ]
    
    found_paths = []
    for path in possible_paths:
        if os.path.exists(path):
            found_paths.append(path)
            print(f"✅ Found: {path}")
            
            # Check for Python bindings
            python_path = os.path.join(path, "Development", "bin", "Python")
            if os.path.exists(python_path):
                print(f"  🐍 Python bindings: {python_path}")
                
                # List Python files
                try:
                    python_files = [f for f in os.listdir(python_path) if f.endswith('.py')]
                    print(f"  📄 Python files: {python_files}")
                except Exception as e:
                    print(f"  ❌ Error listing Python files: {e}")
            else:
                print(f"  ❌ No Python bindings found")
    
    if not found_paths:
        print("❌ No FLIR Spinnaker installation found")
        return False
    
    return True

def check_python_path():
    """Check Python path for FLIR"""
    print("\n🔍 Checking Python path...")
    
    flir_in_path = False
    for path in sys.path:
        if 'FLIR' in path or 'Spinnaker' in path:
            print(f"✅ FLIR path in sys.path: {path}")
            flir_in_path = True
    
    if not flir_in_path:
        print("❌ No FLIR path found in sys.path")
        print("🔧 Try adding FLIR path to Python path")
        return False
    
    return True

def provide_solution():
    """Provide solution recommendations"""
    print("\n🔧 SOLUTION RECOMMENDATIONS:")
    print("=" * 50)
    
    print("\n1️⃣ REINSTALL FLIR SPINNAKER SDK:")
    print("   - Download latest version from FLIR website")
    print("   - Run installer as Administrator")
    print("   - Select 'Custom' installation")
    print("   - IMPORTANT: Check 'Python Bindings' option")
    print("   - Complete installation")
    
    print("\n2️⃣ VERIFY INSTALLATION:")
    print("   - Check: C:\\Program Files\\FLIR Systems\\Spinnaker\\Development\\bin\\Python")
    print("   - Should contain PySpin.py and PySpin.dll")
    
    print("\n3️⃣ TEST INSTALLATION:")
    print("   - Open new Command Prompt")
    print("   - Run: python -c \"import PySpin; print(dir(PySpin))\"")
    print("   - Should show many FLIR classes and functions")
    
    print("\n4️⃣ ALTERNATIVE - MANUAL INSTALLATION:")
    print("   - Find PySpin files in FLIR installation")
    print("   - Copy to Python site-packages")
    print("   - Add FLIR Python path to environment variables")

def main():
    """Main diagnostic function"""
    print("🚀 PySpin Installation Diagnostic Tool")
    print("=" * 50)
    
    # Run all checks
    checks = [
        ("PySpin File Check", check_pyspin_file),
        ("PySpin Content Check", check_pyspin_content),
        ("FLIR Installation Check", check_flir_installation_paths),
        ("Python Path Check", check_python_path),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print(f"\n{'='*20} SUMMARY {'='*20}")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Checks passed: {passed}/{total}")
    
    if passed < total:
        print("\n❌ ISSUES FOUND - PySpin installation is incomplete")
        provide_solution()
        return False
    else:
        print("\n✅ All checks passed - PySpin installation looks good")
        return False  # Still need to fix the camera detection

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
