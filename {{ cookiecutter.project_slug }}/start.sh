#!/bin/sh

alembic upgrade head

python -m {{ cookiecutter.project_slug }}
