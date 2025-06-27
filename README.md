# Speech-Transcript-Analyzer
LLM-Powered Meeting Analysis Tool
This project delivers a web-based application that leverages large language models (LLMs) to automate and streamline meeting analysis. It intelligently processes speech transcripts to generate concise summaries, extract actionable insights, identify clear action items with responsible parties and deadlines, and attribute statements to individual speakers. Built with Python (FastAPI) for the backend and a responsive HTML/CSS/JavaScript frontend, this tool transforms raw meeting transcripts into structured, actionable outputs, enhancing productivity and decision-making. Designed with open-source LLMs in mind for local deployment and cost-free operation.

Table of Contents
Core Features

Technical Stack

Setup Instructions

Prerequisites

Backend Setup

Frontend Setup

Usage

Sample Input/Output

Future Enhancements (Bonus Features)

Acknowledgements

Core Features
Transcript Ingestion: Accepts transcript files in common formats (.txt, .docx, .pdf).

Automatic Summarization: Generates concise summaries of the transcript content.

Action Item Extraction: Identifies and lists action items, including responsible parties and deadlines if mentioned.

Insight Extraction: Highlights key insights, decisions, and important discussion points.

Speaker Attribution: Attributes statements, action items, and insights to individual speakers where possible.

Interactive UI: Provides a simple web-based interface for uploading transcripts and viewing results.

Export Results: Allows users to export summaries, action items, and insights in PDF and CSV formats (reflecting actual analyzed data).

Technical Stack
Backend:

Python 3.8+

FastAPI (Web Framework)

Hugging Face Transformers (for LLM functionalities like summarization, using t5-small model)

PyTorch (as the deep learning backend for Transformers)

python-docx (for .docx parsing)

PyPDF2 (for .pdf parsing)

reportlab (for PDF generation)

csv (Python built-in for CSV generation)

Frontend:

HTML5

CSS3

JavaScript (ES6+)

Setup Instructions
Follow these steps to get the application up and running on your local machine.

Prerequisites
Python 3.8 or higher installed.

pip (Python package installer) installed.

git (for cloning the repository).

A modern web browser (Chrome, Firefox, Edge).

Backend Setup
Clone the repository:

git clone https://github.com/YOUR_GITHUB_USERNAME/meeting_analyzer.git
cd meeting_analyzer

(Replace YOUR_GITHUB_USERNAME with your actual GitHub username if you've already created the repo and pushed the code).

Create and activate a virtual environment:
It's highly recommended to use a virtual environment to manage dependencies.

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

Navigate to the backend directory:

cd backend

Install backend dependencies:

pip install -r requirements.txt

If requirements.txt is missing, you can create it with the following content and then run pip install -r requirements.txt:

fastapi
uvicorn
python-docx
PyPDF2
transformers
torch
accelerate
scikit-learn
numpy
reportlab

Run the FastAPI backend server:

uvicorn main:app --reload

You should see output indicating that Uvicorn is running, typically on http://127.0.0.1:8000. Keep this terminal window open and running.

Frontend Setup
The frontend is a simple HTML/CSS/JavaScript application and does not require a separate server to run locally, as it directly accesses the backend API.

Navigate to the frontend directory (if you're not already there):

cd ../frontend

(Or, from the project root meeting_analyzer directory, just locate the frontend folder.)

Open index.html in your web browser:
Simply double-click the index.html file in your file explorer, or drag and drop it into your browser.
Alternatively, copy its full path (e.g., C:\Users\satis\Downloads\meeting_analyzer\frontend\index.html) and paste it into your browser's address bar, then press Enter.

Usage
Start the Backend Server (as per "Backend Setup" above).

Open the Frontend index.html file in your browser (as per "Frontend Setup" above).

Upload a Transcript: Click the "Choose File" button and select a .txt, .docx, or .pdf meeting transcript. You can use the provided sample files from the transcripts folder.

Analyze: Click the "Analyze Transcript" button. The application will process the file, and the summary, action items, insights, and speaker attributions will be displayed below.

Export Results: Once analysis is complete, click "Export as PDF" or "Export as CSV" to download the structured results. These exports will contain the actual data generated from your uploaded transcript.

Sample Input/Output
You can find sample transcript files in the transcripts/ directory within this repository. These files are designed to showcase the tool's capabilities.

sample_meeting.txt

project_kickoff_v2.txt

strategic_review_v2.txt

bug_fix_standup.txt

client_feedback_session.txt

quarterly_financial_brief.txt

When you upload these, the generated PDF and CSV files will dynamically reflect the analysis of their content.

Future Enhancements (Bonus Features)
Multilingual Support: Integrate a multilingual LLM or translation service to process transcripts in various languages.

Real-time Processing: Adapt the backend to support live transcription analysis via a streaming API.

Integration: Connect with external calendar or task management tools (e.g., Google Calendar, Trello) to directly add action items.

Sentiment Analysis: Analyze and display sentiment trends throughout the transcript.

Customizable Summaries: Allow users to define summary length or focus (e.g., decisions only, action items only).

Database Persistence: Replace the in-memory analysis_store with a persistent database (like Firestore) to save user analyses.

Acknowledgements
FastAPI: For building a robust and efficient backend API.

Hugging Face Transformers: For providing powerful, open-source LLMs and NLP tools.

PyTorch: The deep learning framework powering the LLMs.

python-docx and PyPDF2: For efficient document parsing.

reportlab: For professional PDF generation.
