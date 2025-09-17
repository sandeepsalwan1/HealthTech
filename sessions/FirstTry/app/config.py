import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

APP_NAME: str = os.getenv("APP_NAME", "HealthTech")
BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")

OPENAI_API_KEY: Optional[str] = (os.getenv("OPENAI_API_KEY", "").strip() or None)
TAVILY_API_KEY: Optional[str] = (os.getenv("TAVILY_API_KEY", "").strip() or None)

ALLOW_DEMO_LOGIN: bool = os.getenv("APP_ALLOW_DEMO_LOGIN", "true").lower() in ("1", "true", "yes", "y")
FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "*")
AGENT_THREAD_ID: str = os.getenv("AGENT_THREAD_ID", "demo-thread")


def get_logo_path() -> Optional[str]:
	"""Return an absolute path to a suitable logo image if available."""
	here = Path(__file__).resolve()
	# Search up to a few parent directories for logo.png, then fallback to resources/example.jpeg
	for i in range(min(6, len(here.parents))):
		candidate = here.parents[i] / "logo.png"
		if candidate.exists():
			return str(candidate)
	for i in range(min(6, len(here.parents))):
		candidate = here.parents[i] / "resources" / "example.jpeg"
		if candidate.exists():
			return str(candidate)
	return None


def get_openai_client():
	"""Return an OpenAI client if an API key is configured, otherwise None."""
	if not OPENAI_API_KEY:
		return None
	from openai import OpenAI
	return OpenAI(api_key=OPENAI_API_KEY)