"""Sale Model and Data storage functions"""
from datetime import datetime

from Product import Product


class Sales():
    """This class defines the Sales Model and
        the various methods of manipulating the Sales data"""

    sale_id = 1
    salesList = []

    def __init__(self, made_by, **kwargs):
        """Initialize the Sales Model with constructor"""

        self.id = len(Sales.salesList) + 1
        self.cart = []
        # for product_item in kwargs.items():
        #     found_product = Product.fetch_single_product(int(product_item[0][-1]))
        #     if found_product == 'not found':
        #         print('not found')
        #     else:
        #         if  product_item[1] > found_product[0]['product_quantity']:
        #             print('not found')
        #         else:
        #             # self.cart.append(found_product)
        #             print('one success')
        # # print(self.cart)
        self.made_by = made_by
        self.cart_price = 0
        self.date_created = datetime.now()
        self.date_modified = datetime.now()

    def post_sales(self):
        """Sale method to make a sale record"""

        # Check for product availability in inventory
        # Check for product quantity
        # Deduct product quantity
        # retrieve product details
        # record sale
        sale_item = dict(
            id=self.id,
            made_by=self.made_by,
            cart=self.cart,
            date_created=self.date_created,
            date_modified=self.date_modified
        )
        Sales.salesList.append(sale_item)
        return sale_item

    def fetch_all_sales(self):
        """Sale method to fetch all sales"""
        return Sales.salesList

    def fetch_single_sale(self, saleId):
        """Sale method to fetch a single sale record"""
        sale_record = [sale for sale in Sales.salesList if sale['sale_id'] == saleId]
        if sale_record:
            return sale_record
        return 'not found'

# new_product = Product('omo', 'grest', 200, 'soap', 200)
# new_product1 = Product('shark', 'grest', 200, 'fish', 200)
# new_product2 = Product('volvo', 'grest', 200, 'car', 200)
# new_product.post_product()
# new_product1.post_product()
# new_product2.post_product()

# new_sale = Sales('Warachi', id1=23, id2=30, id3=2)
# print(new_sale.made_by)