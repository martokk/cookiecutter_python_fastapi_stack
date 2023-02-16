"""This module is called after project is created."""
import os
import textwrap
from pathlib import Path
import shutil
import subprocess

# PROJECT_NAME = "Test Project"
# PROJECT_SLUG = "test_project"
# PROJECT_DESCRIPTION = "Test Project Description"
# FIRST_MODEL = "source"
# FIRST_SUPERUSER_USERNAME = "a7dj38fh"
# FIRST_SUPERUSER_EMAIL = "a7dj38fh@asdasd.com"
# FIRST_SUPERUSER_PASSWORD = "s5feY3A8"
# GITHUB_USERNAME = "github_username"
# EMAIL = "email@email.com"
# TELEGRAM_API_TOKEN = "123456"
# TELEGRAM_CHAT_ID = 0
# CWD = Path("~/temp").expanduser().absolute()


PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
PROJECT_DESCRIPTION = "{{ cookiecutter.project_description }}"
FIRST_MODEL = "{{ cookiecutter.first_model }}"
FIRST_SUPERUSER_USERNAME = "{{ cookiecutter.first_superuser_username }}"
FIRST_SUPERUSER_EMAIL = "{{ cookiecutter.first_superuser_email }}"
FIRST_SUPERUSER_PASSWORD = "{{ cookiecutter.first_superuser_password }}"
GITHUB_USERNAME = "{{ cookiecutter.github_username }}"
EMAIL = "{{ cookiecutter.email }}"
TELEGRAM_API_TOKEN = "{{ cookiecutter.telegram_api_token }}"
TELEGRAM_CHAT_ID = "{{ cookiecutter.telegram_chat_id }}"
CWD = Path.cwd().absolute()


PROJECT_PATH = CWD / PROJECT_SLUG
"""

- In messages:
    - Link to GitHub Action to await build fail/success for "dev" brannch.
    - edit .env file


"""


# OS FUNCTIONS
def delete_folder_if_exists(folder_name: str) -> None:
    """
    Delete the folder if it exists
    """
    if os.path.exists(folder_name):
        os.system(f"rm -rf {folder_name}")


def change_cwd(change_to: Path) -> None:
    """
    Change the current working directory
    """
    os.chdir(change_to)


def clone_example_files() -> None:
    """
    Clone the example files
    """
    example_files = Path(".").glob("**/*.example")

    for example_file in example_files:
        new_file = Path(example_file.name).stem
        new_file_path = example_file.parent.joinpath(new_file)
        shutil.copy(example_file, new_file_path)


def rename_filename_strings(find: str, replace: str) -> None:
    """
    Replace filename strings with given variable
    """
    for filename in Path(".").rglob(f"*{find}*"):
        os.rename(
            str(filename),
            str(filename).replace(find, replace),
        )


def replace_text_in_file(
    file_path: Path, find: str, replace: str, ignore: list[str] = []
) -> None:
    """
    Search and replace strings in a file
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            filedata = f.read().replace(find, replace)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(filedata)
    except UnicodeDecodeError:
        return


def replace_text_in_files(find: str, replace: str, ignore: list[str] = []) -> None:
    """
    Search and replace strings in all files
    """
    paths = Path(".").rglob("*")
    for filename in paths:
        if os.path.basename(filename) in ignore or any(
            element in ignore for element in os.path.split(filename)
        ):
            print(
                f"{filename} is in the ignore list, ignoring this file and all its children"
            )
            continue

        # Only open the file if it's a true file and not a folder
        if os.path.isfile(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    filedata = f.read().replace(find, replace)
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(filedata)
            except UnicodeDecodeError:
                continue


# GIT FUNCTIONS
def git_clone(clone_to: str) -> None:
    """
    Clone the repo
    """
    os.system(
        f"git clone https://github.com/martokk/python_fastapi_stack/ '{clone_to}'"
    )


def git_init_and_link_repo(project_slug: str) -> None:
    """
    Initialize git repo and link to github
    """
    os.system("git init")

    # Create remote ORIGIN for new project
    os.system(f"git remote add origin git@github.com:{project_slug}.git")

    # Create UPSTREAM remote for new project
    os.system(
        "git remote add upstream https://github.com/martokk/python_fastapi_stack.git"
    )


def git_commit(message: str) -> None:
    """
    Commit changes to git
    """
    os.system("git add .")
    os.system(f'git commit -m "{message}"')


def git_create_branch(branch_name: str) -> None:
    """
    Create a new branch
    """
    os.system(f"git branch {branch_name}")


def git_checkout_branch(branch_name: str) -> None:
    """
    Checkout a branch
    """
    os.system(f"git checkout {branch_name}")


def git_merge(
    merge_from: str,
    merge_to: str,
) -> None:
    """
    Merge a branch
    """
    git_checkout_branch(branch_name=merge_to)
    os.system(f"git merge {merge_from}")


def git_push(branch_name: str) -> None:
    """
    Push to git
    """
    # os.system(f"git push -u origin {branch_name}")
    print('os.system(f"git push -u origin {branch_name}")')


# POETRY FUNCTIONS
def install_poetry() -> None:
    """
    Install poetry.
    """
    try:
        subprocess.check_output(["poetry", "--version"])
    except subprocess.CalledProcessError:
        print("Installing poetry: Running `make poetry-download`...")
        subprocess.check_call(["make", "poetry-download"])
        print("Poetry has been successfully downloaded.")


# MAKEFILE FUNCTIONS
def install_dependencies() -> None:
    """
    Install dependencies.
    """
    print("Installing dependencies: Running `make install`...")
    subprocess.check_call(["make", "install"])


def install_pre_commit() -> None:
    """
    Install pre-commit hooks.
    """
    print("Installing pre-commit hooks: Running `make pre-commit-install`...")
    subprocess.check_call(["make", "pre-commit-install"])


# CODE LINTING, CHECKING, FORMATTING FUNCTIONS
def make_format() -> None:
    """
    Format the code.
    """
    print("Running `make format` to format the code...")
    subprocess.check_call(["make", "format"])


def make_check() -> None:
    """
    Check the code.
    """
    print("Running `make check` to check the code style, formatting...")
    subprocess.check_call(["make", "check"])


def make_test() -> None:
    """
    Run the tests.
    """
    print("Running `make test` to run the tests...")
    subprocess.check_call(["make", "test"])


# ALEMBIC FUNCTIONS
def alembic_init_db() -> None:
    """
    Initialize the database.
    """
    print("Initializing the database via Alembic: Running `make alembic-init`...")
    subprocess.check_call(["make", "alembic-init"])


# PYPROJECT FUNCTIONS
def bump_version(version: str) -> None:
    """
    Bump the version.
    """
    print(f"Bumping version to {version} via Poetry: Running `make bump-version`...")
    subprocess.check_call(["poetry", "version", version])


def print_further_instructions() -> None:
    """
    Show user what to do next after project creation.
    """
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


def clone_repo_and_init() -> None:
    """
    Clone the repo and initialize it.
    """
    # delete_folder_if_exists(folder_name=PROJECT_SLUG)
    git_clone(clone_to=".")
    # change_cwd(change_to=PROJECT_PATH)
    git_init_and_link_repo(project_slug=PROJECT_SLUG)
    bump_version(version="0.0.0")
    git_commit(message="Initial Commit")


def create_branch_and_checkout(branch_name: str) -> None:
    """
    Create a new branch and checkout to it.
    """
    git_create_branch(branch_name=branch_name)
    git_checkout_branch(branch_name=branch_name)


def generate_example_files() -> None:
    """
    Generates all `.example` files.
    """
    clone_example_files()

    file_path = Path(f"{CWD}/app/data/.env")
    ignore = [".git", ".vscode", "typings", ".gitignore"]
    env_find_replace = [
        (
            'UVICORN_ENTRYPOINT = "***********************************.core.app:app"',
            f'UVICORN_ENTRYPOINT = "{PROJECT_SLUG}.core.app:app"',
        ),
        (
            'EMAILS_FROM_EMAIL="***********************************"',
            f'EMAILS_FROM_EMAIL="{EMAIL}"',
        ),
        (
            'NOTIFY_EMAIL_TO="***********************************"',
            f'NOTIFY_EMAIL_TO="{EMAIL}"',
        ),
        (
            'FIRST_SUPERUSER_USERNAME="***********************************"',
            f'FIRST_SUPERUSER_USERNAME="{FIRST_SUPERUSER_USERNAME}"',
        ),
        (
            'FIRST_SUPERUSER_EMAIL="***********************************"',
            f'FIRST_SUPERUSER_EMAIL="{FIRST_SUPERUSER_EMAIL}"',
        ),
        (
            'FIRST_SUPERUSER_PASSWORD="***********************************"',
            f'FIRST_SUPERUSER_PASSWORD="{FIRST_SUPERUSER_PASSWORD}"',
        ),
        (
            'TELEGRAM_API_TOKEN = "***********************************"',
            f'TELEGRAM_API_TOKEN = "{TELEGRAM_API_TOKEN}"',
        ),
        ("TELEGRAM_CHAT_ID = 0", f"TELEGRAM_CHAT_ID = {TELEGRAM_CHAT_ID}"),
        (
            'PROJECT_NAME="***********************************"',
            f'PROJECT_NAME="{PROJECT_NAME}"',
        ),
        (
            'PROJECT_DESCRIPTION="***********************************"',
            f'PROJECT_DESCRIPTION="{PROJECT_DESCRIPTION}"',
        ),
    ]

    for find, replace in env_find_replace:
        replace_text_in_file(
            find=find, replace=replace, ignore=ignore, file_path=file_path
        )

    git_commit(message="Add example files")


def rename_folders_and_files() -> None:
    """
    Rename folders and files.
    """
    rename_filename_strings(find="python_fastapi_stack", replace=PROJECT_SLUG)
    git_commit(message=f"Renamed 'python_fastapi_stack' to '{PROJECT_SLUG}'")

    rename_filename_strings(find="video", replace=FIRST_MODEL)
    git_commit(message=f"Renamed 'video' to '{FIRST_MODEL}'")


def replace_strings_in_files() -> None:
    """
    Replace text in files.
    """
    replace_text_in_files(
        find="25113632+martokk@users.noreply.github.com",
        replace=EMAIL,
        ignore=[".git", "settings.json", "typings", ".gitignore"],
    )
    replace_text_in_files(
        find="Python FastAPI Stack: poetry, fastapi, sqlmodel, alembic, loguru, crud, notify.",
        replace=PROJECT_DESCRIPTION,
        ignore=[".git", "settings.json", "typings", ".gitignore"],
    )
    replace_text_in_files(
        find="martokk",
        replace=GITHUB_USERNAME,
        ignore=[".git", "settings.json", "typings", ".gitignore"],
    )
    replace_text_in_files(
        find="python_fastapi_stack",
        replace=PROJECT_SLUG,
        ignore=[".git", "settings.json", "typings"],
    )
    replace_text_in_files(
        find="Python FastAPI Stack",
        replace=PROJECT_NAME,
        ignore=[".git", "settings.json", "typings", ".gitignore"],
    )

    replace_text_in_files(
        find="video",
        replace=FIRST_MODEL,
        ignore=[".git", "settings.json", "typings", ".gitignore"],
    )
    replace_text_in_files(
        find="Video",
        replace=FIRST_MODEL.title().replace("_", "").replace("-", ""),
        ignore=[".git", "settings.json", "typings", ".gitignore"],
    )
    replace_text_in_files(
        find="VIDEO",
        replace=FIRST_MODEL.upper().replace(" ", "_").replace("-", "_"),
        ignore=[".git", "settings.json", "typings", ".gitignore"],
    )
    git_commit(message=f"Replaced 'video' to '{FIRST_MODEL}'")


def install_project() -> None:
    """
    Install project.
    """
    install_poetry()
    install_dependencies()
    install_pre_commit()
    git_commit(message="Installed project")
    alembic_init_db()
    git_commit(message="Initialized database")


def format_and_test() -> None:
    """
    Format and test project.
    """
    make_format()
    make_check()
    git_commit(message="Formatted and checked code")

    make_test()


def bump_and_merge() -> None:
    """
    Bump version and merge branch.
    """
    git_merge(merge_from="cookiecutter-init", merge_to="dev")
    git_push(branch_name="dev")

    bump_version(version="0.0.1")


def main() -> None:
    """
    Main function.
    """
    change_cwd(change_to=CWD)
    print("Running post_gen_project.py")
    print("PROJECT_PATH: ", PROJECT_PATH)
    print("PROJECT_SLUG: ", PROJECT_SLUG)
    print("GITHUB_USERNAME: ", GITHUB_USERNAME)
    print("CWD: ", os.getcwd())

    clone_repo_and_init()
    create_branch_and_checkout(branch_name="dev")
    create_branch_and_checkout(branch_name="cookiecutter-init")

    generate_example_files()

    rename_folders_and_files()
    replace_strings_in_files()

    install_project()

    format_and_test()
    bump_and_merge()

    print_further_instructions()


if __name__ == "__main__":
    main()
