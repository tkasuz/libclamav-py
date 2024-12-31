from pathlib import Path

import pytest
from pydantic import ByteSize

from libclamav_py.clamav import Client
from libclamav_py.config.engine import EngineConfig, PUAConfig
from libclamav_py.utils.constant import MB


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

    def test_set_engine_conf(self, client):
        client.set_engine_conf(EngineConfig(MaxScanSize=ByteSize(100 * MB)))

        config = client.get_engine_conf()
        assert config.max_scan_size == 100 * MB

    def test_set_pua_conf(self, client):
        client.set_pua_conf(PUAConfig(enabled=True, excludes=["NetTool", "PWTool"]))
        client.set_pua_conf(PUAConfig(enabled=True, includes=["Spy", "Scanner", "RAT"]))


def test_from_clamd_conf():
    Client.from_clamd_conf(clamd_conf_path="etc/clamd.conf")
