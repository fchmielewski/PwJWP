from __future__ import annotations

import os
from typing import Optional

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# Configuration
MODEL_NAME = os.getenv("HF_SUMMARY_MODEL", "facebook/bart-large-cnn")
DEVICE = 0 if torch.cuda.is_available() else -1  # GPU if available

# FastAPI application instance
app = FastAPI(
    title="Text Summarization API",
    description="Abstractive summarization with key-information retention",
    version="1.0.0",
)


# Pydantic schemas
class SummarizeRequest(BaseModel):
    """Input payload for /summarize."""

    text: str = Field(..., description="Raw text to summarize")
    max_length: int = Field(200, ge=10, le=512)
    min_length: int = Field(30, ge=5, le=256)
    do_sample: bool = Field(False, description="Sampling vs greedy decoding")


class SummarizeResponse(BaseModel):
    """Response model with generated summary."""

    summary: str


# Model loading (startup hook)
@app.on_event("startup")
def _load_model() -> None:
    """Initialise HF pipeline once at startup."""

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    # Global for reuse across requests (thread‑safe in FastAPI workers)
    global summarizer
    summarizer = pipeline(
        "summarization", model=model, tokenizer=tokenizer, device=DEVICE
    )


# Endpoint
@app.post("/summarize", response_model=SummarizeResponse, tags=["summarization"])
def summarize(req: SummarizeRequest) -> SummarizeResponse:

    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="'text' field cannot be empty")

    # Hugging Face pipeline handles tokenization/truncation internally
    result = summarizer(
        text,
        max_length=req.max_length,
        min_length=req.min_length,
        do_sample=req.do_sample,
        truncation=True,
    )[0]["summary_text"]

    return SummarizeResponse(summary=result)