import pytest


@pytest.fixture
def libclamav_path() -> str:
    return "etc/libclamav.so"


@pytest.fixture
def database_config() -> dict:
    return {
        "phishing_signatures": True,
        "phishing_scan_urls": True,
        "detect_pua": True,
        "official_database_only": True,
        "bytecode": True,
    }
