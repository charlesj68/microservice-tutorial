"""Support the Order API."""
from bson.objectid import ObjectId
from datetime import datetime
from flask import (
    Blueprint,
    jsonify,
    make_response,
    request)
from json import dumps
from pymongo import MongoClient
import excepts

# Constants

DB_NAME = 'mongodb'
DB_USER = 'root'
DB_PASSWD = 'example'

# Endpoints returning lists
# /orders/open GET - Return IDs of all active orders
# /orders/pending GET - Return IDs of all orders ready for prep
# /orders/plated GET - Return IDs of all orders ready for serving
# /orders/monitor GET - Return IDs of all orders served and awaiting checkout

# Endpoints returning full order details
# /orders/<id> GET - Return details of a specific order

# Endpoints for data creation or update
# /orders POST - Create a new order
# /orders/<id>/state/<state> PUT - Transition an order to a new state


# Minimum data format for orders
# {
#   "createTime": Time of order creation,
#   "startTime": Time of entry into kitchen,
#   "serveTime": Time of exit from kitchen,
#   "checkoutTime": Time of payment made,
#   "status": One of "new", "preparing", "served", "closed",
#   "items": [
#       {
#           "name": Menu item name,
#           "quantity": Number ordered
#       }
#   ]
# }

def get_order_db():
    """Obtain the order_db table from Mongo."""
    client = MongoClient(
        DB_NAME,
        username=DB_USER,
        password=DB_PASSWD)
    return client.order_db


def find_all_order_ids_by(test):
    """Return list of order _id's based on specified test."""
    order_set = get_order_db().all_orders
    cursor = order_set.find(test)
    return [str(item['_id']) for item in cursor]


def find_one_order_detail_by(test):
    """Return full order detail based on specified test."""
    order_set = get_order_db().all_orders
    return order_set.find_one(test)


api = Blueprint('orders', __name__, url_prefix='/orders')


@api.route('/', methods=['POST'])
def orders_detail_post():
    """Create new order in database."""
    jsonData = request.get_json()
    orderdoc = {
        "createTime": datetime.now(),
        "status": "new",
        "items": jsonData}
    order_collection = get_order_db().all_orders
    order_id = order_collection.insert_one(orderdoc).inserted_id
    return make_response(jsonify(id=str(order_id)), 201)


@api.route('/<id>', methods=['GET'])
def orders_detail_get(id):
    """Get detailed order info for given _id."""
    return dumps(
        find_one_order_detail_by({"_id": ObjectId(id)}),
        default=str)


@api.route('/<id>/status/<new_status>', methods=['PUT'])
def orders_move_status_put(id, new_status):
    """Change the status of an order, and register when it happens."""
    # Since we're implementing a tiny state engine, let us make sure that
    # requested transitions are valid. This dict maps current statuses to
    # a list of valid target statuses.
    valid_transitions = {
        "new": ["preparing"],
        "preparing": ["served"],
        "served": ["closed"]}

    # Within our database we're marking the times that the status transitions
    # take place. The names of the database fields are tied to, but differ from
    # the names of the statuses being transitioned. This dict maps the target
    # status to the database field that records that status-entry-time
    target_time_field = {
        "preparing": "startTime",
        "served": "serveTime",
        "closed": "checkoutTime"
    }

    # Get the current order document from the database
    order_set = get_order_db().all_orders
    order_doc = find_one_order_detail_by({"_id": ObjectId(id)})

    # If the requested new status is already the current value, just return.
    if order_doc["status"] == new_status:
        return make_response("0", 204)

    # Check that the transition is valid, and raise a 409 if it is not
    if new_status not in valid_transitions[order_doc["status"]]:
        raise excepts.ErrorStatus(
            'Invalid status transition from {} to {}'.format(
                order_doc["status"], new_status),
            status_code=409)

    # Update the document we obtained from the database with the new status
    # value, and the appropriate transition time stamp
    field_name = target_time_field[new_status]
    order_doc["status"] = new_status
    order_doc[field_name] = datetime.now()

    # Replace the document in the database with the modified document
    res = order_set.replace_one({"_id": ObjectId(id)}, order_doc)
    if res.matched_count != 1:
        raise excepts.ErrorStatus(
            'Database update failed to apply',
            status_code=400
        )

    return make_response(jsonify(res.matched_count), 204)


@api.route('/open', methods=['GET'])
def orders_open():
    """Get list of orders not yet closed."""
    return dumps(find_all_order_ids_by({"status": {"$ne": "closed"}}))


@api.route('/pending', methods=['GET'])
def orders_pending():
    """Get list of orders not yet preparing."""
    return dumps(find_all_order_ids_by({"status": {"$eq": "new"}}))


@api.route('/plated', methods=['GET'])
def orders_plated():
    """Get list of orders not yet served."""
    return dumps(find_all_order_ids_by({"status": {"$eq": "preparing"}}))


@api.route('/monitor', methods=['GET'])
def orders_monitor():
    """Get list of orders not yet paid."""
    return dumps(find_all_order_ids_by({"status": {"$eq": "served"}}))
