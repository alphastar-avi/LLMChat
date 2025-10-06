# LLMChat

A local LLM chat application and can also uses your Journal as a knowledge base for context-aware conversations.


https://github.com/user-attachments/assets/671f6090-c43f-4b08-8303-8004e64c20bb



## Setup

1. Install Ollama:
```bash
# macOS/Linux
brew install ollama
```

2. Install a model:
```bash
ollama pull deepseek-r1:1.5b
```

3. Install application dependencies:
```bash
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

## Usage

1. Enter your model name in the application (e.g., `deepseek-r1:1.5b`)
2. Add entries to your diary through the memory interface
3. Chat with the AI using your diary as context

## Technical Stack

- Backend: Flask, LangChain, Ollama
- Frontend: HTML, CSS, JavaScript, Tailwind CSS
- Database: ChromaDB ( Vector Store )


