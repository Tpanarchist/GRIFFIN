"""
Smoke tests for initial package imports.
"""
import griffin
from griffin.cli.main import main


def test_imports_and_main():
    assert hasattr(griffin, "__version__")
    assert main(()) == 0
