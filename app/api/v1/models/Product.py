"""Product Model and data storage functions"""
from datetime import datetime


class Product():
    """This class defines the Product model and
        the various methods of manipulating the product data"""

    product_id = 1
    product_quantity_store = 0
    productList = []

    def __init__(self, product_name, product_description, product_quantity,
       product_category, product_moq):
        """Initialise the Product model with constructor"""
        self.product_id = len(Product.productList) + 1
        self.product_name = product_name
        self.product_description = product_description
        self.product_quantity = product_quantity
        self.product_category = product_category
        self.product_moq = product_moq
        self.product_quantity_store = Product.product_quantity_store

        self.date_created = datetime.now()
        self.date_modified = datetime.now()

    def post_product(self):
        """Product Class method to add product to list"""
        product_item = dict(
            product_id=self.product_id,
            product_name=self.product_name,
            product_description=self.product_description,
            product_quantity=self.product_quantity,
            product_category=self.product_category,
            product_moq=self.product_moq,
            product_quantity_store=self.product_quantity_store,
            date_created=self.date_created,
            date_modified=self.date_modified
        )
        self.productList.append(product_item)
        return product_item

    def fetch_all_products(self):
        """Product Class method to fetch all products"""
        return Product.productList

    @staticmethod
    def fetch_single_product(productId):
        """Product Class method to fetch a single product by ID"""
        product_item = [prod for prod in Product.productList if prod['product_id'] == productId]
        if product_item:
            return product_item
        return 'not found'

    def put(self, productId):
        """Class method to Edit Product details"""
        product_item = [prod for prod in Product.productList if prod['product_id'] == productId]
        if product_item:
            product_item['product_name'] = self.product_name
            product_item['product_description'] = self.product_description
            product_item['product_quantity'] = self.product_quantity
            product_item['product_category'] = self.product_category
            product_item['product_moq'] = self.product_moq
            product_item['product_quantity_store'] += self.product_quantity_store
            product_item['date_modified'] = datetime.now()

            return product_item
        return 'not found'

    def delete(self, productId):
        """Class method to delete products from inventory"""

        purge_product = [prod for prod in Product.productList if prod['product_id'] == productId]
        if purge_product:
            Product.productList.remove(purge_product[0])
            return purge_product
        return 'not found'