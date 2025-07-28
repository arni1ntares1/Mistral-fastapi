from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from llama_cpp import Llama
import os

app = FastAPI()

# Load the model once on startup
MODEL_PATH = os.getenv("MODEL_PATH", "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")

try:
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=4096,
        n_threads=os.cpu_count(),
        n_batch=512,
        use_mlock=True,
        verbose=False
    )
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")


class Prompt(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 512
    stop: list[str] | None = None


@app.post("/generate")
async def generate(prompt: Prompt):
    try:
        output = llm(
            prompt=prompt.prompt,
            temperature=prompt.temperature,
            max_tokens=prompt.max_tokens,
            stop=prompt.stop,
            echo=False,
        )
        return {"response": output["choices"][0]["text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"message": "FastAPI LLM endpoint is running"}
