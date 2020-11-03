"""Package & module import."""
from online_store import db

# Set product quantity when adding to cart


def set_product_quantity(product, quant_added):
    """Set quantity and make adj. to title when out of stock."""
    if product.quantity > 0:
        product.quantity -= int(quant_added)
        return product.quantity
    return product.quantity


# Helper function for executing adding items to cart & totalling prices


def update_cart_subtotal(cart):
    """Update cart subtotal when new items are added."""
    product_total = 0

    for product in cart.products:
        product_total += product.price * product.quant_in_cart

    cart.subtotal = product_total
    db.session.commit()
    return cart.subtotal


def add_to_cart_helper(quantity, product, cart):
    """
    Increment product quantity in cart and append new prod to cart.

    Call set product quantity on product.
    """
    cart.products.append(product)
    cart.products_quantity += quantity
    product.quant_in_cart += quantity
    db.session.commit()

    set_product_quantity(product, quantity)
    update_cart_subtotal(cart)
    return cart, product


def clear_cart_helper(cart):
    """Clear cart on checkout or when empty cart button is pushed."""
    for product in cart.products:
        product.quant_in_cart = 0
    db.session.delete(cart)
    db.session.commit()
    return


def remove_from_cart_helper(cart, product):
    """Adjust quantities when item is removed from cart."""
    cart.products.pop(cart.products.index(product))
    product.quantity += product.quant_in_cart
    product.quant_in_cart = 0
    cart.products_quantity -= 1
    update_cart_subtotal(cart)
    return cart
