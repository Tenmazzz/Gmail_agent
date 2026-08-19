# Gmail Agent

An AI agent built with LangGraph and a local LLM (Ollama) that processes your unread Gmail messages: it summarizes them, flags urgent ones, and drafts replies when a response is needed. Everything is delivered through Telegram, with a global summary of all emails plus detailed alerts for the important ones.

## How it works

For each unread email:

1. **Summary** — the email is summarized in a few concise lines.
2. **Urgency check** — the agent decides whether the email needs quick attention (interview, deadline, unexpected change...).
3. **Draft reply** — if a reply is expected, a draft is generated (never sent automatically).
4. **Telegram notification** — a global recap of all processed emails is sent first, then a detailed message for each email flagged as urgent.

The agent never sends or deletes anything on its own. It only reads and drafts.

## Architecture

- **LangGraph** orchestrates the flow: summary → urgency/draft decision → parallel branches → convergence.
- **Ollama** runs the LLM locally.
- **Gmail API** (via `langchain-google-community`) is used to search and read unread emails.
- **Telegram Bot API** is used for notifications.

## Setup

### 1. Environment variables

Copy `.env.example` to `.env` and fill in your own values:

```bash
cp .env.example .env
```

#### Optional: running Ollama on a remote machine

> **Note:** this section only applies if you want to run your LLM on a more powerful remote machine instead of locally. If you're running Ollama on the same machine as the agent, you can skip this.

The `SSH_OLLAMA_MODEL` and `SSH_OLLAMA_BASE_URL` variables let the agent connect to an Ollama instance running on a remote machine (for example, accessed over Tailscale and SSH). Set `SSH_OLLAMA_BASE_URL` to the remote machine's address, and make sure Ollama is reachable from the container running the agent.

### 2. Google Cloud / Gmail API

1. Create a project on [Google Cloud Console](https://console.cloud.google.com).
2. Enable the **Gmail API**.
3. Configure the **OAuth consent screen** (External, Testing mode — add your own Gmail account as a test user).
4. Create an **OAuth client ID** of type **Desktop app**.
5. Download the credentials file, rename it `credentials.json`, and place it in `backend/`.

`credentials.json` and `token.json` are excluded from version control via `.gitignore` — never commit them.

### 3. Telegram bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the prompts (choose a name and a username for your bot). BotFather will reply with your bot's **token** — save it for `TELEGRAM_BOT_TOKEN`.
3. Send at least one message to your new bot (search for it by its username and start a chat).
4. Get your **chat ID** by visiting this URL in your browser (replace `<TOKEN>` with your bot token):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
   Look for `"chat":{"id": ...}` in the response, that number is your `TELEGRAM_CHAT_ID`.
5. Add both values to your `.env`.

### 4. Run

```bash
docker compose run --rm backend python main.py
```

The first run will open a browser authorization flow for Gmail — subsequent runs reuse the saved token automatically.

## Project structure

```
.
├── backend/
│   ├── clients/            # LLM and Telegram clients
│   ├── gmail/               # Gmail authentication, search, and decoding logic
│   ├── nodes/               # LangGraph nodes (summary, decision, draft, alert)
│   ├── prompts/             # Prompt templates for each node
│   ├── credentials.json     # Google OAuth credentials (not committed)
│   ├── token.json           # Google OAuth token, generated on first run (not committed)
│   ├── graph.py              # LangGraph graph definition
│   ├── main.py                # Orchestration: fetch emails, run the graph, notify
│   └── requirements.txt
├── docker/
│   └── python/
│       └── Dockerfile
├── docker-compose.yml
├── .env                       # your own environment variables (not committed)
├── .env.example
└── .gitignore
```