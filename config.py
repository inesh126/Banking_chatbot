import os
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SIMULATION_DATA_FILE = DATA_DIR / "simulation.json"
KNOWLEDGE_BASE_FILE = DATA_DIR / "knowledge_base.json"
ENV_FILE = BASE_DIR / ".env"
LOCAL_SITE_PACKAGES = BASE_DIR / ".venv" / "Lib" / "site-packages"


def _bootstrap_local_venv():
    if not LOCAL_SITE_PACKAGES.exists():
        return

    local_site_packages = str(LOCAL_SITE_PACKAGES)
    if local_site_packages not in sys.path:
        sys.path.insert(0, local_site_packages)


def _load_dotenv_file():
    if not ENV_FILE.exists():
        return

    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


_bootstrap_local_venv()
_load_dotenv_file()

LLM_API_URL = os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")
LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "20"))
