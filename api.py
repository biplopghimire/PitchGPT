"""
FastAPI server for PitchGPT analysis.

Usage:
    uvicorn api:app --reload --port 8000

Then visit: http://localhost:8000
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
import os

from pitchgpt import PitchGPT

app = FastAPI(
    title="PitchGPT API",
    description="Analyze startup pitch decks with AI-powered insights",
    version="1.0.0"
)

# CORS middleware for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (HTML frontend)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve data files (PDFs for download)
if os.path.exists("pitchgpt_rag/data"):
    app.mount("/data", StaticFiles(directory="pitchgpt_rag/data"), name="data")

# Initialize PitchGPT
try:
    analyzer = PitchGPT(model_type='gemini_api', model_name='gemini-2.5-flash')
except Exception as e:
    print(f"Warning: Could not initialize PitchGPT: {e}")
    analyzer = None


class PitchRequest(BaseModel):
    pitch_text: str = Field(..., description="The startup pitch deck text to analyze", min_length=10)
    prompt_key: Optional[str] = Field(default="default_analysis", description="Which prompt template to use")
    custom_prompt: Optional[str] = Field(default=None, description="Optional custom prompt template")


class PitchResponse(BaseModel):
    analysis: str = Field(..., description="The AI-generated analysis in Markdown format")
    context: Optional[str] = Field(default=None, description="The retrieved RAG context sources")
    prompt: Optional[str] = Field(default=None, description="The full prompt sent to the model")
    success: bool = Field(default=True)
    error: Optional[str] = Field(default=None)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page."""
    html_path = "static/index.html"
    if os.path.exists(html_path):
        with open(html_path, 'r') as f:
            return f.read()
    return """
    <html>
        <head><title>PitchGPT</title></head>
        <body>
            <h1>PitchGPT API</h1>
            <p>API is running. Visit <a href="/docs">/docs</a> for interactive API documentation.</p>
            <p>Frontend not found. Create static/index.html for the web interface.</p>
        </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "analyzer_loaded": analyzer is not None
    }


@app.post("/analyze", response_model=PitchResponse)
async def analyze_pitch(request: PitchRequest):
    """
    Analyze a startup pitch deck.
    
    Returns AI-generated insights including risks and due diligence questions.
    """
    if analyzer is None:
        raise HTTPException(
            status_code=503,
            detail="PitchGPT analyzer not initialized. Check your .env file for GEMINI_API_KEY."
        )
    
    try:
        # Get the context separately
        from pitchgpt_rag.src.rag_context import retrieve_context
        context = retrieve_context(request.pitch_text, k=6)
        
        # Build the prompt for display
        if request.custom_prompt:
            prompt_template = request.custom_prompt
        else:
            prompt_template = analyzer.prompts.get(request.prompt_key, analyzer.prompts.get('default_analysis', '{pitch_text}'))
        
        # Ensure template can accept {context}
        if "{context}" not in prompt_template:
            prompt_template = f"{prompt_template}\n\nContext:\n{{context}}"
        
        full_prompt = prompt_template.format(pitch_text=request.pitch_text, context=context)
        
        analysis = analyzer.analyze_pitch(
            pitch_text=request.pitch_text,
            prompt_key=request.prompt_key,
            custom_prompt=request.custom_prompt
        )
        
        return PitchResponse(
            analysis=analysis,
            context=context,
            prompt=full_prompt,
            success=True
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/prompts")
async def list_prompts():
    """List available prompt templates."""
    if analyzer is None:
        return {"prompts": {}}
    return {"prompts": analyzer.prompts}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
