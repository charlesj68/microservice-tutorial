"""Create the Flask app for the locations service."""
from flask import Flask, jsonify
import orders
import excepts


def create_app():
    """Create and return app instance."""
    app = Flask("locations")
    app.register_blueprint(orders.api)

    @app.errorhandler(excepts.ErrorStatus)
    def handle_conflict_usage(error):
        """Create handler for ErrorStatus exceptions."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
