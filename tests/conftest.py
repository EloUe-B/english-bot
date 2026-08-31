import sys
import types
from unittest.mock import MagicMock

dotenv_stub = types.ModuleType("dotenv")
dotenv_stub.load_dotenv = MagicMock()
sys.modules["dotenv"] = dotenv_stub

genai_stub = types.ModuleType("google.genai")
genai_stub.Client = MagicMock()
sys.modules["google.genai"] = genai_stub

genai_types_stub = types.ModuleType("google.genai.types")
genai_types_stub.GenerateContentConfig = MagicMock()
sys.modules["google.genai.types"] = genai_types_stub
