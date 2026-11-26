import subprocess
from pathlib import Path


def build_docker_image(project_path, image_name):

    project_path = Path(project_path).resolve()

    dockerfile_path = project_path / "Dockerfile"

    if not dockerfile_path.exists():
        raise FileNotFoundError(f"Dockerfile not found: {dockerfile_path}")

    print("\nStarting Docker image build...")
    print(f"Image name: {image_name}")

    command = [
        "docker",
        "build",
        "-t",
        image_name,
        "-f",
        str(dockerfile_path),
        str(project_path),
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    print("\n========== DOCKER BUILD OUTPUT ==========")
    print(result.stdout)

    if result.returncode != 0:
        print("\n========== DOCKER BUILD ERROR ==========")
        print(result.stderr)

        return {"success": False, "error": result.stderr, "output": result.stdout}

    print("\nDocker image built successfully!")

    return {"success": True, "error": None, "output": result.stdout}
