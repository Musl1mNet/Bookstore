from django.urls import path

from order.views import cart_inc, cart_dec, CheckoutView

app_name = "order"

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("cart-inc/<int:id>/", cart_inc, name="inc"),
    path("cart-dec/<int:id>/", cart_dec, name="dec"),
]