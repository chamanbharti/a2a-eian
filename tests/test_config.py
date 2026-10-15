from dataclasses import FrozenInstanceError

import pytest
from eian.config import AppConfig


def test_default_configuration() -> None:
    config = AppConfig()

    assert config.service_name == "eian"
    assert config.environment == "local"
    assert config.log_level == "INFO"


def test_custom_configuration() -> None:
    config = AppConfig(
        service_name="claims-agent",
        environment="test",
        log_level="DEBUG",
    )

    assert config.service_name == "claims-agent"
    assert config.environment == "test"
    assert config.log_level == "DEBUG"


def test_configuration_is_immutable() -> None:
    config = AppConfig()

    with pytest.raises(FrozenInstanceError):
        config.environment = "production"  # type: ignore[misc]

def test_invalid_environment() -> None:
    with pytest.raises(ValueError, match="Unsupported environment"):
        AppConfig(environment="development")


def test_invalid_log_level() -> None:
    with pytest.raises(ValueError, match="Unsupported log level"):
        AppConfig(log_level="TRACE")        