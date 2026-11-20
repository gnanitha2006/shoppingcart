
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Product
from .cart import get_cart


# Display all available products
def product_list(request):

    products = Product.objects.filter(
        is_available=True,
        stock__gt=0
    )

    return render(
        request,
        "shop/product_list.html",
        {"products": products}
    )


# Add product to cart
@require_POST
def cart_add(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    cart = request.session.get("shopping_cart", {})
    key = str(product.id)

    current_quantity = cart.get(key, 0)

    if current_quantity < product.stock:

        cart[key] = current_quantity + 1
        request.session["shopping_cart"] = cart

        messages.success(request, "Product added to cart!")

    else:

        messages.error(
            request,
            "Available stock limit reached."
        )

    return redirect("shop:product_list")


# Display cart
def cart_detail(request):

    items, total = get_cart(request)

    return render(
        request,
        "shop/cart_detail.html",
        {
            "items": items,
            "total": total,
        }
    )


# Update cart quantity
@require_POST
def cart_update(request, product_id):

    cart = request.session.get("shopping_cart", {})
    key = str(product_id)

    if key not in cart:
        return redirect("shop:cart_detail")

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        messages.error(request, "Invalid quantity.")
        return redirect("shop:cart_detail")

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    if quantity <= 0:

        cart.pop(key, None)
        messages.success(request, "Product removed.")

    elif quantity > product.stock:

        messages.error(
            request,
            f"Only {product.stock} items are available."
        )

    else:

        cart[key] = quantity
        messages.success(request, "Cart updated!")

    request.session["shopping_cart"] = cart

    return redirect("shop:cart_detail")


# Remove product from cart
@require_POST
def cart_remove(request, product_id):

    cart = request.session.get("shopping_cart", {})
    key = str(product_id)

    if key in cart:

        cart.pop(key)

        request.session["shopping_cart"] = cart

        messages.success(request, "Product removed successfully.")

    return redirect("shop:cart_detail")
