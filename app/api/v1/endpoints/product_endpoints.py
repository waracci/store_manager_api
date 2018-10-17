"""Product endpoints get and post methods"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify
from ..models.Product import Product

api = Namespace('Product_endpoints',
                description='A collection of endpoints for the product model; includes get and post endpoints')

parser = reqparse.RequestParser()
parser.add_argument('product_name')
parser.add_argument('product_description')
parser.add_argument('product_quantity')
parser.add_argument('product_category')
parser.add_argument('product_moq')


@api.route('')
class ProductEndpoint(Resource):
    """Contains all the endpoints for Product Model"""

    docStr = "Endpoint to post a Product"

    @api.doc(docStr)
    def post(self):
        """add product"""
        args = parser.parse_args()
        name = args['product_name']
        description = args['product_description']
        quantity = args['product_quantity']
        category = args['product_category']
        moq = args['product_moq']

        new_product = Product(name, description, quantity, category, moq)
        posted_product = new_product.post_product()
        return make_response(jsonify({'status': 'ok',
                                      'message': 'success',
                                      'product': posted_product}), 201)

    def get(self):
        """Retrieve all products"""
        products = Product.fetch_all_products(self)
        return make_response(jsonify({'message': 'success',
                                      'status': 'ok',
                                      'product': products}), 200)


@api.route('/<int:productId>')
class GetSingleQuestion(Resource):
    """Get a single Product record"""
    def get(self, productId):
        """Retrieve a single product"""
        single_product = Product.fetch_single_product(productId)
        if single_product == 'not found':
            return make_response(jsonify({'message': 'not found',
                                          'status': 'ok'}), 404)
        return make_response(jsonify({'message': 'success',
                                      'status': 'ok',
                                      'product': single_product}), 200)
