import pytest

@pytest.fixture()
def package_name():
    # Setup
    name = 'pyshb'
    yield name
    # Teardown
