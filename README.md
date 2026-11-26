# AI Dockerfile Generator

An AI-powered Dockerfile generator that scans application projects, uses a local Ollama model to generate Dockerfiles, builds Docker images, and attempts to fix Docker build errors automatically.

## Features

- Scans project files and detects application details.
- Detects Python and Flask projects.
- Generates Dockerfiles using a local Ollama AI model.
- Builds Docker images automatically.
- Attempts to fix Docker build errors with up to three retries.
- Supports configurable Ollama URL and model through environment variables.

## Tech Stack

- Python
- Docker
- Ollama
- Qwen 2.5 (1.5B)
- Requests

## Prerequisites

- Python 3.12
- Docker installed and running
- Ollama installed
- A downloaded Ollama model, such as `qwen2.5:1.5b`

## Installation

Clone the repository:

```bash
git clone https://github.com/Suchitdev/ai-dockerfile-generator.git
cd ai-dockerfile-generator
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Ollama Setup

Download the model:

```bash
ollama pull qwen2.5:1.5b
```

Configure the Ollama connection:

```bash
export OLLAMA_URL="http://localhost:11434"
export OLLAMA_MODEL="qwen2.5:1.5b"
```

If running the generator inside WSL while Ollama runs on Windows, replace `localhost` with the reachable Windows host address.

## Usage

Run the generator against a project directory:

```bash
python main.py sample-app
```

The generator scans the project, creates a Dockerfile, and builds the Docker image.

## Example Output

```text
Project type: Python
Framework: Flask
Entry point: app.py
Application port: 5000

Dockerfile successfully created.

Docker image built successfully!

Image: ai-generated-sample-app:latest
```

## Project Structure

```text
ai-dockerfile-generator/
├── ai_engine.py
├── docker_builder.py
├── dockerfile_writer.py
├── error_fixer.py
├── main.py
├── project_scanner.py
├── requirements.txt
├── sample-app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── .gitignore
└── README.md
```

## Current Limitations

This is an MVP currently tested with Python Flask applications. Support for additional frameworks and programming languages is planned for future versions.

AI-generated Dockerfiles should always be reviewed before production use.

## Future Improvements

- Django and FastAPI support.
- Node.js, React and other technology support.
- Improved Dockerfile optimization.
- More advanced build-error analysis.
- Automated testing and validation.

## Author

**Suchit Deshmukh**

GitHub: [Suchitdev](https://github.com/Suchitdev)
