"""Shared pytest configuration for openmc-agent."""
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-k \"not slow\"')")
