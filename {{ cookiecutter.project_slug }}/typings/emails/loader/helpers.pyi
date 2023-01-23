"""
This type stub file was generated by pyright.
"""

__all__ = ['guess_charset', 'fix_content_type']
class ReRules:
    re_meta = ...
    re_is_http_equiv = ...
    re_parse_http_equiv = ...
    re_charset = ...
    def __init__(self, conv=...) -> None:
        ...



RULES_U = ...
RULES_B = ...
def guess_text_charset(text, is_html=...): # -> str | None:
    ...

def guess_html_charset(html): # -> str | None:
    ...

def guess_charset(headers, html): # -> str | bytes | None:
    ...

COMMON_CHARSETS = ...
def decode_text(text, is_html=..., guess_charset=..., try_common_charsets=..., charsets=..., fallback_charset=...): # -> tuple[Unknown, None] | tuple[Unknown | str | bytes | None, Unknown]:
    ...