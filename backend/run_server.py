"""
College Admissions Simulator - Enhanced Version
Start script for the API server

Run this file to start the server:
    python run_server.py
"""

import uvicorn
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 70)
    print("COLLEGE ADMISSIONS SIMULATOR - ENHANCED VERSION")
    print("=" * 70)
    print()
    print("Features:")
    print("  * 100 Top US Universities (Complete Top 100)")
    print("  * 11 Gender Options (inclusive LGBTQ+ identities)")
    print("  * 38 AP Subjects (all categories)")
    print("  * Application Rounds (ED/EA/REA/RD with multipliers)")
    print("  * Specific Countries & States (26 countries, 52 states)")
    print("  * ML-Powered Predictions (Hybrid ML + Rule-based)")
    print()
    print("Server starting on: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print()
    print("Available Endpoints:")
    print("  GET  /schools       - List all 100 universities")
    print("  GET  /ap-subjects   - List all 38 AP subjects")
    print("  GET  /countries     - List all countries")
    print("  GET  /us-states     - List all US states")
    print("  POST /evaluate      - Evaluate applicant profile")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 70)
    print()

    try:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
    except OSError as e:
        if "10048" in str(e) or "address already in use" in str(e).lower():
            print()
            print("=" * 70)
            print("ERROR: Port 8000 is already in use!")
            print("=" * 70)
            print()
            print("Trying port 8001 instead...")
            print("Server will be available at: http://localhost:8001")
            print()
            uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False)
        else:
            raise

if __name__ == "__main__":
    main()
