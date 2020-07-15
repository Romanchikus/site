from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse
from decimal import Decimal
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length =110)
    slug = models.SlugField(blank=True)
    objects = models.Manager()  

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category_detail', kwargs= {'category_slug': self.slug})

def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(instance.name)
        instance.slug = slug

pre_save.connect(pre_save_category_slug, sender=Category)



# class Brand(models.Model):
#    name = models.CharField(max_length =110)


#    def __str__(self):
#       return self.name

def image_folder(instance, filename):
    filename = instance.slug +'.'+ filename.split('.')[1]
    return '{}/{}'.format(instance.slug, filename)

class ProductManager(models.Manager):

    def all(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().filter(availeble=True)

class Comment(models.Model):
    objects = models.Manager()
    slug = models.SlugField()
    author = models.CharField(max_length= 120)
    comments = models.TextField()

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    # brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    title = models.CharField(max_length= 120)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to = image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    availeble = models.BooleanField(default=True)
    comment = models.ManyToManyField(Comment,  blank = True)
    objects = ProductManager()

    def add_comment(self,comment,author, slug):
        product = self
        
        if not Comment.objects.filter(author=author, slug = slug).exists():
            new_item, _ = Comment.objects.get_or_create(comments=comment, author=author, slug=slug )
            product.comment.add(new_item)
            product.save()
            print('save comment))')

    def __str__(self):
        return self.title   
    def get_absolute_url(self):
        return reverse('product_detail', kwargs= {'slug': self.slug})





class Image(models.Model):
    slug = models.SlugField()
    image = models.ImageField(upload_to = image_folder)
    product = models.ForeignKey(Product, default=None, related_name='images',on_delete=models.PROTECT)
        


class CartItem(models.Model):         
    objects = models.Manager()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    def __unicode__(self):
        return "Cart item for product {0}".format(self.product.title)



class Cart(models.Model):

    item  = models.ManyToManyField(CartItem, blank = True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default = 0.00)
    objects = models.Manager()
    def __unicode__(self):
        return str(self.id)
    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug = product_slug)
        new_item, _ = CartItem.objects.get_or_create(product = product, item_total=product.price)
        if new_item not in cart.item.all():
            cart.item.add(new_item)
            cart.save()

        
    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug = product_slug)
        for cart_item in cart.item.all():
            if cart_item.product == product:
                cart.item.remove(cart_item)
                cart.save()
    def change_qty(self, qty, item_id, cart_item):
        cart = self
        # print(int(qty))
        cart_item.qty = int(qty)
        cart_item.item_total = int(cart_item.qty)*Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.item.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()


ORDER_STATUS_CHOICES = {
    ('Accepted for processing','Accepted for processing'),
    ('Performed', 'Performed'),
    ('Paid', 'Paid')
}
class Order(models.Model):

    item = models.ForeignKey(Cart, on_delete=models.PROTECT, default="")
    objects = models.Manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    address  = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    country = models.CharField(max_length=254)
    zipcode = models.CharField(max_length=10)
    card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=20)
    card_code = models.IntegerField()
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    NameonCard = models.CharField(max_length=100)
    CreditCardType = models.CharField(max_length=20)

    phone = models.CharField(max_length=20)
        
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    status = models.CharField(max_length=200, choices=ORDER_STATUS_CHOICES)
        

    def __unicode__(self):
        return "Order № {0}".format(str(self.id))

class Member(models.Model):
    objects = models.Manager()
    member = models.CharField(max_length=100, unique=True, null=True)
    admin = models.BooleanField(default=False)
    

class Messages(models.Model):
    # objects = models.Manager()
    member = models.CharField(max_length=100, null=True)
    message = models.TextField(verbose_name= ("Сообщение"),default='')
    pub_date = models.DateTimeField(verbose_name= ('Дата сообщения'), default=timezone.now)
    admin = models.BooleanField(default=False)

    


class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    messages = models.ManyToManyField(Messages)
    member = models.ForeignKey(Member, on_delete=models.PROTECT, default="")

        
    def send_message(self, member,message,admin=False):
        chat = self
        new_message = Messages.objects.create(message=message,member=member, admin=admin)
        chat.messages.add(new_message)
        chat.save()
        print('save mess')
        return new_message
        
    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('chat_view', kwargs= {'chat_id': str(self.id)})




    