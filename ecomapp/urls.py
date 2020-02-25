from django.urls import path, re_path
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from ecomapp.views import (base_view,
    category_view,
    product_view,
    cart_view,
    add_to_cart_view,
    remove_from_cart,
    change_item_qty,
    checkout_view,
    order_create_view,
     make_order_view,
     account_view,
     registration_view,
     login_view,
     add_comment,
     chat_view,
     send_message,
     chat_detail,
    )



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
    re_path(r'^chat_view/(?P<chat_id>[-\w]+)/$', chat_view, name = 'chat_view'),
    re_path(r'^send_message/$', send_message, name = 'send_message'),
    re_path(r'^chat_detail', chat_detail, name = 'chat_detail'),

    
    # re_path(r'^dialogs/$', login_required(views.DialogsView.as_view()), name='dialogs'),
    # re_path(r'^dialogs/create/(?P<user_id>\d+)/$', login_required(views.CreateDialogView.as_view()), name='create_dialog'),
    # re_path(r'^dialogs/(?P<chat_id>\d+)/$', login_required(views.MessagesView.as_view()), name='messages'),
    # # re_path(r'^order_make/$', make_order_card, name = 'make_order_card'),
    
]   
# <br>
    
# <table class="table table-striped dedd" >
#         <thead>
#                 <tr>
#     <th scope="col">
#         User
#     </th>
#     <th scope="col">
#         Message
#     </th>
# </tr>
# </thead>
# {% for mes in chat.messages.all %}
# <tr>
#     {{% if not mes.admin %}}
#     <td><strong class="comment-title"> {{ mes.member }} </strong></td>
#     <td>  <strong class='comment-same'> {{ mes.message }}</strong></td>
# </tr> <tr>
#     <td>  <strong class='comment-same'> {{ mes.pub_date }}</strong></td>
#     <td></td>
#     {{% else %}}
#     <td><strong class="comment-title"> {{ mes.member }} </strong>
#         <img src="/media/108-128.png" class="" id="s4-icon" data-ccw="style-4" alt="true">
#     </td>
#     <td>  <strong class='comment-same'> {{ mes.message }}</strong></td>
# </tr> <tr>
#     <td>  <strong class='comment-same'> {{ mes.pub_date }}</strong></td>
    
#     {{% endif %}}
        
# </tr>   
# {% endfor %}
# <div >
    
# </div>
# </table>


   

# <script src='{% static "js/jquery.js" %}'></script>
# <script>
# $(document).ready(function(){
#     $('.send_message').on("click", function(e){
#         e.preventDefault()
#         var message = $('#message').val();    
#         data = {
#             message: message
#         }
        
#         $.ajax({
#             type: "GET",
#             url: '{% url "send_message" %}',
#             data: data,

#             success: function(data){
#                 // location.reload();
#                 $('.dedd').append(
#                     '<tr ><td><strong class="comment-title">'
#                     + data.member+' </strong> <img src="'
#                     + data.img+'" class="" id="s4-icon" data-ccw="style-4" alt=""></td><td>  <strong class="comment-same">'
#                     + data.message+'</strong></td></tr> <tr><td>  <strong class="comment-same">'
#                     + data.pub_date+' {{ mes.pub_date }}</strong></td></tr>'
#                 )

#             }
            
#         })
        

#     })
# })
# </script>