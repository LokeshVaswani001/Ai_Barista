# AI Barista — RAG Agent (Streamlit + Google ADK)

A simple AI barista chatbot for a coffee shop. It uses Google's Agent
Development Kit (ADK) with a Gemini model, and grounds its answers in a
local `menu.json` file using Retrieval-Augmented Generation (RAG).

## Files

- `menu.json` — the coffee shop's menu (mock data source for RAG)
- `barista_agent.py` — the ADK agent + RAG tools (search menu, filter allergens)
- `app.py` — the Streamlit chat interface
- `requirements.txt` — Python dependencies

## How to deploy for free (no credit card required)

### 1. Get a free Gemini API key
Go to https://aistudio.google.com/app/apikey and click **"Get API Key"**.
Copy the key — you'll need it in step 4.

### 2. Create a GitHub repository
- Go to https://github.com and create a free account if you don't have one.
- Create a **new repository** (e.g. `ai-barista`).
- Upload these 4 files (`menu.json`, `barista_agent.py`, `app.py`,
  `requirements.txt`) to that repository.

### 3. Deploy on Streamlit Community Cloud
- Go to https://share.streamlit.io and sign in with your GitHub account.
- Click **"New app"**.
- Select your `ai-barista` repository, branch `main`, and main file
  `app.py`.
- Click **"Advanced settings"** → **"Secrets"** and add:
  ```
  GOOGLE_API_KEY = "paste-your-api-key-here"
  ```
- Click **"Deploy"**.

### 4. Get your live link
After a minute or two, your app will be live at a URL like:

```
https://your-app-name.streamlit.app
```

Copy that link and submit it wherever it's needed (e.g. the Hack2Skill
"Upload the deployed project link" field).

## Testing locally (optional)

```bash
pip install -r requirements.txt
export GOOGLE_API_KEY="your-key-here"
streamlit run app.py
```
