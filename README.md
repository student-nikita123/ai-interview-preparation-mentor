# AI Interview Preparation Mentor

A Streamlit chat interface for practicing technical and behavioral interview
questions. The app uses LangChain to connect to the locally running Ollama
model configured in `app/config.py`.

## Requirements

- Python 3.13
- [Ollama](https://ollama.com/) installed and running
- The configured model available in Ollama (by default, `llama3.2:latest`)

## Setup

From the project root, activate your virtual environment and install dependencies:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull llama3.2:latest
```

## Run the Streamlit app

```powershell
python -m streamlit run app/ui/streamlit_app.py
```

Streamlit opens the app in your browser. Make sure Ollama is running locally
before submitting a question. The existing terminal interface remains available:

```powershell
python -m app.main
```

## Run tests

```powershell
python -m unittest discover -s tests
```

## Project structure

```text
app/
  config.py                 # Ollama model configuration
  prompts.py                # Mentor system prompt
  main.py                   # Existing terminal interface
  services/
    chat.py                 # Question validation and model interaction
  ui/
    streamlit_app.py        # Streamlit user interface
tests/
  test_chat_service.py      # Chat validation and response tests
.streamlit/
  config.toml               # Streamlit theme
requirements.txt
```
