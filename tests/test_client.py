from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from libclamav_py.clamav import Client


@pytest.fixture
def client():
    client = Client()
    yield client
    del client


@pytest.mark.skipif(
    not Path("/opt/lib/libclamav.so").exists(), reason="Not implemented"
)
class TestClient:
    def test_scan_file(self, client):
        client.load_db()
        client.compile_engine()

        result = client.scan_file("etc/no_virus.txt")
        assert result is None


def test_from_clamd_conf(mocker: MockerFixture):
    mocker.patch("libclamav_py.clamav.Client.__init__", return_value=None)
    mocker.patch("libclamav_py.clamav.Client.set_engine_conf")
    Client.from_clamd_conf(clamd_conf_path="etc/clamd.conf")
