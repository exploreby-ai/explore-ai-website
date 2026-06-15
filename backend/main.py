from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import datetime
import os

current_time = datetime.datetime.now().strftime("%B %d, %Y")

# 1. Get the secret API key from Render's Environment Variables securely
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY environment variable not found. Check Render settings!")

# Configure the API
genai.configure(api_key=api_key)

# Give the AI its personality and tell it the current date (from your original idea!)
system_prompt = f"The current date is {current_time}. You are ExploreAI, a helpful, smart, and friendly AI assistant."
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_prompt
)

# 2. Initialize the FastAPI app
app = FastAPI()

# 3. Enable CORS so your frontend HTML file can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Define the data structure we expect from the frontend
class ChatRequest(BaseModel):
    message: str

# 5. Create the API endpoint
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Send the user's message to the AI model
        response = model.generate_content(request.message)
        
        # Return the AI's text response back to the frontend
        return {"reply": response.text}
    
    except Exception as e:
        # Handle errors gracefully
        return {"reply": f"Sorry, I encountered an error: {str(e)}"}
