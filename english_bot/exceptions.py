class AppError(Exception):
    """Base class for all bot-specific errors."""


class ConfigError(AppError):
    """Raised when required env variables are missing or invalid."""


class AIError(AppError):
    """Raised when the Gemini API call fails."""
