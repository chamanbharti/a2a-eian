from dataclasses import dataclass

VALID_ENVIRONMENTS = frozenset({
    "local",
    "test",
    "production",
})

VALID_LOG_LEVELS = frozenset({
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
})


@dataclass(frozen=True)
class AppConfig:
    service_name: str = "eian"
    environment: str = "local"
    log_level: str = "INFO"

    def __post_init__(self) -> None:
        if self.environment not in VALID_ENVIRONMENTS:
            raise ValueError(
                f"Unsupported environment: {self.environment}"
            )

        if self.log_level not in VALID_LOG_LEVELS:
            raise ValueError(
                f"Unsupported log level: {self.log_level}"
            )