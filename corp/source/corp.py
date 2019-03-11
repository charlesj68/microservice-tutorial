"""Provide microservice for Corp. database."""
from flask import Flask, Blueprint, jsonify
from MySQLdb import connect
from MySQLdb.cursors import DictCursor
from os import environ

# **********
# Database Constants
#
# If you are running the Corp service outside a Docker container, then you
# can pass in the IP address of the MySQL container in the DB_HOST environment
# variable.
if "DB_HOST" in environ:
    DB_HOST = environ["DB_HOST"]
else:
    # This value is the name of the MySQL container as defined in the Ansible
    # playbook.
    DB_HOST = "mysqldb"

DB_USER = "a_user"
DB_PASSWD = "a_password"  # No, we should not have password here in real life!
DB_NAME = "CorpDb"
DB_PORT = 3306

# **********
# SQL Statements
#
# SQL statements can get complicated and thus benefit from good indentation
# and formatting. I like to separate them into their own section with
# triple-quoted strings. In a real project they might even be in another file
# all-together.

SQL_GET_MENUS = """
    SELECT item_name
        FROM menu"""


# **********
# Helper functions
#
# Though not particuarlly helpful in this case, frequently repeated blocks of
# code should live in their own functions. Within a REST API the action of
# obtaining a connection to the database is just such a repeated block.

def connect_db():
    """Create and return MySQLdb connection."""
    return connect(
        user=DB_USER,
        passwd=DB_PASSWD,
        db=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        cursorclass=DictCursor)


# **********
# Blueprints
#
# Using Flask Blueprints you can group related API endpoints together. In our
# tutorial this isn't required, but it's a powerful tool for making API
# handlers that can grow. To learn more, see:
# http://flask.pocoo.org/docs/1.0/blueprints/#blueprints

menus_api = Blueprint('menus', __name__, url_prefix='/menus')

# This is our lone endpoint. It will return a simple list of all the menu item
# names in the database and it will be invoked as a GET request to
# http://FLASKHOST:PORT/menus/
@menus_api.route('/', methods=['GET'])
def menus():
    """Return a list of all active menu item names."""
    cursor = connect_db().cursor()
    cursor.execute(SQL_GET_MENUS)
    return jsonify(cursor.fetchall())


# **********
# Flask App
#
# The last detail, we need to provide a create_app factory function to
# instantiate and return the Flask app.
def create_app():
    """Create and return the Flask app."""
    app = Flask("corp")
    app.register_blueprint(menus_api)
    return app
