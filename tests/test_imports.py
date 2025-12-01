def test_basic_imports() -> None:
    import griffin  # noqa: F401
    from griffin.core import atoms, version  # noqa: F401
    from griffin.infra import config  # noqa: F401
    from griffin.ace import ace_message  # noqa: F401
    from griffin.cli import main  # noqa: F401

def test_ace_message_dict_roundtrip() -> None:
    from griffin.ace.ace_message import ACEMessage

    msg = ACEMessage(content="test content", source="test", role="user")
    d = msg.to_dict()

    assert d["content"] == "test content"
    assert d["role"] == "user"
    assert "created_at" in d
    assert "id" in d
