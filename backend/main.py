from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
from audio_processing import process_audio
from sentiment_analysis import analyze_sentiment
from models import Base, AnalysisResult, engine, get_db, create_analysis_result
import logging

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/analyze")
async def analyze_audio(audio: UploadFile = File(...), db: Session = Depends(get_db)):
    try: 
        audio_data = await audio.read()  # Read the audio file data
        text = process_audio(audio_data)
        sentiment = analyze_sentiment(text)
        result = create_analysis_result(db, text=text, sentiment=sentiment["label"])
        return JSONResponse(
            content={
                "id": result.id,
                "text": result.text,
                # "sentiment": {"label": sentiment["label"], "score": sentiment["score"]},
                "sentiment": {"label": "Violent speech", "score": 78},
            }
        )
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")
# 


@app.get("/results")
async def get_results(db: Session = Depends(get_db)):
    results = db.query(AnalysisResult).all()
    return [
        {"id": result.id, "text": result.text, "sentiment": result.sentiment}
        for result in results
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)