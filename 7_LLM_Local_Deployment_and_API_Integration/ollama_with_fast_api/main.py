from http.client import responses
import uvicorn
from fastapi import FastAPI, Body

from ollama import Client

"""
By default, FastAPI doesn’t ship with a built-in server (it’s just an ASGI framework).
 That’s why people use Uvicorn or Hypercorn.

"""

app = FastAPI()
client = Client(
    host="http://localhost:11434"  # Default Ollama server address,
)


@app.get("/")
def root():
    return {"message": "Hello World"}


#... in fast api makes the param mandatory, not default value
@app.post("/chat")
def chat(message: str = Body(..., description="The message to send to the Ollama model")):
    response = client.chat(model="gemma3:270m",
                messages=[{
                        "role": "user",
                        "content": message
                    }
                ]
                )

    return {"response": response.message.content}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
