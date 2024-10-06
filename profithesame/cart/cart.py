from decimal import Decimal

from django.conf import settings
from django.http import HttpRequest

from shop.models import Product


class Cart:
    def __init__(self, request:HttpRequest) -> None:
        """
        Initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in th session
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart

    def add(self,
            product:Product,
            quantity:int=1,
            override_quantity:bool=False) -> None:
        """
        Add a product to the cart or update its quantity. 
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        
    def save(self) -> None:
        self.session.modified = True

    def remove(self, product:Product) -> None:
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self) -> dict:
        """
        Iterate over the items in the cart and get the products 
        from the database.
        """
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self) -> int:
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        return sum(Decimal(item['price']) * item['quantity']
            for item in self.cart.values())

    def clear(self) -> None:
        del self.session[settings.CART_SESSION_ID]
        self.save()
        