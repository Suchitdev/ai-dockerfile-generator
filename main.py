import argparse
import re
import sys
from pathlib import Path

from dockerfile_writer import create_dockerfile
from error_fixer import build_with_auto_fix


def generate_image_name(project_path):
    project_name = project_path.name.lower()

    project_name = re.sub(r"[^a-z0-9_.-]+", "-", project_name).strip("-._")

    if not project_name:
        project_name = "application"

    return f"ai-generated-{project_name}:latest"


def main():
    parser = argparse.ArgumentParser(
        description="AI-powered Dockerfile generator and builder"
    )

    parser.add_argument(
        "project_path", help="Path to the application you want to Dockerize"
    )

    args = parser.parse_args()
    project_path = Path(args.project_path).resolve()

    if not project_path.exists() or not project_path.is_dir():
        print(f"Error: Invalid project directory: {project_path}")
        sys.exit(1)

    image_name = generate_image_name(project_path)

    print("\n======================================")
    print("       AI DOCKERFILE GENERATOR")
    print("======================================")
    print(f"\nProject: {project_path}")
    print(f"Docker image: {image_name}")

    try:
        print("\n[STEP 1] Generating Dockerfile...")

        create_dockerfile(project_path, overwrite=True)

        print("\n[STEP 2] Building Docker image...")

        result = build_with_auto_fix(project_path, image_name, max_retries=3)

        if result["success"]:
            print("\nSUCCESS: Docker image created!")
            print(f"Image: {image_name}")
            print(f"Inspect with: docker images {image_name}")
            return

        print("\nFAILED: Docker build could not be completed.")
        sys.exit(1)

    except Exception as error:
        print(f"\nERROR: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
