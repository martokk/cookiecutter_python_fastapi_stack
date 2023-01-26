"""This module is called after project is created."""
import os
import subprocess
import textwrap
from pathlib import Path

# Project root directory
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
PROJECT_PATH = Path.cwd().absolute()

# Values to generate github repository
GITHUB_USERNAME = "{{ cookiecutter.github_username }}"


def install_poetry() -> None:
    """Install poetry."""
    try:
        subprocess.check_output(["poetry", "--version"])
    except subprocess.CalledProcessError:
        print("Installing poetry: Running `make poetry-download`...")
        subprocess.check_call(["make", "poetry-download"])
        print("Poetry has been successfully downloaded.")


def init_git() -> None:
    """Initialize git repository."""
    os.chdir(PROJECT_PATH)
    print("Initializing git repository: Running `git init`...")
    subprocess.check_call(["git", "init"])

    print("Adding initial commit: Running `git add .`...")
    subprocess.check_call(["git", "add", "."])

    print("Creating main branch: Running `git branch -M main`...")
    subprocess.check_call(["git", "branch", "-M", "main"])

    print("Creating Remote on Github: Running `git remote add origin`...")
    subprocess.check_call(
        [
            "git",
            "remote",
            "add",
            "origin",
            f"https://github.com/{GITHUB_USERNAME}/{PROJECT_SLUG}.git",
        ]
    )

    print(
        "Creating Upsteam to python_fastapi_stack: Running `git remote add upstream`..."
    )
    subprocess.check_call(
        [
            "git",
            "remote",
            "add",
            "upstream",
            f"https://github.com/{GITHUB_USERNAME}/python_fastapi_stack.git",
        ]
    )


def install_dependencies() -> None:
    """Install dependencies."""
    print("Installing dependencies: Running `make install`...")
    subprocess.check_call(["make", "install"])


def install_pre_commit() -> None:
    """Install pre-commit hooks."""
    print("Installing pre-commit hooks: Running `make pre-commit-install`...")
    subprocess.check_call(["make", "pre-commit-install"])


def make_codestyle() -> None:
    """Run codestyle.""" ""
    print("Running codestyle: Running `make codestyle`...")
    subprocess.check_call(["make", "codestyle"])


def run_pre_commit() -> None:
    """Run pre-commit hooks."""
    print("Running pre-commit hooks: Running `pre-commit run --all-files`...")
    subprocess.check_call(["pre-commit", "run", "--all-files"])


def commit_git() -> None:
    """Commit git."""
    print("Committing initial commit: Running `git commit -m 'Initial commit'`...")
    subprocess.check_call(["git", "commit", "-q", "-m", "Initial commit"])


def init_alembic_database_migrations() -> None:
    """Run alembic database migrations."""
    print(
        "Running alembic database migrations: Running `alembic revision --autogenerate -m 'init'`..."
    )
    subprocess.check_call(
        ["poetry", "run", "alembic", "revision", "--autogenerate", "-m", "init"]
    )


def print_further_instructions() -> None:
    """Show user what to do next after project creation."""
    # old_message = f"""
    # Your project {project_slug} is created.

    # 1) Now you can start working on it:

    #     $ cd {project_slug} && git init

    # 2) If you don't have Poetry installed run:

    #     $ make poetry-download

    # 3) - Initialize poetry
    #    - Install pre-commit hooks
    #    - Run codestyle

    #     $ make install && make pre-commit-install && make codestyle

    # 4) Run initial Alembic database migration:
    #     $ alembic revision --autogenerate -m "init"

    # 5) Upload initial code to GitHub:

    #     $ git add .
    #     $ git commit -m ":tada: Initial commit"
    #     $ git branch -M main
    #     $ git remote add origin https://github.com/{GITHUB_USERNAME}/{project_slug}.git
    #     $ git push -u origin main
    # """

    message = f"""
    Your project {PROJECT_SLUG} is created, now you can start working on it:

    1) Upload initial code to GitHub:
        $ git push -u origin main
        
        
    2) Create a new branch for initial project setup:
        $ git checkout -b feature/init-project-setup
        
    3) Edit the following files:
        - .env

        
    
    """
    print(textwrap.dedent(message))


def main() -> None:
    install_poetry()
    install_dependencies()
    init_alembic_database_migrations()

    init_git()
    install_pre_commit()

    make_codestyle()
    run_pre_commit()
    commit_git()

    print_further_instructions()


if __name__ == "__main__":
    main()
