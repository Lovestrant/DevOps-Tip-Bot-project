"""DevOps Tip Bot - prints a random DevOps tip with some runtime info."""
import os
import platform
import random
import socket
from datetime import datetime, timezone

TIPS = [
    "Automate everything you do more than twice.",
    "Keep your Docker images small: use slim base images.",
    "Never hardcode secrets. Use a credentials store.",
    "A pipeline that is not versioned in Git is not a pipeline.",
    "Fail fast: run your quickest tests first.",
    "Tag images with build numbers, not just 'latest'.",
    "If it hurts, do it more often (continuous integration).",
]


def get_tip() -> str:
    return random.choice(TIPS)


def main() -> None:
    print("=" * 50)
    print("DevOps Tip Bot")
    print("=" * 50)
    print(f"Time      : {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print(f"Host      : {socket.gethostname()}")
    print(f"Python    : {platform.python_version()}")
    print(f"Build tag : {os.getenv('BUILD_TAG', 'local')}")
    print("-" * 50)
    print(f"Tip: {get_tip()}")


if __name__ == "__main__":
    main()
