from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uuid
import json
from typing import List, Dict, Union
from io import BytesIO, StringIO # Ensure StringIO is imported here for CSV handling

from core.file_parser import parse_transcript
from core.summarizer import Summarizer
from core.extractor import Extractor

app = FastAPI()

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

summarizer = Summarizer()
extractor = Extractor()

UPLOAD_DIR = "uploaded_transcripts"
os.makedirs(UPLOAD_DIR, exist_ok=True)
RESULTS_DIR = "analysis_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

class AnalysisResult(BaseModel):
    summary: str
    action_items: List[Dict]
    insights: List[str]
    attributed_statements: List[Dict]
    attributed_action_items_insights: Dict[str, Dict[str, List]]


@app.post("/analyze_transcript/", response_model=AnalysisResult)
async def analyze_transcript(file: UploadFile = File(...)):
    """
    Analyzes an uploaded transcript file to generate a summary,
    extract action items and insights, and attribute statements to speakers.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    file_extension = os.path.splitext(file.filename)[1].lower()
    allowed_extensions = ['.txt', '.docx', '.pdf']
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")

    try:
        file_content = await file.read()
        transcript_text = parse_transcript(file.filename, file_content)

        # Generate summary using the Summarizer class
        summary = summarizer.generate_summary(transcript_text)
        
        # Extract action items and insights using the Extractor class
        action_items = extractor.extract_action_items(transcript_text)
        insights = extractor.extract_insights(transcript_text)
        
        # Attribute statements to individual speakers
        attributed_statements = extractor.attribute_statements(transcript_text)
        
        # Attribute action items and insights to speakers based on proximity
        attributed_action_items_insights = extractor.attribute_action_items_and_insights(transcript_text, action_items, insights)

        return AnalysisResult(
            summary=summary,
            action_items=action_items,
            insights=insights,
            attributed_statements=attributed_statements,
            attributed_action_items_insights=attributed_action_items_insights
        )
    except ValueError as e:
        # Handle specific parsing errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch any other unexpected errors during analysis
        print(f"Error during transcript analysis: {e}") # Log the error for debugging
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {e}")

@app.get("/export_results/{format}/{analysis_id}")
async def export_results(format: str, analysis_id: str):
    """
    Exports dummy analysis results in PDF or CSV format.
    NOTE: In a production application, 'analysis_id' would be used to retrieve
    actual stored analysis results, rather than dummy data.
    """
    # For this example, we use dummy data for demonstration purposes.
    # In a real application, you would load the actual results associated with analysis_id.
    dummy_summary = "This is a dummy summary for export. It demonstrates how a concise overview would appear in the report."
    dummy_action_items = [
        {"item": "Dummy Action Item 1: Review project milestones.", "responsible_party": "Alice", "deadline": "2025-07-10"},
        {"item": "Dummy Action Item 2: Prepare Q3 budget report.", "responsible_party": "Bob", "deadline": "2025-07-15"}
    ]
    dummy_insights = [
        "Dummy Insight 1: Customer feedback indicates a strong preference for mobile-first design.",
        "Dummy Insight 2: Decision made to pivot marketing strategy towards social media influencers."
    ]

    filename = f"analysis_results_{analysis_id}.{format}"
    
    if format == "pdf":
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch # Import unit 'inch' here

        buffer = BytesIO() # Bytes buffer for PDF output
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Add title
        story.append(Paragraph("Meeting Analysis Report", styles['h1']))
        story.append(Spacer(1, 0.2 * inch)) # Use inch for consistent spacing

        # Add Summary
        story.append(Paragraph("Summary:", styles['h2']))
        story.append(Paragraph(dummy_summary, styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

        # Add Action Items
        story.append(Paragraph("Action Items:", styles['h2']))
        for item in dummy_action_items:
            story.append(Paragraph(f"- {item['item']} (Responsible: {item['responsible_party']}, Deadline: {item['deadline']})", styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

        # Add Key Insights
        story.append(Paragraph("Key Insights:", styles['h2']))
        for insight in dummy_insights:
            story.append(Paragraph(f"- {insight}", styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

        # Build the PDF document
        doc.build(story)
        buffer.seek(0) # Rewind the buffer to the beginning
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    elif format == "csv":
        import csv
        csv_buffer = StringIO() # Use StringIO for text-based CSV writing
        writer = csv.writer(csv_buffer)
        
        # Write CSV header row
        writer.writerow(["Type", "Content", "Responsible Party", "Deadline"])
        
        # Write Summary row
        writer.writerow(["Summary", dummy_summary, "", ""]) # Summary has no specific party or deadline
        
        # Write Action Items
        for item in dummy_action_items:
            writer.writerow(["Action Item", item['item'], item['responsible_party'], item['deadline']])
        
        # Write Insights
        for insight in dummy_insights:
            writer.writerow(["Insight", insight, "", ""]) # Insights have no specific party or deadline
        
        csv_buffer.seek(0) # Rewind the text buffer to the beginning
        # Get the string content from StringIO, then encode it to bytes for the StreamingResponse
        return StreamingResponse(
            BytesIO(csv_buffer.getvalue().encode('utf-8')), # Encode the string to bytes
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    else:
        raise HTTPException(status_code=400, detail="Unsupported export format. Choose 'pdf' or 'csv'.")

if __name__ == "__main__":
    import uvicorn
    # When running directly, start the Uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=8000)
