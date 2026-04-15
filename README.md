# Flask Chatbot

This project provides a simple Flask-based chatbot with:

- Predefined responses for common university questions.
- A fallback to OpenAI responses when a question is not predefined.

## Run app

```bash
python app.py
```

## System architecture simulation

You can simulate the current architecture behavior (routing, latency, and failures):

```bash
python architecture_simulation.py --requests 50 --seed 7
```

Useful flags:

- `--openai-failure-rate` (default: `0.08`)
- `--predefined-ratio` (default: `0.55`)

Example:

```bash
python architecture_simulation.py --requests 100 --seed 42 --predefined-ratio 0.65
```
