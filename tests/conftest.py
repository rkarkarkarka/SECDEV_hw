# tests/conftest.py
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]  # корень репозитория
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app  # noqa: E402
from src.app import dependencies  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_state():
    dependencies.reset_state()
    yield


@pytest.fixture
def client():
    return TestClient(app)
