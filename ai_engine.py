import requests
import os

# Ollama configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")


def clean_dockerfile(response_text):
    """
    Remove Markdown formatting and validate AI-generated Dockerfile.
    """

    dockerfile = response_text.strip()

    if dockerfile.startswith("```"):
        lines = dockerfile.splitlines()
        lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        dockerfile = "\n".join(lines).strip()

    if not dockerfile.startswith("FROM "):
        raise ValueError("AI did not generate a valid Dockerfile.")

    return dockerfile


def generate_dockerfile(project_info):
    """
    Generate a Dockerfile using detected project metadata
    and application source files.
    """

    project_type = project_info["project_type"]
    framework = project_info["framework"]
    entry_point = project_info["entry_point"]
    port = project_info["port"]
    project_context = project_info["context"]

    prompt = f"""
You are an expert Docker and containerization engineer.

Analyze the application metadata and source files.

PROJECT INFORMATION:
- Project type: {project_type}
- Framework: {framework}
- Entry point: {entry_point}
- Application port: {port}

APPLICATION FILES:
{project_context}

DOCKERFILE REQUIREMENTS:

1. Select a suitable official base image.
2. Set WORKDIR /app.
3. Copy dependency files BEFORE installing dependencies.
4. Install dependencies only after copying their files.
5. Copy the remaining application source files.
6. Expose the detected application port when applicable.
7. Use the correct application startup command.
8. Never reference a file before copying it into the image.
9. Do not invent dependencies or startup commands.
10. Do not copy environment secrets into the image.
11. Use efficient Docker instructions.

PYTHON APPLICATION RULES:

- Use an appropriate official Python base image.
- If requirements.txt exists, follow this exact order:

  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .

- If requirements.txt does not exist, inspect the available
  Python dependency files.
- Use the detected entry point when valid.
- Inspect application files for the correct startup command.

NODE.JS APPLICATION RULES:

- Use an appropriate official Node.js base image.
- Set WORKDIR /app.
- Copy package.json and available lock files first.
- Use npm ci when a compatible package-lock.json exists.
- Otherwise use an appropriate npm installation command.
- Copy application source files after installing dependencies.
- Inspect package.json scripts for the startup command.

OUTPUT REQUIREMENTS:

- Return ONLY the complete Dockerfile.
- Do not include Markdown fences.
- Do not include explanations.
- The first instruction must be FROM.
- Never install dependencies before copying their files.

Generate the Dockerfile now.
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 350},
        },
        timeout=300,
    )

    response.raise_for_status()

    return clean_dockerfile(response.json()["response"])


def fix_dockerfile(dockerfile, build_error):
    """
    Analyze Docker build errors and generate a corrected Dockerfile.
    """

    prompt = f"""
Role: Docker Build Diagnostics and Remediation Engine.

Objective:
Analyze the failed Docker build and produce a corrected Dockerfile.

ENGINEERING REQUIREMENTS:

1. Identify the root cause from the supplied build output.
2. Correct invalid Docker instructions.
3. Correct dependency installation and file-copy ordering.
4. Preserve the application's runtime configuration.
5. Retain required application files and dependencies.
6. Preserve the correct exposed application port.
7. Preserve the application's startup command.
8. Avoid unnecessary changes to working instructions.
9. Do not invent application dependencies or startup commands.
10. Never reference files that have not been copied into the image.

OUTPUT CONSTRAINTS:

- Return the complete corrected Dockerfile.
- Output valid Dockerfile syntax only.
- Do not include Markdown formatting.
- Do not include explanations.
- The first instruction must be FROM.

EXISTING DOCKERFILE:
{dockerfile}

DOCKER BUILD DIAGNOSTICS:
{build_error}

Generate the corrected Dockerfile now.
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 350},
        },
        timeout=300,
    )

    response.raise_for_status()

    return clean_dockerfile(response.json()["response"])
