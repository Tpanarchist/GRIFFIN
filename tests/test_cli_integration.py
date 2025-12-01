def test_cli_ping_integration() -> None:
    import sys
    import subprocess

    # Run the CLI module and capture output
    proc = subprocess.run([sys.executable, "-m", "griffin.cli.main", "ping"], capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")

    assert "Reply from ACEStack" in out
    assert "echo: ping from CLI" in out
