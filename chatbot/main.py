from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()  # Load environment variables from .env file

openai_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
llm = ChatOpenAI(api_key=openai_api_key, model_name="gpt-3.5-turbo")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str

def get_response_from_openai(message: str):
    prompt_template = PromptTemplate(
        input_variables=["message"],
        template="Respond to the user's message in a conversational manner:\n{message}"
    )
    sequence = prompt_template | llm
    response = sequence.invoke({"message": message})
    # Extract the content from the response object
    return response.content

@app.post("/chatbot/")
async def chatbot_response(query: Query):
    try:
        response = get_response_from_openai(query.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
