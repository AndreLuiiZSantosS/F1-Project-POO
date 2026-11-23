import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ui import UI


class LoginTests(unittest.TestCase):
    @patch("ui.View.cliente_autenticar", return_value=None)
    @patch("builtins.input", side_effect=["admin", "admin"])
    def test_hardcoded_admin_credentials_are_rejected(self, _input, _authenticate):
        UI.is_admin = True

        self.assertFalse(UI.login())
        self.assertFalse(UI.is_admin)


if __name__ == "__main__":
    unittest.main()
