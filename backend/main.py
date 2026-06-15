from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import datetime
current_time = datetime.datetime.now().strftime("%B %d, %Y")

# Send this to the AI: 
# "System: The current date is {current_time}. User asks: What is the date?"
# 1. Configure the AI API (Replace with your actual API key)
genai.configure(api_key="API KEY")
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# 2. Initialize the FastAPI app
app = FastAPI()

# 3. Enable CORS so your frontend HTML file can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your specific frontend URL
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
