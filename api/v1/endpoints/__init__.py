#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.endpoints.room.create_category import *
from api.v1.endpoints.room.creat_room import *



