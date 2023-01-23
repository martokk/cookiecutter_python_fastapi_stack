from unittest.mock import patch

from {{ cookiecutter.project_slug }}.__main__ import main


def test_main() -> None:
    """
    test __main__.py
    """
    with patch("{{ cookiecutter.project_slug }}.__main__.typer_app") as mock_typer_app:
        main()

    assert mock_typer_app.called
    assert mock_typer_app.call_count == 1
