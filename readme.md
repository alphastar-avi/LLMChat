# Diary Chat Assistant

A local LLM chat application that uses your diary as a knowledge base for context-aware conversations.

## Setup

1. Install Ollama:
```bash
# macOS/Linux
curl https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

2. Install a model:
```bash
ollama pull deepseek-r1:1.5b
```

3. Install application dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Access the application at `http://localhost:5000`

## Usage

1. Enter your model name in the application (e.g., `deepseek-r1:1.5b`)
2. Add entries to your diary through the memory interface
3. Chat with the AI using your diary as context

## Technical Stack

- Backend: Flask, LangChain, Ollama
- Frontend: HTML, CSS, JavaScript, Tailwind CSS
- Database: Chroma (Vector Store)

