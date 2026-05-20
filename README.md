# ProjectMaestro

An intelligent multi-agent automation framework with voice and text interface capabilities, designed to orchestrate complex tasks through a supervisor-based agent architecture.

## Overview

ProjectMaestro is a sophisticated Python-based system that combines AI-powered agents with a user-friendly interface to execute automated workflows. The system leverages multiple specialized agents coordinated by a master supervisor agent, integrated with voice transcription capabilities and an intuitive Gradio-based chat interface.

## Key Features

- **Multi-Agent Architecture**: Specialized agents for coding, OS management, and task supervision
- **Voice Interface**: Integrated Whisper speech-to-text transcription for hands-free interaction
- **Intelligent Supervisor**: Master agent that orchestrates task delegation across specialized agents
- **Interactive Chat UI**: Gradio-powered interface supporting both text and voice inputs
- **LLM Integration**: Support for multiple LLM providers (OpenAI, Groq) for enhanced AI capabilities
- **Command Execution**: Automated execution of generated commands and workflows

## Project Structure

```
projectMaestro/
├── main.py                 # Application entry point with Gradio UI
├── agents/
│   ├── supervisor/         # Master supervisor agent for task coordination
│   ├── coder/             # Specialized agent for coding tasks
│   └── os_manager/        # Specialized agent for OS-level operations
├── tools/                 # Utility functions and helper tools
├── test/                  # Test suite and validation scripts
└── .gitignore            # Git configuration
```

## Technology Stack

- **Language**: Python 3.x
- **UI Framework**: Gradio
- **LLM Integration**: OpenAI SDK, Groq API
- **Speech Processing**: Whisper (via Groq)
- **Environment Management**: python-dotenv

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TahiraTufail/projectMaestro.git
cd projectMaestro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Add your API keys:
# GROQ_API=your_groq_api_key
# OPENAI_API=your_openai_api_key
```

## Usage

Start the application:
```bash
python main.py
```

The Gradio interface will launch with:
- Text input field for typed commands
- Microphone input for voice commands
- Chat history display
- Real-time task execution feedback

## How It Works

1. **User Input**: Users provide instructions via text or voice
2. **Voice Processing**: Audio input is transcribed using Whisper
3. **Task Routing**: Supervisor agent analyzes the request and routes it to appropriate specialized agents
4. **Execution**: Generated commands are executed and results are reported back
5. **Response**: User receives feedback on completed tasks

## Agent Architecture

### Supervisor Agent
- Orchestrates task distribution
- Analyzes user requests
- Determines task routing to specialized agents

### Coder Agent
- Handles code generation and development tasks
- Manages programming-related workflows

### OS Manager Agent
- Manages system-level operations
- Handles OS commands and file system operations

## Requirements

- Python 3.8+
- Active API keys for:
  - OpenAI (for GPT models)
  - Groq (for Whisper transcription)

## Notes

- Commands are executed sequentially as separated by `&&` operators
- Voice transcription requires microphone access
- Ensure proper API credentials are configured before running

## License

[Add your license information here]

## Support

For issues, questions, or contributions, please refer to the repository's GitHub issues page.
