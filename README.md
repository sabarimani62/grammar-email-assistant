# 📝 Grammar & Email Assistant

A narrow-purpose AI support chatbot built with **Hugging Face** (free Inference API) and **Streamlit**. Unlike a general chatbot, it is deliberately restricted to two tasks:

1. **Grammar & sentence correction** — paste any sentence or paragraph, get a corrected version with an explanation of the fixes.
2. **Email drafting help** — describe the email you need, get a clean, professional draft.

For anything outside those two tasks, the assistant politely declines and redirects the user — demonstrating controlled, scoped AI behavior rather than an open-ended chatbot.

## Tech Stack
- **Hugging Face Inference API** — free-tier hosted LLM (`mistralai/Mistral-7B-Instruct-v0.3`)
- **huggingface_hub Python SDK** — for calling the model
- **Streamlit** — chat interface & free web hosting
- **Prompt engineering** — a system prompt constrains the assistant to its two allowed tasks

## How It Works
1. User sends a message through the chat UI.
2. The app sends the conversation, along with a strict system prompt, to a free Hugging Face-hosted language model via the Inference API.
3. The model either corrects the text / drafts the email, or declines if the request is out of scope.
4. The response is displayed back in the chat.


## Run It Locally
```bash
git clone <your-repo-url>
cd <repo-folder>
pip install -r requirements.txt
export HF_TOKEN=your_huggingface_token_here   # Windows: set HF_TOKEN=...
streamlit run streamlit_app.py
```

## Project Structure
```
├── streamlit_app.py       # Main application
├── requirements.txt       # Python dependencies
└── README.md               # This file
```

## What This Project Demonstrates
- Using Hugging Face's free hosted inference infrastructure instead of running models locally
- Prompt design to safely restrict an LLM's behavior to a defined scope
- Building and deploying a functional AI web app end-to-end at zero cost
