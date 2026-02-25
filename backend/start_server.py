"""
Start the College Admissions Simulator API server
"""
import uvicorn
from main import app

if __name__ == "__main__":
    print("=" * 60)
    print("Starting College Admissions Simulator API")
    print("=" * 60)
    print()
    print("Features:")
    print("  - 53 Top US Universities")
    print("  - 11 Gender Options")
    print("  - 38 AP Subjects")
    print("  - Application Rounds (ED/EA/REA/RD)")
    print("  - Specific Countries & States")
    print()
    print("Server will start on: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    print()

    uvicorn.run(app, host="0.0.0.0", port=8000)
