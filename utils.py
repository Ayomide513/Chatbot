from google import genai
from config import Settings
from typing import Optional
from prompt import SYSTEM_PROMPT
import time

# Get google_api_key from settings
settings = Settings()
client = genai.Client(api_key=settings.google_api_key)

# Initialize chat session globally (maintains conversation history)
chat_session = None

def initialize_chat():
    """Initialize chat session with system prompt"""
    global chat_session
    if chat_session is None:
        chat_session = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[{
                "role": "user",
                "parts": [{"text": f"System Instructions: {SYSTEM_PROMPT}\n\nYou are now initialized. Greet the user warmly but briefly."}]
            }]
        )
    return chat_session

def support_function(user_prompt: str, chat_history: list = None) -> Optional[str]:
    """
    Generate response with conversation history
    
    Args:
        user_prompt: The current user message
        chat_history: List of previous messages for context
    """
    try:
        # Build conversation context
        conversation = f"{SYSTEM_PROMPT}\n\n"
        
        # Add chat history if available
        if chat_history:
            conversation += "Previous conversation:\n"
            for msg in chat_history[-6:]:  # Only last 6 messages for context
                role = msg["role"]
                content = msg["content"]
                conversation += f"{role.capitalize()}: {content}\n"
        
        # Add current user message
        conversation += f"\nUser: {user_prompt}\n\nAssistant:"
        
        # Generate response
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=conversation
        )
        
        return response.text
        
    except Exception as e:
        return f"Error: {str(e)}"

def response_generator(response: str):
    """Stream response word by word"""
    for word in response.split():
        yield word + " "
        time.sleep(0.05)