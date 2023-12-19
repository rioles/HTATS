from api.v1.endpoints import app_views
from flask_cors import cross_origin
from flask import abort, jsonify, make_response, request

from models.room import Room
from models.room_occupation import RoomOccupation

from services.occupation.occupation_adapter import OccupationAdapter
from services.occupation.occupation_port import OccupationPort
from services.paginator import Paginator


from flask_jwt_extended import  jwt_required


from services.room_service.room_category_manager.adapter.room_category_adapter import CreateCategoryRoom

@app_views.route('/occupation', methods=['POST'], strict_slashes=False)
@cross_origin()
def get_room_not_occupied():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '404', 'message': 'The request data is empty'}), 400)
    print(request.get_json())
    obj:OccupationPort = OccupationAdapter()
    room = obj.find_object_by_intervall(RoomOccupation,request.get_json()["start_date"], request.get_json()["end_date"], Room)
    page_obj = Paginator(room)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=10, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)


@app_views.route('/invoice', methods=['POST'], strict_slashes=False)
@cross_origin()
def post_invoice():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj:OccupationPort=OccupationAdapter()
      
    all_object = obj.add_object(
        **request.get_json())
    return make_response(jsonify(all_object), 201)

@app_views.route('/occupant', methods=['POST'], strict_slashes=False)
@cross_origin()
def post_room_occupant():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj:OccupationPort=OccupationAdapter()
      
    all_object = obj.add_object_occupant(
        **request.get_json())
    return make_response(jsonify(all_object), 201)

@app_views.route('/invoice_with_customer', methods=['GET'], strict_slashes=False)
@cross_origin()
@jwt_required()
def get_invoice_with_customer():
    obj:OccupationPort = OccupationAdapter()
    invoices = obj.find_all_ivoice_by_customer()
    page_obj = Paginator(invoices)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=10, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)



@app_views.route('/make_payment', methods=['POST'], strict_slashes=False)
@cross_origin()
def make_payment():
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj:OccupationPort = OccupationAdapter()
    invoices = obj.make_payment(**request.get_json())
    return make_response(jsonify(invoices), 201)


@app_views.route('/invoices', methods=['GET'], strict_slashes=False)
@cross_origin()
def get_invoice_by_customer():
    obj:OccupationPort = OccupationAdapter()
    invoices = obj.find_all_both_ivoice_by_customer()
    page_obj = Paginator(invoices)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=10, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)


@app_views.route('/room_and_occupation', methods=['POST'], strict_slashes=False)
@cross_origin()
def get_room_occupation_by_invoice():
    obj:OccupationPort = OccupationAdapter()
    room_occupation_adapter = obj.get_occupation_and_room_by_invoice(**request.get_json())
    return make_response(jsonify(room_occupation_adapter), 200)

@app_views.route('/room_and_occupants', methods=['POST'], strict_slashes=False)
@cross_origin()
def get_room():
    """create a new client"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
        
    room_ob: OccupationPort = OccupationAdapter()
    room_objects = room_ob.get_room_entity_data(**request.get_json())
    return make_response(jsonify(room_objects), 200)


@app_views.route('/update_room', methods=['POST'], strict_slashes=False)
@cross_origin()
def update_room():
    """create a new client"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
        
    room_ob: OccupationPort = OccupationAdapter()
    room_objects = room_ob.vacate_room(**request.get_json())
    return make_response(jsonify(room_objects), 200)

@app_views.route('/room_availlable', methods=['GET'], strict_slashes=False)
@cross_origin()
def room_availlable():
    """get all room availlable """
    room_ob: OccupationPort = OccupationAdapter()
    room_objects = room_ob.get_available_room()
    return make_response(jsonify(room_objects), 200)

