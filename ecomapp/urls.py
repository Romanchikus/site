from django.urls import path, re_path, include, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from ecomapp.views import *


urlpatterns = [
    path("", Base.as_view(), name="base"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("base")), name="logout"),
    path("signup/", registration_view, name="signup"),
    path("", include("django.contrib.auth.urls")),
    re_path(
        r"^category/(?P<category_slug>[-\w]+)/$",
        CategoryView.as_view(),
        name="category_detail",
    ),
    re_path(
        r"^product/(?P<slug>[-\w]+)/$", ProductView.as_view(), name="product_detail"
    ),
    re_path(r"^cart/$", CartView.as_view(), name="cart"),
    re_path(r"^add_to_cart/$", add_to_cart_view, name="add_to_cart"),
    re_path(r"^remove_from_cart/$", remove_from_cart, name="remove_from_cart"),
    re_path(r"^change_item_qty/$", change_item_qty, name="change_item_qty"),
    re_path(r"^checkout/$", checkout_view, name="checkout"),
    re_path(r"^order/$", order_create_view, name="create_order"),
    re_path(r"^make_order/$", make_order_view, name="make_order"),
    re_path(
        r"^thank_you/$",
        TemplateView.as_view(template_name="thank_you.html"),
        name="thank_you",
    ),
    re_path(r"^account/$", account_view, name="account"),
    re_path(r"^add_comment/$", add_comment, name="add_comment"),
    re_path(r"^chat_view/(?P<chat_id>[-\w]+)/$", Room.as_view(), name="chat_view"),
    re_path(r"^chat_detail", chat_detail, name="chat_detail"),
    path("update_order/", AddOrder.as_view(), name="update_order"),
    path("add_order/", add_order, name="add_order"),
]
