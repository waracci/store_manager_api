"""Sales Endpoints get and post methods"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify

from ..models.Sales import Sales

api = Namespace('Sales endpoints')