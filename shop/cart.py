from .models import Product


def get_cart(request):

    cart_data = request.session.get(
        "shopping_cart", {}
    )

    products = Product.objects.filter(
        id__in=cart_data.keys(),
        is_available=True
    )

    items = []
    total = 0

    for product in products:

        key = str(product.id)

        quantity = min(
            max(int(cart_data[key]), 0),
            product.stock
        )

        if quantity <= 0:
            continue

        line_total = product.price * quantity

        total += line_total

        items.append({
            "product": product,
            "quantity": quantity,
            "line_total": line_total,
        })

    return items, total