"""This module is called before project is created."""

import re
import sys

import os
from pathlib import Path

PROJECT_SLUG = "tubecast"
GITHUB_USERNAME = "martokk"
# PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
# GITHUB_USERNAME = "{{ cookiecutter.github_username }}"

MODULE_REGEX = re.compile(r"^[a-z][a-z0-9\-\_]+[a-z0-9]$")
SEMVER_REGEX = re.compile(
    r"""
        ^
        (?P<major>0|[1-9]\d*)
        \.
        (?P<minor>0|[1-9]\d*)
        \.
        (?P<patch>0|[1-9]\d*)
        (?:-(?P<prerelease>
            (?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
            (?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*
        ))?
        (?:\+(?P<build>
            [0-9a-zA-Z-]+
            (?:\.[0-9a-zA-Z-]+)*
        ))?
        $
    """,
    re.VERBOSE,
)


def validate_project_slug(project_slug: str) -> None:
    """Ensure that `project_name` parameter is valid.

    Valid inputs starts with the lowercase letter.
    Followed by any lowercase letters, numbers or underscores.

    Args:
        project_name: current project name

    Raises:
        ValueError: If project_name is not a valid Python module name
    """
    if MODULE_REGEX.fullmatch(project_slug) is None:
        message = f"ERROR: The project name `{project_slug}` is not a valid Python module name."
        raise ValueError(message)


def clone_repo(project_slug: str) -> None:
    """
    Clone the repo to the current directory
    """
    os.system(
        f"git clone https://github.com/martokk/python_fastapi_stack/ {project_slug}"
    )


def init_and_link_repo() -> None:
    """
    Initialize git repo and link to github
    """
    os.chdir(f"{PROJECT_SLUG}")
    os.system("git init")
    os.system(f"git remote add origin git@github.com:{PROJECT_SLUG}.git")
    os.system(
        "git remote add upstream https://github.com/martokk/python_fastapi_stack.git"
    )


def rename_filename_strings(find: str, replace: str) -> None:
    """
    Replace filename strings with given variable
    """
    for filename in Path(".").rglob(f"*{find}*"):
        os.rename(
            str(filename),
            str(filename).replace(find, replace),
        )


def git_commit(message: str) -> None:
    """
    Commit changes to git
    """
    os.system("git add .")
    os.system(f'git commit -m "{message}"')


def replace_file_strings(find: str, replace: str) -> None:
    """
    Search and replace strings in all files
    """
    for filename in Path(".").rglob("*"):
        with open(filename, "r") as f:
            filedata = f.read()
        filedata = filedata.replace(find, replace)
        with open(filename, "w") as f:
            f.write(filedata)


def main() -> None:
    try:
        # validate_project_slug(project_slug=PROJECT_SLUG)

        # Clone the repo
        clone_repo(project_slug="{{ cookiecutter.project_slug }}")
        git_commit("Initial commit")
        print("Successfully cloned the repo")

        # Initialize and link the git repo
        init_and_link_repo()
        git_commit("Initialized and linked the git repo")
        print("Successfully initialized and linked the git repo")

        # Replace the filename strings
        rename_filename_strings(
            find="python_fastapi_stack", replace="{{ cookiecutter.project_slug }}"
        )
        git_commit(
            "Replaced python_fastapi_stack with {{ cookiecutter.project_slug }} in filenames"
        )
        print("Successfully replaced the filename strings")

        # Replace the file strings
        replace_file_strings(
            find="python_fastapi_stack", replace="{{ cookiecutter.project_slug }}"
        )
        git_commit(
            "Replaced python_fastapi_stack with {{ cookiecutter.project_slug }} in files"
        )
        print("Successfully replaced the file strings")

    except ValueError as ex:
        print(ex)
        sys.exit(1)


if __name__ == "__main__":
    main()
