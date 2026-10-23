#!/usr/bin/env python3
import os
import yaml

def find_models():
    models = []
    port = 8001
    root_dirs = ["llm", "tts", "stt"]
    for category_dir in root_dirs:
        if not os.path.isdir(category_dir):
            continue
        for model_name in sorted(os.listdir(category_dir)):
            model_path = os.path.join(category_dir, model_name)
            if os.path.isdir(model_path):
                dockerfile_path = os.path.join(model_path, "Dockerfile")
                dockerfile_lower = os.path.join(model_path, "dockerfile")
                requirements_path = os.path.join(model_path, "requirements.txt")
                demo_path = os.path.join(model_path, "demo.py")
                has_dockerfile = os.path.exists(dockerfile_path) or os.path.exists(dockerfile_lower)
                has_requirements = os.path.exists(requirements_path)
                has_demo = os.path.exists(demo_path)
                if has_dockerfile and has_requirements and has_demo:
                    dockerfile_name = "Dockerfile" if os.path.exists(dockerfile_path) else "dockerfile"
                    models.append({
                        "name": model_name,
                        "category": category_dir,
                        "path": model_path,
                        "dockerfile_name": dockerfile_name,
                        "port": port
                    })
                    port += 1
    return models

def generate_compose():
    models = find_models()
    if not models:
        print("No containerized models found in llm/, tts/, or stt/.")
        return

    services = {}
    for model in models:
        service_name = model["name"].replace("-", "_").replace(".", "_").lower()
        services[service_name] = {
            "build": {
                "context": f"./{model['path']}",
                "dockerfile": model["dockerfile_name"]
            },
            "profiles": [model["category"]],
            "ports": [f"{model['port']}:8000"],
            "volumes": [
                f"./{model['path']}:/app",
                f"./models/{model['name']}:/app/models",
                "~/.cache/huggingface:/root/.cache/huggingface"
            ],
            "environment": {
                "MODEL_NAME": model["name"],
                "PORT": "8000"
            },
            "restart": "no",
            "container_name": f"model-{model['name']}",
            "stdin_open": True,
            "tty": True
        }

    compose_dict = {
        "version": "3.9",
        "services": services,
        "networks": {
            "models-network": {"driver": "bridge"}
        }
    }

    for service in compose_dict["services"].values():
        service["networks"] = ["models-network"]

    with open("docker-compose.yml", "w", encoding="utf-8") as f:
        yaml.dump(compose_dict, f, default_flow_style=False, sort_keys=False)

    print(f"Generated docker-compose.yml with {len(models)} services across profiles: llm, tts, stt")
    print("Execution Guide:")
    print("  1. Build Base Image:")
    print("     docker build -f Dockerfile.base -t ml-base-cpu:latest .")
    print("  2. Run specific category without OOM crash:")
    print("     docker compose --profile llm up -d")
    print("     docker compose --profile tts up -d")
    print("     docker compose --profile stt up -d")
    print("  3. Run single model:")
    print("     docker compose up <service-name>")
    print("  Note: CV models run natively via cv/run_all_tests.sh for direct webcam/display access.")

if __name__ == "__main__":
    generate_compose()
