"""reference this array to display categories to the users, and the forms"""
PRODUCT_CATEGORIES = (
    ('books', 'Books'),
    ('kitchen_appliances', 'Kitchen Appliances')
)

"""reference this to implement user types"""
USER_TYPES = (
    ('buyer', 'Buyer'),
    ('merchant', 'Merchant')
)

DEFAULT_USER_TYPE = 'buyer'

"""reference this to implement payment options"""
PAYMENT_METHOD = (
    ('cash_on_delivery', 'Cash on Delivery'),
    ('bank', 'Bank'),
    ('card', 'Card')
)

DEFAULT_PAYMENT_METHOD = 'cash_on_delivery'
