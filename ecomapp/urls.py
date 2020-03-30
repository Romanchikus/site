from django.urls import path, re_path
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from ecomapp.views import *



urlpatterns = [
    path('', base_view, name='base'),
    re_path(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name = 'category_detail'),
    re_path(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name = 'product_detail'),
    re_path(r'^cart/$', cart_view, name = 'cart'),
    re_path(r'^add_to_cart/$', add_to_cart_view, name = 'add_to_cart'),
    re_path(r'^remove_from_cart/$', remove_from_cart, name = 'remove_from_cart'),
    re_path(r'^change_item_qty/$', change_item_qty, name = 'change_item_qty'),
    re_path(r'^checkout/$', checkout_view, name = 'checkout'),
    re_path(r'^order/$', order_create_view, name = 'create_order'),
    re_path(r'^make_order/$', make_order_view, name = 'make_order'),
    re_path(r'^thank_you/$', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
    re_path(r'^account/$', account_view, name = 'account'),
    re_path(r'^registration/$', registration_view, name = 'registration'),
    re_path(r'^login/$', login_view, name = 'login'),
    re_path(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('base')), name='logout'),
    re_path(r'^add_comment/$', add_comment, name = 'add_comment'),
    re_path(r'^chat_view/(?P<chat_id>[-\w]+)/$', changed_room, name = 'chat_view'),
    re_path(r'^send_message/$', send_message, name = 'send_message'),
    re_path(r'^chat_detail', chat_detail, name = 'chat_detail'),
    path('chat/', index, name='index'),
    path('chat/<str:room_name>/', room, name='room'),
    path('changed_index/', changed_index, name='changed_index'),
    path('changed_index/<str:room_name>/', changed_room, name='changed_room'),
    
]   