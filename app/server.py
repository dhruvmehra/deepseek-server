from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import uvicorn

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.7

# Global variables for model and tokenizer
model = None
tokenizer = None

def load_model():
    global model, tokenizer
    model_id = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading model on {device}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map="auto"
    )

@app.on_event("startup")
async def startup_event():
    load_model()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "device": "cuda" if torch.cuda.is_available() else "cpu"
    }

@app.post("/generate")
async def generate(request: GenerateRequest):
    try:
        inputs = tokenizer(request.prompt, return_tensors="pt")
        inputs = inputs.to(model.device)
        
        outputs = model.generate(
            **inputs,
            max_length=request.max_tokens,
            temperature=request.temperature,
            pad_token_id=tokenizer.eos_token_id
        )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"generated_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)