
import os
import json
from pathlib import Path

IGNORED_DIRS = {
    ".git", ".venv", "venv", "env", "node_modules",
    "__pycache__", ".pytest_cache", "dist", "build",
    ".idea", ".vscode", ".next", "coverage"
}

IGNORED_FILES = {
    ".env", ".env.local", ".env.production",
    ".env.development", "id_rsa", "id_ed25519",
    "credentials", "secrets.json"
}

SENSITIVE_SUFFIXES = {
    ".pem", ".key", ".p12", ".pfx", ".crt"
}

ALLOWED_FILES = {
    "requirements.txt", "pyproject.toml", "Pipfile",
    "setup.py", "setup.cfg", "package.json",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "app.py", "main.py", "manage.py", "server.py",
    "index.js", "index.ts", "server.js", "server.ts"
}

SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".json", ".toml"}

MAX_FILE_SIZE = 100_000
MAX_TOTAL_CONTEXT = 500_000


def detect_project_type(project_path):
    """Identify the likely application runtime and framework."""

    files = {file.name for file in project_path.rglob("*") if file.is_file()}

    if "package.json" in files:
        package_path = project_path / "package.json"

        try:
            package = json.loads(package_path.read_text(encoding="utf-8"))
            dependencies = {
                **package.get("dependencies", {}),
                **package.get("devDependencies", {})
            }

            if "express" in dependencies:
                return "Node.js", "Express"
            return "Node.js", "Node.js application"

        except (OSError, json.JSONDecodeError):
            return "Node.js", "Unknown Node.js framework"

    if "requirements.txt" in files or "pyproject.toml" in files:
        dependency_text = ""

        for filename in ("requirements.txt", "pyproject.toml"):
            dependency_file = project_path / filename

            if dependency_file.exists():
                try:
                    dependency_text += dependency_file.read_text(
                        encoding="utf-8"
                    ).lower()
                except OSError:
                    pass

        if "flask" in dependency_text:
            return "Python", "Flask"
        if "django" in dependency_text:
            return "Python", "Django"
        if "fastapi" in dependency_text:
            return "Python", "FastAPI"

        return "Python", "Python application"

    return "Unknown", "Unknown"


def detect_entry_point(project_path, project_type):
    """Find a likely application startup file."""

    if project_type == "Python":
        candidates = ["app.py", "main.py", "manage.py", "server.py"]

    elif project_type == "Node.js":
        candidates = ["server.js", "index.js", "server.ts", "index.ts"]

    else:
        candidates = []

    for filename in candidates:
        if (project_path / filename).is_file():
            return filename

    return "Not detected"


def detect_port(project_path, framework):
    """Determine a likely application port."""

    defaults = {
        "Flask": 5000,
        "Django": 8000,
        "FastAPI": 8000,
        "Express": 3000,
        "Node.js application": 3000
    }

    return defaults.get(framework, 8000)


def scan_project(project_path):
    """Scan project files and return structured project information."""

    project_path = Path(project_path).resolve()

    if not project_path.exists():
        raise FileNotFoundError(
            f"Project directory not found: {project_path}"
        )

    if not project_path.is_dir():
        raise NotADirectoryError(
            f"Expected a directory: {project_path}"
        )

    project_type, framework = detect_project_type(project_path)
    entry_point = detect_entry_point(project_path, project_type)
    port = detect_port(project_path, framework)

    project_context = []
    total_size = 0

    for root, dirs, files in os.walk(project_path):

        dirs[:] = [
            directory for directory in dirs
            if directory not in IGNORED_DIRS
        ]

        for filename in sorted(files):

            if filename in IGNORED_FILES:
                continue

            file_path = Path(root) / filename

            if file_path.suffix.lower() in SENSITIVE_SUFFIXES:
                continue

            if filename not in ALLOWED_FILES:
                if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                    continue

            try:
                file_size = file_path.stat().st_size

                if file_size > MAX_FILE_SIZE:
                    print(f"Skipping large file: {file_path.name}")
                    continue

                if total_size + file_size > MAX_TOTAL_CONTEXT:
                    print("Maximum project context limit reached.")
                    break

                content = file_path.read_text(encoding="utf-8")

                relative_path = file_path.relative_to(project_path)

                project_context.append(
                    f"\nFile: {relative_path}\n{content}\n"
                )

                total_size += file_size

            except (UnicodeDecodeError, OSError):
                print(f"Skipping unreadable file: {file_path}")

        if total_size >= MAX_TOTAL_CONTEXT:
            break

    if not project_context:
        raise ValueError("No supported application files found.")

    return {
        "project_type": project_type,
        "framework": framework,
        "entry_point": entry_point,
        "port": port,
        "context": "\n".join(project_context)
    }
