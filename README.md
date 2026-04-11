# Banking Chatbot

A simple banking chatbot project with FastAPI, a LangChain-powered banking agent, UI, and tests.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Banking Agent

The chatbot now uses a LangChain agent backed by an OpenAI-compatible chat completion endpoint. The agent can route questions across these banking areas:

- account info
- transaction search
- spending summaries
- statements and documents
- cards
- beneficiaries and payees
- loans
- deposits and investments
- support and disputes
- profile and service
- banking FAQs

Payments and transfers are intentionally not supported in this demo.

Set these environment variables to enable it:

```bash
LLM_API_KEY=your_api_key
LLM_MODEL=your_model_name
LLM_API_URL=https://api.openai.com/v1/chat/completions
```

If `LLM_API_KEY` or `LLM_MODEL` is missing, or the LLM call fails, the `/chat` endpoint returns an error until the LLM is configured correctly.
