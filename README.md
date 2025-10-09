---
title: AI Meeting Assistant
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
---

# AI Meeting Assistant

[![CI](https://github.com/sashour82/ai-meeting-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/sashour82/ai-meeting-assistant/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive meeting assistant that transcribes audio recordings and provides intelligent summaries using OpenAI's Whisper and GPT models.

## Features

- 🎧 **Audio Transcription**: Convert MP3/WAV files to text using OpenAI Whisper
- 📝 **Intelligent Summarization**: Generate structured meeting summaries in Arabic
- 🌐 **Web Interface**: User-friendly Gradio interface with RTL support
- 🔗 **LangChain Integration**: Advanced text processing capabilities
- ⚙️ **Configurable**: Easy configuration through environment variables

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai_meeting_assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
cp .env.example .env
# then fill OPENAI_API_KEY in .env
```

## Usage

### Command Line
```bash
python main.py
```

### Programmatic Usage
```python
from ai_meeting_assistant import SpeechToTextProcessor, MeetingSummarizer

# Initialize processors
stt = SpeechToTextProcessor()
summarizer = MeetingSummarizer()

# Process audio file
transcript = stt.transcribe("meeting.mp3")
summary = summarizer.summarize(transcript)

print(f"Transcript: {transcript}")
print(f"Summary: {summary}")
```

## Project Structure

```
ai_meeting_assistant/
├── src/
│   ├── __init__.py
│   ├── speech_to_text.py    # Audio transcription module
│   ├── summarizer.py        # Text summarization module
│   └── interface.py         # Gradio web interface
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration settings
├── tests/
│   └── __init__.py
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Configuration

The application can be configured through environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `WHISPER_MODEL`: Whisper model to use (default: "whisper-1")
- `GPT_MODEL`: GPT model for summarization (default: "gpt-4o-mini")
- `TRANSCRIPTION_LANGUAGE`: Language for transcription (default: "ar")

## Supported Audio Formats

- MP3
- WAV

## License

This project is part of the Agentic AI Course.