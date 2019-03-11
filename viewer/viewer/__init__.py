"""Provide a viewer into the Orders data."""
from datetime import datetime
from flask import Flask, render_template
from requests import get


def create_app():
    """Create Flask application."""
    app = Flask(__name__)

    @app.route('/debug', methods=['GET'])
    def debug():
        """Simply return a string to indicate aliveness."""
        return "Hello World"

    @app.route('/', methods=['GET'])
    def main_page():
        """Create home page for viewer app."""
        # Get various lists from Locations service
        # LOCATIONS_HOST = "172.17.0.5:5000"
        LOCATIONS_HOST = "locations:5000"
        resp = get("http://{}/orders/pending".format(LOCATIONS_HOST))
        new_orders = resp.json()
        resp = get("http://{}/orders/plated".format(LOCATIONS_HOST))
        prepping_orders = resp.json()
        resp = get("http://{}/orders/monitor".format(LOCATIONS_HOST))
        served_orders = resp.json()
        closed_orders = ["Not Implemented"]
        now = datetime.now()
        return render_template(
            'main_page.html',
            new_orders=new_orders,
            prepping_orders=prepping_orders,
            served_orders=served_orders,
            closed_orders=closed_orders,
            now=now)

    return app
