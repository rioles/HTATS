from api.v1.endpoints import app_views
from flask_cors import cross_origin
from flask import abort, jsonify, make_response, request
from services.settlement.settlement_port import SettlementPort
from services.settlement.settlement_adapter import SettlementAdapter
from flask_jwt_extended import  jwt_required

@app_views.route('/earn', methods=['GET'], strict_slashes=False)
@cross_origin()
#@jwt_required()
def get_invoice_with_customer():
    if not request.get_json():
        return make_response(jsonify(
            {'status': '404', 'message': 'The request data is empty'}), 400)
    print(request.get_json())
    obj:SettlementPort = SettlementAdapter()
    summ = obj.get_sum_with_intervall(**request.get_json())
    return make_response(jsonify(summ), 200)