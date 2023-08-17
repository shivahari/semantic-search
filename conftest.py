import os
import pytest
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def url():
    "URL for the test suite"
    return os.environ.get('URL')

