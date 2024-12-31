import pytest

from libclamav_py.config.database import DatabaseConfig


class TestDatabaseConfig:
    def test_initialization(self, database_config: dict):
        config = DatabaseConfig.model_validate(database_config)
        assert config.phishing_signatures is True
        assert config.phishing_scan_urls is True
        assert config.detect_pua is True
        assert config.official_database_only is True
        assert config.bytecode is True

    @pytest.mark.parametrize(
        "config, hex",
        [
            (DatabaseConfig(PhishingScanUrls=True), 8202),
            (DatabaseConfig(PhishingSignatures=True), 8202),
            (DatabaseConfig(DetectPUA=True), 8218),
            (DatabaseConfig(OfficialDatabaseOnly=True), 12298),
            (DatabaseConfig(Bytecode=True), 8202),
        ],
    )
    def test_to_big_flag(self, config, hex):
        assert config._to_bit_flag().value == hex
