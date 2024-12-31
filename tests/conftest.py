import pytest


@pytest.fixture
def libclamav_path() -> str:
    return "etc/libclamav.so"


@pytest.fixture
def database_config() -> dict:
    return {
        "PhishingSignatures": True,
        "PhishingScanUrls": True,
        "DetectPUA": True,
        "OfficialDatabaseOnly": True,
        "Bytecode": True,
    }
