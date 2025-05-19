from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, validator
from app.chatbot import get_conversational_chain
from typing import List, Tuple

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="templates")

chain = get_conversational_chain()

class ChatRequestBody(BaseModel):
    message: str
    chat_history: List[Tuple[str, str]] = []

    @validator('message')
    def message_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("message must not be empty")
        return value

@app.post("/chat")
async def chat(body: ChatRequestBody):
    try:
        result = chain({"question": body.message, "chat_history": body.chat_history})
        return JSONResponse(content={"answer": result["answer"]})
    except ValueError as ve: # Catch Pydantic validation error
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"Error in /chat endpoint: {e}") # Log the error for debugging
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
