from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx
import os
from evaluator import CodeEvaluator

app = FastAPI()
evaluator = CodeEvaluator()

# Add logic to serve static files if they exist
# In this hackathon setup, we just return index.html from root
@app.get("/", response_class=HTMLResponse)
async def get_index():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>UI Not Found</h1><p>Please ensure index.html is in the root directory.</p>"

class EvaluateRequest(BaseModel):
    language: str
    code: str
    tests: list[dict] # [{"input": "...", "expected": "..."}]

@app.post("/evaluate")
async def evaluate_code(req: EvaluateRequest):
    result = await evaluator.evaluate(req.language, req.code, req.tests)
    return result

@app.get("/languages")
async def get_languages():
    runtimes = await evaluator.get_runtimes()
    # Just return supported languages keys
    return list(runtimes.keys())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
