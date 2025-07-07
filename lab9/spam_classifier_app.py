from __future__ import annotations

import os
from typing import Dict

import torch
import gradio as gr
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Konfiguracja
MODEL_NAME = os.getenv(
    "HF_SPAM_MODEL", "mrm8488/bert-tiny-finetuned-enron-spam-detection"
)
MAX_LEN: int = int(os.getenv("EMAIL_MAX_LEN", "512"))

# Urządzenie-
if torch.cuda.is_available() and bool(int(os.getenv("USE_CUDA", "0"))):
    DEVICE = torch.device("cuda:0")
elif bool(int(os.getenv("USE_MPS", "0"))) and torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
else:
    DEVICE = torch.device("cpu")

# Wyłącz równoległe tokenizery
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

# Model i tokenizer
print(f"🔄 Loading {MODEL_NAME} on {DEVICE}…")
_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
_tokenizer.model_max_length = MAX_LEN

_model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
_model.to(DEVICE)
_model.eval()
print("✅ Model loaded.")

# Mapowanie id-etykieta
id2label = _model.config.id2label  # np. {0: 'ham', 1: 'spam'}
LABEL_HUMAN: Dict[str, str] = {
    "ham": "nie-spam",
    "spam": "spam",
    "LABEL_0": "nie-spam",
    "LABEL_1": "spam",
}


# Predykcja

def predict(email_text: str) -> Dict[str, float] | str:
    email_text = email_text.strip()
    if not email_text:
        return "⚠️ Wklej treść e-maila."

    enc = _tokenizer(
        email_text,
        truncation=True,
        padding="max_length",
        max_length=MAX_LEN,
        return_tensors="pt",
    ).to(DEVICE)

    with torch.no_grad():
        logits = _model(**enc).logits.squeeze(0)
        probs = torch.softmax(logits, dim=-1).cpu().tolist()

    return {
        LABEL_HUMAN.get(id2label[idx], id2label[idx]): float(probs[idx])
        for idx in range(len(probs))
    }


# Interfejs Gradio

demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(lines=15, placeholder="Wklej pełną treść e-maila…"),
    outputs=gr.Label(num_top_classes=2),
    title="Klasyfikator spamu (BERT-tiny / Enron)",
    description="Prawdopodobieństwo, że wiadomość to *spam* versus *nie-spam*.",
    examples=[
        ["Congratulations! You won a FREE lottery! Click here to claim now."],
        ["Cześć Kasiu, przesyłam notatki ze spotkania w załączniku."],
    ],
    allow_flagging="never",
    theme="default",
)

if __name__ == "__main__":
    demo.launch()
