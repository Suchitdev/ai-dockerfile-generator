
from pathlib import Path

from project_scanner import scan_project
from ai_engine import generate_dockerfile


def create_dockerfile(project_path, overwrite=False):
    """
    Scan a project, generate a Dockerfile using AI,
    and save it without silently overwriting an existing file.
    """

    project_path = Path(project_path).resolve()

    if not project_path.exists():
        raise FileNotFoundError(
            f"Project directory not found: {project_path}"
        )

    if not project_path.is_dir():
        raise NotADirectoryError(
            f"Expected a directory: {project_path}"
        )

    dockerfile_path = project_path / "Dockerfile"

    if dockerfile_path.exists() and not overwrite:
        raise FileExistsError(
            f"Dockerfile already exists: {dockerfile_path}. "
            "Use overwrite=True to replace it."
        )

    print("\n[1/3] Scanning project files...")

    project_info = scan_project(project_path)

    print(f"Project type: {project_info['project_type']}")
    print(f"Framework: {project_info['framework']}")
    print(f"Entry point: {project_info['entry_point']}")
    print(f"Application port: {project_info['port']}")

    print("\n[2/3] Asking AI to generate Dockerfile...")

    dockerfile_content = generate_dockerfile(project_info)

    if not dockerfile_content.startswith("FROM "):
        raise ValueError("Generated Dockerfile failed validation.")

    print("\n[3/3] Saving Dockerfile...")

    dockerfile_path.write_text(
        dockerfile_content.strip() + "\n",
        encoding="utf-8"
    )

    print("\nDockerfile successfully created at:")
    print(dockerfile_path)

    return dockerfile_path
