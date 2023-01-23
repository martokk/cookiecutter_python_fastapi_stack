from {{ cookiecutter.project_slug }} import logger
from {{ cookiecutter.project_slug }}.core.cli import typer_app


def main():
    logger.info("--- Start ---")
    logger.info(f"Starting Typer App: '{typer_app.info.name}'...")
    typer_app()


if __name__ == "__main__":
    main()  # pragma: no cover
