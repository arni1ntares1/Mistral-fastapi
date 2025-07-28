from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI()

# Load the model (only once)
llm = Llama(model_path="models/mistral-7b-instruct-v0.1.Q4_K_M.gguf", n_ctx=2048)

# Define request schema
class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"message": "Mistral FastAPI is running!"}

@app.post("/generate")
def generate_text(req: PromptRequest):
    response = llm(
        req.prompt,
        max_tokens=200,
        temperature=0.7,
        top_p=0.9,
        stop=["</s>"]
    )
    return {"response": response["choices"][0]["text"].strip()}
