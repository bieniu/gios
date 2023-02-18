"""GIOS exceptions."""


class GiosError(Exception):
    """Base class for GIOS errors."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status


class ApiError(GiosError):
    """Raised when GIOS API request ended in error."""


class InvalidSensorsDataError(GiosError):
    """Raised when sensors data is invalid."""


class NoStationError(GiosError):
    """Raised when no measuring station error."""
