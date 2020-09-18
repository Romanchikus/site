from django.shortcuts import render
from ecomapp.models import Category, Product, CartItem, Cart, Order, Comment, Messages, Chat, Member

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from decimal import Decimal
from ecomapp.forms import OrderForm, RegistrationForm, LoginForm, CommentForm
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import View, DetailView
import urllib.request
from .utils import *
from django.contrib.auth.views import LoginView




# forma = 'name ={},\n last_name ={}'.format(
#             'name1','last_name')
# forma = urllib.parse.quote(forma)
# urllib.request.urlopen('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(token,chat_id,forma))

class Base(Cart_and_chat_init ,View):
    
    template_name='base.html'
        

    def get(self, request):
        self.context = { 'products': Product.objects.all()}
        return self.get_base(request)

class CustomLoginView(LoginView):
    template_name = 'login.html'


def login_view(request):
   
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        username = get_object_or_404(User, username=username)
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form
    }
    return render(request, 'login.html', context) 

class ProductView(Cart_and_chat_init, View):
    template_name = "product.html"

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        images = product.images.all()
        if not images:
            images = False
        self.context={'product': product,
        'images':images,
        'form':CommentForm(request.POST or None)
        }
        return self.get_base(request) 


class CategoryView(Cart_and_chat_init, View):
    template_name = "category.html"

    def get(self, request, category_slug):
        category = get_object_or_404(Category,slug=category_slug)
        categories = Category.objects.all()
        products_of_category = Product.objects.filter(category=category)
        self.context = {
            'category': category,
            'products_of_category': products_of_category
        }
        return self.get_base(request)

class CartView(Cart_and_chat_init, View):
    template_name = "cart.html"
    def get(self, request):
        self.context = {}
        return self.get_base(request)

def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get("product_slug")
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.item.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total':  cart.item.count(),
                         "cart_total_price": cart.cart_total})


def remove_from_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get("product_slug")
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.item.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total':  cart.item.count(),
                         "cart_total_price": cart.cart_total})


def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart_item = CartItem.objects.get(id=int(item_id))
    cart.change_qty(qty, item_id, cart_item)
    return JsonResponse({'cart_total':  cart.item.count(),
                         'item_total': cart_item.item_total,
                         "cart_total_price": cart.cart_total})


def checkout_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'cart': cart
    }
    return render(request, 'checkout.html', context)


def order_create_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    categories = Category.objects.all()
    context = {
        'form': form,
        'cart': cart,
        'categories': categories
    }
    return render(request, 'order.html', context)


def make_order_view(request):
    __token = '875809845:AAHxB49VM_TowQhXtaBz80fx07XrIvgcHIc'
    __tl_chat_id = 406434091
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    categories = Category.objects.all()
    print(form.is_valid())
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        card_number = form.cleaned_data['card_number']
        expiry_date = form.cleaned_data['expiry_date']
        card_code = form.cleaned_data['card_code']
        address = form.cleaned_data['address']
        country = form.cleaned_data['country']
        city = form.cleaned_data['city']
        zipcode = form.cleaned_data['zipcode']
        NameonCard = form.cleaned_data['NameonCard']
        comments = form.cleaned_data['comments']

        forma = 'name ={}\n last_name ={}\n phone={}\ncard_number={}\nexpiry_date={}\ncard_code={}\naddress={}\ncountry={}\ncity={}\nzipcode={}\nNameonCard={}\ncomments={}\ncart_total={}\n'.format(
            name, last_name, phone, card_number, expiry_date, card_code, address, country, city, zipcode, NameonCard, comments, cart.cart_total)
        forma = urllib.parse.quote(forma)
        # urllib.request.urlopen(
        #     'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(__token, __tl_chat_id, forma))

        new_order = Order.objects.create(
            user=request.user,
            item=cart,
            total=cart.cart_total,
            first_name=name,
            last_name=last_name,
            phone=phone,
            card_number=card_number,
            expiry_date=expiry_date,
            card_code=card_code,
            address=address,
            comments=comments,
            country=country,
            city=city,
            zipcode=zipcode,
            NameonCard=NameonCard
        )
        del request.session['cart_id']
        del request.session['total']
        return HttpResponseRedirect(reverse('thank_you'))
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'order.html', context)


def account_view(request):
    order = Order.objects.filter(user=request.user).order_by('-id')
    context = {
        'order': order
    }
    return render(request, 'account.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'registration.html', context)





def add_comment(request):

    product_slug = request.GET.get("product_slug")
    comment = request.GET.get("txt")

    product = Product.objects.get(slug=product_slug)
    if comment:
        user_id = request.session.session_key
        product.add_comment(comment, user_id, product_slug)

    else:
        print('form.is_INvalid')

    return JsonResponse({'auth_id': str(user_id),
                         'last_comm': str(comment)})


def chat_detail(request):
    if not request.session.session_key: request.session.save()
    if request.user.is_superuser:
        chats = Chat.objects.all()
        context = {'chats':  chats.order_by('-id')}
        # print(dir(request.session.update('123')))
        # print(dir(request.session.session_key))        
        return render(request, "chat_detail.html", context)
    else:
        return HttpResponseRedirect(reverse('base'))

class Room(Cart_and_chat_init, View):
    template_name = 'changed_room.html'
    
    def get(self, request, chat_id):
        self.context={}

        if request.user.is_superuser:
            self.chat_id = chat_id
            return self.get_base(request)
        else:
            return HttpResponseRedirect(reverse('base'))

def changed_room(request, chat_id):
    if not request.session.session_key:
        request.session.save()
    if request.user.is_superuser:
        chat = Chat.objects.get(id=chat_id)
        member = Member.objects.get(chat=chat)
    else:
        member_id = request.session.session_key
        print('-changed_room-member_id-----', member_id)
        try:
            member = Member.objects.get(member=member_id)
            chat = Chat.objects.get(member=member)
        except:
            member = Member(member=member_id)
            member.save()
            chat = Chat(member=member)
            chat.save()
    chat_id = chat.id
    print('chat_id =', chat_id)
    messages = messages_to_list(get_last_10_messages(chat_id))
    exist_mess = Messages.objects.filter(member=member).exists()
    context = {'chat':  messages,
               'room_name': chat_id,
               'exist_mess': exist_mess}
    return render(request, 'changed_room.html', context)


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-pub_date').all()[:10]

def messages_to_list(messages):
        result = []
        for message in messages:
            result.append(message_to_list(message))
        result.reverse()
        return result

def message_to_list(message):
        return {
        'member': str(message.member),  
        'message': str(message.message),
        'pub_date': str(message.pub_date.strftime(" %B %d,%Y, %A %I:%M%p ")),
        'admin': message.admin
        }
