"""
This type stub file was generated by pyright.
"""

class DKIMSigner:
    def __init__(self, selector, domain, key=..., ignore_sign_errors=..., **kwargs) -> None:
        ...

    def get_sign_string(self, message): # -> bytes | None:
        ...

    def get_sign_header(self, message): # -> tuple[bytes | str, bytes | str] | None:
        ...

    def sign_message(self, msg):
        """
        Add DKIM header to email.message
        """
        ...

    def sign_message_string(self, message_string): # -> bytes:
        """
        Insert DKIM header to message string
        """
        ...