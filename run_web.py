#!/usr/bin/env python3
"""
MARS Web Interface Launcher
Run this file to start the web-based interface for the Multi-Agent Research System.
"""

import os
import sys
import subprocess

def main():
    print("🚀 Starting MARS Web Interface...")
    print("=" * 50)
    print("📱 The web interface will be available at: http://localhost:5000")
    print("🔄 Starting Flask server...")
    print()
    
    try:
        # Run the Flask app
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 MARS Web Interface stopped.")
    except Exception as e:
        print(f"\n❌ Error starting web interface: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
