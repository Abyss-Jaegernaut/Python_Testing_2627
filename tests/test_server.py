from unittest.mock import patch
import runpy


def test_app_runs_when_executed_directly():

    with patch("server.app.run") as mock_run:
        runpy.run_module("server", run_name="__main__")
        mock_run.assert_called_once()
