from ecomapp.models import Category, Product, CartItem, Cart, Order, Comment, Messages, Chat, Member
from django.shortcuts import render



class Cart_and_chat_init:

    chat_id = False
    def get_base(self,request):

        chat, chat_id, exist_mess = self.chat(request)
        categories = Category.objects.all()

        self.context = {**self.context,
        'categories': categories,
        'cart': self.cart(request),
        'chat':  chat,
        'room_name': chat_id,
        'exist_mess': exist_mess
        }
        return self.render(request)

        
    def render(self, request):
        return render(request, self.template_name, self.context)

    def chat(self, request):
        if not request.session.session_key:
            request.session.save()
        member_id = request.session.session_key
        member, _ = Member.objects.get_or_create(member=member_id)
        member.save()
        try:
            if self.chat_id and request.user.is_superuser:
                chat = Chat.objects.get(id=self.chat_id)
                member = Member.objects.get(chat=chat)
            else:
                chat, _ = Chat.objects.get_or_create(member=member)
        except:
            member = Member(member=member_id)
            member.save()
            chat = Chat(member=member)
            chat.save()
        return chat.messages.order_by('-pub_date').all()[:10], chat.id, Messages.objects.filter(member=member).exists()
    
    def cart(self, request):
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
        return cart






