"""Provide an error status exception for use in Flask API."""


class ErrorStatus(Exception):
    """Define an exception that handles HTTP Status Codes."""

    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        """Initialize exception."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Convert payload and message members into a dict."""
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
