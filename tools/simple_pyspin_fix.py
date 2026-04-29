#!/usr/bin/env python3
"""
Simple FLIR Python Bindings Fix
Target only the essential PySpin files
"""

import os
import sys
import shutil
import site

def find_pyspin_files():
    """Find only the essential PySpin files"""
    print("🔍 Searching for PySpin files...")
    
    search_paths = [
        r"C:\Program Files\FLIR Systems\Spinnaker\Development\bin\Python",
        r"C:\Program Files (x86)\FLIR Systems\Spinnaker\Development\bin\Python",
        r"C:\Program Files\FLIR Systems\Spinnaker\Python",
        r"C:\Program Files (x86)\FLIR Systems\Spinnaker\Python",
    ]
    
    pyspin_files = []
    
    for path in search_paths:
        if os.path.exists(path):
            print(f"📁 Checking: {path}")
            
            # Look for PySpin files
            for file in os.listdir(path):
                if 'pyspin' in file.lower() or file.endswith('.py'):
                    file_path = os.path.join(path, file)
                    pyspin_files.append(file_path)
                    print(f"  🐍 Found: {file}")
    
    return pyspin_files

def copy_pyspin_files(pyspin_files):
    """Copy PySpin files to site-packages"""
    print(f"\n📦 Copying {len(pyspin_files)} PySpin files...")
    
    # Get site-packages path
    site_packages = site.getsitepackages()[0]
    print(f"📁 Target: {site_packages}")
    
    copied = 0
    
    for file_path in pyspin_files:
        try:
            dest = os.path.join(site_packages, os.path.basename(file_path))
            shutil.copy2(file_path, dest)
            print(f"✅ Copied: {os.path.basename(file_path)}")
            copied += 1
        except Exception as e:
            print(f"❌ Failed to copy {os.path.basename(file_path)}: {e}")
    
    return copied

def test_pyspin():
    """Test PySpin import"""
    print("\n🧪 Testing PySpin import...")
    
    try:
        # Clear module cache
        if 'PySpin' in sys.modules:
            del sys.modules['PySpin']
        
        import PySpin
        print("✅ PySpin imported!")
        
        # Check attributes
        attrs = [a for a in dir(PySpin) if not a.startswith('_')]
        print(f"📋 PySpin has {len(attrs)} public attributes")
        
        if len(attrs) > 10:
            print("✅ PySpin looks properly installed!")
            return True
        else:
            print("❌ PySpin still has very few attributes")
            return False
            
    except ImportError as e:
        print(f"❌ PySpin import failed: {e}")
        return False

def main():
    """Main fix function"""
    print("🚀 Simple FLIR Python Bindings Fix")
    print("=" * 40)
    
    # Find PySpin files
    pyspin_files = find_pyspin_files()
    
    if not pyspin_files:
        print("\n❌ No PySpin files found")
        print("🔧 FLIR Python bindings are not installed")
        print("📋 Please reinstall FLIR Spinnaker SDK with Python bindings")
        return False
    
    # Copy files
    copied = copy_pyspin_files(pyspin_files)
    
    if copied == 0:
        print("\n❌ No files were copied")
        return False
    
    print(f"\n✅ Copied {copied} files")
    
    # Test
    if test_pyspin():
        print("\n🎉 SUCCESS! PySpin is working!")
        return True
    else:
        print("\n❌ PySpin still not working")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
