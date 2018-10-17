"""Sales Endpoints get and post methods"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify

from ..models.Sales import Sales

api = Namespace('Sales endpoints',
                description='A collection of endpoints for the Sales model')

parser = reqparse.RequestParser()
parser.add_argument('made_by')
parser.add_argument('cart')
parser.add_argument('cart_price')


@api.route('')
class SalesEndpoint(Resource):
    """Contains all the endpoints for Sales Model"""

    docstr = "Endpoint to post a sale"

    @api.doc(docstr)
    def post(self):
        """Make a Sale"""
        args = parser.parse_args()
        made_by = args['made_by']
        cart = args['cart']
        cart_price = ['cart_price']

        new_sale = Sales(made_by, cart, cart_price)
        posted_sale = new_sale.post_sales()

        return make_response(jsonify({'status': 'ok',
                                      'message': 'success',
                                      'sales': posted_sale}), 201)

    def get(self):
        """Retrieve all sales"""
        sales = Sales.fetch_all_sales(self)
        return make_response(jsonify({'status': 'ok',
                                      'message': 'success',
                                      'sales': sales}), 200)

@api.route('/<int:saleId>')
class GetSingleSale(Resource):
    """Gets a single sale record"""
    def get(self, saleId):
        single_sale = Sales.fetch_single_sale(saleId)
        if single_sale == 'not found':
            return make_response(jsonify({'message': 'not found',
                                            'status': 'ok'}), 404)
        return make_response(jsonify({'message': 'success',
                                        'status': 'ok',
                                        'product': single_sale}), 200)

        