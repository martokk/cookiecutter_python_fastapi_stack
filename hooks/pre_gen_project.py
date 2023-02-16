"""This module is called before project is created."""

import re
import shutil
import sys

import os
from pathlib import Path


PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
GITHUB_USERNAME = "{{ cookiecutter.github_username }}"
PROJECT_ROOT = Path().cwd() / PROJECT_SLUG

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


def main() -> None:
    try:
        validate_project_slug(project_slug=PROJECT_SLUG)
        print("\n\nEnding Pre Generation Hook\n\n")

    except ValueError as ex:
        print(ex)
        sys.exit(1)


if __name__ == "__main__":
    main()
