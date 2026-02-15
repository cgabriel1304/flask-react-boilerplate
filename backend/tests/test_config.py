"""Tests for configuration classes."""
from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig, config


class TestBaseConfig:
    def test_sqlalchemy_track_modifications_disabled(self):
        assert Config.SQLALCHEMY_TRACK_MODIFICATIONS is False

    def test_secret_key_has_default(self):
        assert Config.SECRET_KEY is not None


class TestDevelopmentConfig:
    def test_debug_enabled(self):
        assert DevelopmentConfig.DEBUG is True

    def test_sqlalchemy_echo_enabled(self):
        assert DevelopmentConfig.SQLALCHEMY_ECHO is True

    def test_database_uri_set(self):
        assert DevelopmentConfig.SQLALCHEMY_DATABASE_URI is not None
        assert 'postgresql' in DevelopmentConfig.SQLALCHEMY_DATABASE_URI


class TestTestingConfig:
    def test_testing_enabled(self):
        assert TestingConfig.TESTING is True

    def test_uses_sqlite_memory(self):
        assert TestingConfig.SQLALCHEMY_DATABASE_URI == 'sqlite:///:memory:'


class TestProductionConfig:
    def test_debug_disabled(self):
        assert ProductionConfig.DEBUG is False

    def test_sqlalchemy_echo_disabled(self):
        assert ProductionConfig.SQLALCHEMY_ECHO is False


class TestConfigDict:
    def test_all_environments_present(self):
        assert 'development' in config
        assert 'testing' in config
        assert 'production' in config
        assert 'default' in config

    def test_default_is_development(self):
        assert config['default'] is DevelopmentConfig
