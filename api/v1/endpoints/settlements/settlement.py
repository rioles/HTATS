from api.v1.endpoints import app_views
from flask_cors import cross_origin
from flask import abort, jsonify, make_response, request
from services.settlement.settlement_port import SettlementPort
from services.settlement.settlement_adapter import SettlementAdapter
from flask_jwt_extended import  jwt_required
from services.paginator import Paginator

@app_views.route('/earn/<string:user_id>', methods=['GET'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def get_settlement_amount(user_id):
    data = {"user_id":user_id}
    obj:SettlementPort = SettlementAdapter()
    summ = obj.get_sum_with_intervall(**data)
    return make_response(jsonify(summ), 200)

@app_views.route('/sttlement_by_user', methods=['POST'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def get_list_settlement():
    """get list of settlement"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj:SettlementPort = SettlementAdapter()
    settlement_obj = obj.get_settlement_list_by_criteria(**request.get_json())

    return make_response(jsonify(settlement_obj), 200)

@app_views.route('/unpaid_invoice_customer', methods=['POST'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def get_unpaid_list_invoice():
    """get list of invoice"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)

    obj:SettlementPort = SettlementAdapter()
    invoice_object = obj.get_unpaid_invoice_list_by_criteria(**request.get_json())
    return make_response(jsonify(invoice_object), 200)



@app_views.route('/sttlements', methods=['POST'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def get_all_settlement():
    """get list of settlement"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)

    obj:SettlementPort = SettlementAdapter()
    settlement_obj = obj.get_all_settlement_list_by_criteria(**request.get_json())
    page_obj = Paginator(settlement_obj)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=100, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)



@app_views.route('/invoice_customer', methods=['POST'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def get_list_invoice():
    """get list of invoice"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)

    obj:SettlementPort = SettlementAdapter()
    invoice_object = obj.get_invoice_list_by_criteria(**request.get_json())
    page_obj = Paginator(invoice_object)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=100, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)