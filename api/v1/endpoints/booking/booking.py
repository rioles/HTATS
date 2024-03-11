from api.v1.endpoints import app_views
from flask_cors import cross_origin
from flask import abort, jsonify, make_response, request

from models.room import Room
from models.room_occupation import RoomOccupation
from services.booking.reservation import Booking, BookingService

from services.occupation.occupation_adapter import OccupationAdapter
from services.occupation.occupation_port import OccupationPort
from services.paginator import Paginator


from flask_jwt_extended import  jwt_required


from services.room_service.room_category_manager.adapter.room_category_adapter import CreateCategoryRoom

@app_views.route('/booking', methods=['POST'], strict_slashes=False)
#@jwt_required
@cross_origin()
def get_room_to_reserved():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '404', 'message': 'The request data is empty'}), 400)
    print(request.get_json())
    obj = BookingService()
    room = obj.all_available_room(**request.get_json())
    page_obj = Paginator(room)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=100, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)

@app_views.route('/reserved', methods=['POST'], strict_slashes=False)
#@jwt_required
@cross_origin()
def add_booking():
    """get list of invoice"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj:BookingService = BookingService()
    booking_object = obj.add_object(**request.get_json())
    return make_response(jsonify(booking_object), 200)

@app_views.route('/confirmed', methods=['PUT'], strict_slashes=False)
#@jwt_required
@cross_origin()
def confirmed_booking():
    """get list of invoice"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)

    obj:BookingService = BookingService()
    obj = obj.confirmed_booking(**request.get_json())
    if obj is not None:
        return make_response(jsonify(obj), 200)
    else:
        return make_response(jsonify({"message":"une erreur s'est produit lors du modification", "status":404}), 404)
        
        
    

@app_views.route('/room_booked', methods=['GET'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def get_reserved_room():
    """create a new category"""
    obj = BookingService()
    room = obj.list_booking()
    page_obj = Paginator(room)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=100, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)


@app_views.route('/canceled_booking', methods=['PUT'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def canceled_booking():
    """canceled booking"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)

    obj:BookingService = BookingService()
    obj.canceled_booking(**request.get_json())
    return make_response(jsonify({"message":"update made successfully", "status":200}), 200)

@app_views.route('/confirmed_booking', methods=['GET'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def all_booking_confirmed():
    """create a new category"""
    obj = BookingService()
    room = obj.get_all_confirm_booking()
    page_obj = Paginator(room)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=100, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)
       

@app_views.route('/booking_by_room', methods=['POST'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def booking_by_room():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj = BookingService()
    booking = obj.get_booking_by_room_and_date(**request.get_json())
    return make_response(jsonify(booking), 200)

