#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.endpoints.room.create_category import *
from api.v1.endpoints.room.creat_room import *
from api.v1.endpoints.client.category_client import *
from api.v1.endpoints.room.create_room_item import *
from api.v1.endpoints.client.clients import *
from api.v1.endpoints.user.user import *
from api.v1.endpoints.occupation.occupation import *



