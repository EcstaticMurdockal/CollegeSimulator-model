# How to Open the College Admissions Simulator Website

## Quick Start (2 Steps)

### Step 1: Start the Backend API
Open a terminal/command prompt and run:
```bash
cd C:\Users\汤\Desktop\CollegeSimulator\backend
python run_server.py
```

You should see:
```
College Admissions Simulator API - Enhanced Version
Server starting on: http://localhost:8001
```

**Keep this terminal open!**

### Step 2: Start the Frontend Website
Open a **NEW** terminal/command prompt and run:
```bash
cd C:\Users\汤\Desktop\CollegeSimulator\frontend
npm start
```

The website will automatically open in your browser at:
**http://localhost:3000**

If it doesn't open automatically, manually open your browser and go to:
**http://localhost:3000**

## What You'll See

The website will have a form where you can:
- Select from 53 universities
- Choose from 11 gender options
- Select AP subjects from all 38 available courses
- Choose application rounds (ED/EA/REA/RD)
- Enter your GPA, SAT scores, extracurriculars, etc.
- Get admission probability predictions

## Troubleshooting

### If the backend won't start:
- Make sure Python is installed
- Make sure you're in the correct directory
- Check if port 8001 is available

### If the frontend won't start:
- Make sure Node.js and npm are installed
- Run `npm install` first if you haven't already
- Check if port 3000 is available

### If the website loads but can't connect to backend:
- Make sure the backend is running (Step 1)
- Check that the backend is on port 8001
- The frontend is configured to connect to port 8001

## Ports Used
- **Backend API**: http://localhost:8001
- **Frontend Website**: http://localhost:3000

## Need Help?
- Backend API documentation: http://localhost:8001/docs
- Check backend is running: http://localhost:8001/schools
