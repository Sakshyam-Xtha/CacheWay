from cacheway.utils.helper import env_setter, get_root_path, get_server_path


def test_get_root_path_points_to_project_root():
    root = get_root_path()
    assert (root / "pyproject.toml").exists()


def test_get_server_path_points_to_server_module():
    server_path = get_server_path()
    assert server_path.exists()
    assert server_path.name == "app.py"
    assert "src" in server_path.parts


def test_env_setter_writes_env_variables():
    env_file = get_root_path() / ".env"
    original = env_file.read_text() if env_file.exists() else None

    try:
        env_setter(8888, "example.com")
        content = env_file.read_text()
        assert "PORT" in content and "8888" in content
        assert "ORIGIN" in content and "example.com" in content
        assert "SERVER_PATH" in content and "app.py" in content
    finally:
        if original is not None:
            env_file.write_text(original)
        else:
            env_file.unlink(missing_ok=True)