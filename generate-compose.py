#!/usr/bin/env python3
"""
Auto-detect models and generate docker-compose.yml
Papkalarni avtomatik skanir qiladi va docker-compose.yml ni yaratadi
Usage: python3 generate-compose.py
"""

import os
import yaml
from pathlib import Path

def find_models():
    """Papkalarda models ni topadi"""
    models = []
    port = 8001
    # Root papkalarni skanir qil
    root_dirs = ['cv', 'nlp', 'tts', 'stt', 'llm', 'vision', 'audio', 'models']
    for category_dir in root_dirs:
        if not os.path.isdir(category_dir):
            continue
        # Har bir category ichidagi papkalarni skanir qil
        for model_name in os.listdir(category_dir):
            model_path = os.path.join(category_dir, model_name)
            # Agar papka va Dockerfile/dockerfile bor bo'lsa
            if os.path.isdir(model_path):
                dockerfile_path = os.path.join(model_path, 'Dockerfile')
                dockerfile_lower = os.path.join(model_path, 'dockerfile')
                requirements_path = os.path.join(model_path, 'requirements.txt')
                demo_path = os.path.join(model_path, 'demo.py')
                # Har biri mavjud bo'lsa model deb hisoblash
                has_dockerfile = os.path.exists(dockerfile_path) or os.path.exists(dockerfile_lower)
                has_requirements = os.path.exists(requirements_path)
                has_demo = os.path.exists(demo_path)
                if has_dockerfile and has_requirements and has_demo:
                    dockerfile_name = 'Dockerfile' if os.path.exists(dockerfile_path) else 'dockerfile'
                    models.append({
                        'name': model_name,
                        'path': model_path,
                        'dockerfile_name': dockerfile_name,   # faqat fayl nomi, to'liq yo'l emas
                        'port': port
                    })
                    port += 1
    return models

def generate_compose():
    """Generate docker-compose.yml"""
    models = find_models()
    if not models:
        print("❌ Hech qanday model topilmadi!")
        print("📁 Iltimos, quyidagi struktura tuzib fayllarni to'ldiring:")
        print("""
category/model-name/
├── Dockerfile
├── requirements.txt
└── demo.py
""")
        return
    services = {}
    for model in models:
        service_name = model['name'].replace("-", "_").replace(".", "_").lower()
        services[service_name] = {
            "build": {
                "context": f"./{model['path']}",      # <-- tuzatildi: model o'z papkasi
                "dockerfile": model['dockerfile_name']  # <-- tuzatildi: faqat fayl nomi
            },
            "ports": [f"{model['port']}:8000"],
            "volumes": [
                f"./{model['path']}:/app",
                f"./models/{model['name']}:/app/models"
            ],
            "environment": {
                "MODEL_NAME": model['name'],
                "PORT": "8000"
            },
            "restart": "unless-stopped",
            "container_name": f"model-{model['name']}",
            "stdin_open": True,
            "tty": True
        }
    # docker-compose.yml structure
    compose_dict = {
        "version": "3.9",
        "services": services,
        "volumes": {},
        "networks": {
            "models-network": {
                "driver": "bridge"
            }
        }
    }
    # Add network to all services
    for service in compose_dict["services"].values():
        service["networks"] = ["models-network"]
    # Write docker-compose.yml
    with open("docker-compose.yml", "w") as f:
        yaml.dump(compose_dict, f, default_flow_style=False, sort_keys=False)
    print(f"✅ docker-compose.yml generated with {len(models)} models\n")
    print("📋 Models:")
    for model in models:
        print(f"  • {model['name']:<30} → http://localhost:{model['port']}")
    print("\n🚀 Run:")
    print("  docker build -f Dockerfile.base -t ml-base-cpu:latest .   # avval, bir marta")
    print("  docker compose up <model-name> --build                    # bir modelni ishga tushir")
    print("  docker compose up --build                                 # hammani ishga tushir")

if __name__ == "__main__":
    generate_compose()