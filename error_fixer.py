from pathlib import Path

from ai_engine import fix_dockerfile
from docker_builder import build_docker_image


def build_with_auto_fix(project_path, image_name, max_retries=3):

    project_path = Path(project_path).resolve()
    dockerfile_path = project_path / "Dockerfile"

    if not dockerfile_path.exists():
        raise FileNotFoundError(f"Dockerfile not found: {dockerfile_path}")

    for attempt in range(max_retries + 1):

        print(f"\n========== BUILD ATTEMPT {attempt + 1} ==========")

        result = build_docker_image(project_path, image_name)

        if result["success"]:
            print("\nApplication image is ready!")
            return result

        if attempt == max_retries:
            print("\nMaximum retry limit reached.")
            return result

        print("\nDocker build failed.")
        print("Sending error details to AI for correction...")

        current_dockerfile = dockerfile_path.read_text(encoding="utf-8")

        corrected_dockerfile = fix_dockerfile(current_dockerfile, result["error"])

        dockerfile_path.write_text(corrected_dockerfile + "\n", encoding="utf-8")

        print("\nDockerfile updated by AI.")

    return result
