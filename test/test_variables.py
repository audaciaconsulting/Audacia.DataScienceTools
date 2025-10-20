import pytest
import os
from unittest.mock import patch
from dstools.variables import get_env_var


class TestGetEnvVar:

    def test_get_existing_env_var(self, monkeypatch):
        """Test retrieving an existing environment variable."""
        monkeypatch.setenv("TEST_VAR", "test_value")

        with patch('dstools.variables.load_dotenv'):
            result = get_env_var("TEST_VAR")
            assert result == "test_value"

    def test_missing_env_var_raises_error(self):
        """Test that missing variable raises ValueError."""
        with patch('dstools.variables.load_dotenv'):
            with patch.dict(os.environ, {}, clear=True):
                with pytest.raises(ValueError, match="TEST_VAR not found"):
                    get_env_var("TEST_VAR")