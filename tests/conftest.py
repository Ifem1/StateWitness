import os
import tempfile

import pytest


@pytest.fixture
def direct_llm(direct_vm):
    """Compatibility wrapper for the genlayer-test 0.29 VM mock API."""
    class LLM:
        def __init__(self):
            self._response = ""

        @property
        def mock_response(self):
            return self._response

        @mock_response.setter
        def mock_response(self, response):
            self._response = response
            direct_vm.clear_mocks()
            direct_vm.mock_llm(r"(?s).*", response)

    return LLM()


@pytest.fixture(autouse=True)
def direct_pickling_check(direct_vm):
    direct_vm.check_pickling = True


@pytest.fixture(autouse=True)
def windows_gltest_tempfile_cleanup(monkeypatch):
    """Defer one known gltest fd-0 temp-file unlink failure on Windows."""
    if os.name != "nt":
        return

    original_unlink = os.unlink

    def unlink(path, *args, **kwargs):
        try:
            return original_unlink(path, *args, **kwargs)
        except PermissionError:
            normalized = os.path.normcase(os.path.abspath(path))
            temp_root = os.path.normcase(os.path.abspath(tempfile.gettempdir()))
            if os.path.dirname(normalized) == temp_root and os.path.basename(normalized).startswith("tmp"):
                return None
            raise

    monkeypatch.setattr(os, "unlink", unlink)
