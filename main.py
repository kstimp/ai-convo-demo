import json
import logging
import logging.handlers
import os
import time

from openai import OpenAI

# setup logger  
logger = logging.getLogger()  
logger.setLevel(logging.INFO)  
  
# Create a formatter to define the log format  
formatter = logging.Formatter("%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s")  
  
# Create handler to log to file  
log_dir = "./logs/ai-convo.log"
os.makedirs(log_dir, exist_ok=True)
file_handler = logging.handlers.RotatingFileHandler(  
    log_dir, 
    maxBytes=50000, 
    backupCount=7  
)  
file_handler.setLevel(logging.INFO)  
file_handler.setFormatter(formatter)  
  
# Create handler to log to console  
stream_handler = logging.StreamHandler()  
stream_handler.setLevel(logging.ERROR)  
stream_handler.setFormatter(formatter)  
  
logger.addHandler(file_handler)  
logger.addHandler(stream_handler)

# Function to initialize the OpenAI API with your API key
def init_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    return client
# Function to simulate the phone call
def simulate_phone_call():
    print("Welcome to the AI phone call simulator. Please start talking!")
    print("Note: To end the call, type 'bye' or 'exit'.\n")
    
    # Initialize OpenAI API
    ai = init_openai()

    # Initialize conversation history
    conversation_history = []

    while True:
        user_input = input("You: \n")
        
        # End the call if the user types 'bye' or 'exit'
        if user_input.lower() in ['bye', 'exit']:
            print("Call ended. Goodbye!")
            logger.info(json.dumps(conversation_history, indent=4))
            break
        
        # Add user's input to conversation history
        user_history = {"role": "user", "content": user_input}
        conversation_history.append(user_history)
        #logger.info(json.dumps(user_history, indent=4))
        
        # Generate AI's response
        try:
            completion = ai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a surly older man who owns an auto repair shop. You are helpful but not very kind."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )
            
            ai_response = completion.choices[0].message.content
            
            # Add AI's response to conversation history
            ai_convo = {"role": "assistant", "content": ai_response}
            conversation_history.append(ai_convo)
            #logger.info(json.dumps(ai_convo, indent=4))
            print(f"\nAI: \n{ai_response}\n")
            
            # Simulate a short pause before the next message, just like a phone call.
            time.sleep(2)
        
        except Exception as e:
            logger.error(f"Error with API call: {e}")
            logger.error(json.dumps(conversation_history, indent=4))
            break

if __name__ == "__main__":
    simulate_phone_call()
