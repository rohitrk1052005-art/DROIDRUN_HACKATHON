import os
import uvicorn
import json
from google import genai  
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


API_KEY = "AIzaSyDa_fVYq0DyThAw4-ujzUq9Wk9mZ0XyuDc" 


client = genai.Client(api_key=API_KEY)


MODEL_NAME = "gemini-flash-latest" 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_upsc(request: AnalyzeRequest):
    print(f"📥 Received Text (Length: {len(request.text)})")

    if not request.text or len(request.text) < 5:
        raise HTTPException(status_code=400, detail="Text too short")

    
    prompt = f"""
    You are an expert UPSC Faculty. Analyze the text STRICTLY for UPSC Syllabus.

    INPUT TEXT: "{request.text}"

    TASKS:
    1. Map to GS Paper (1-4) & Subject.
    2. Identify Micro-Topic.
    3. One line Relevance.
    4. Create 1 Prelims MCQ.
    5. Create 1 Mains Question.

    OUTPUT JSON FORMAT:
    {{
        "gs_paper": "GS Paper X",
        "subject": "Subject Name",
        "micro_topic": "Specific Topic",
        "relevance": "Why it matters...",
        "prelims": {{
            "question": "Question?",
            "options": ["A", "B", "C", "D"],
            "answer": "Option",
            "explanation": "Brief reasoning"
        }},
        "mains": "Mains Question?"
    }}
    """

    try:
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                'response_mime_type': 'application/json'
            }
        )
        

        return json.loads(response.text)

    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        return {
            "gs_paper": "Error",
            "subject": "Connection Failed",
            "micro_topic": "Check Terminal",
            "relevance": "Could not connect to Google AI.",
            "prelims": {
                "question": "Error fetching data.",
                "options": ["Try Again"],
                "answer": "",
                "explanation": str(e)
            },
            "mains": "Please check backend console."
        }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)