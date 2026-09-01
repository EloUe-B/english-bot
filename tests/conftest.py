import os
import sys
import types
from unittest.mock import MagicMock

os.environ.setdefault("GEMINI_API_KEY", "fake-key")
os.environ.setdefault("GEMINI_MODEL", "fake-model")
os.environ.setdefault("BOT_TOKEN", "fake-token")

dotenv_stub = types.ModuleType("dotenv")
dotenv_stub.load_dotenv = MagicMock()
sys.modules["dotenv"] = dotenv_stub

genai_client_stub = types.ModuleType("google.genai.client")
genai_client_stub.Client = MagicMock()
genai_client_stub.AsyncClient = MagicMock()
sys.modules["google.genai.client"] = genai_client_stub

genai_stub = types.ModuleType("google.genai")
genai_stub.Client = MagicMock()
genai_stub.client = genai_client_stub
sys.modules["google.genai"] = genai_stub

genai_types_stub = types.ModuleType("google.genai.types")
genai_types_stub.GenerateContentConfig = MagicMock()
sys.modules["google.genai.types"] = genai_types_stub
