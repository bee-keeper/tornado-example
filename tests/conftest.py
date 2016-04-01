import pytest

import example.server


@pytest.fixture
def app():
    """Tornado server instance"""
    return example.server.initialise()
