from unittest.mock import patch

from fastapi import Request
from sqlmodel import Session

from {{ cookiecutter.project_slug }}.views.endpoints.{{ cookiecutter.first_model }}s import html_view_{{ cookiecutter.first_model }}s


async def test_html_view_{{ cookiecutter.first_model }}s(db_with_{{ cookiecutter.first_model }}s: Session, test_request: Request) -> None:
    """
    Test that the html_view_{{ cookiecutter.first_model }}s function returns a response with the correct status code.
    """
    with patch(
        "{{ cookiecutter.project_slug }}.views.endpoints.{{ cookiecutter.first_model }}s.templates.TemplateResponse"
    ) as mock_template_response:
        await html_view_{{ cookiecutter.first_model }}s(
            request=test_request,
            db=db_with_{{ cookiecutter.first_model }}s,
        )

        assert mock_template_response.called

        # Test that the correct arguments are passed to the TemplateResponse
        assert mock_template_response.call_args[0][0] == "view_{{ cookiecutter.first_model }}s.html"

        response_context = mock_template_response.call_args[0][1]
        assert response_context["request"] == test_request
        assert len(response_context["{{ cookiecutter.first_model }}s"]) == 3
