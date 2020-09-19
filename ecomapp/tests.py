from django.test import TestCase, SimpleTestCase
from .models import *
from django.contrib.auth import get_user_model

class HomePageTests(TestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('base'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('base'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
    
class SignupPageTests(TestCase):

    username = 'newuser'
    email = 'newuser@email.com'

    def test_signup_page_status_code(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
                self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()
                [0].username, self.username)
        self.assertEqual(get_user_model().objects.all()
                [0].email, self.email)





# class PostModelTest(TestCase):

#     def setUp(self):

#         self.cart = Cart()


#         self.order = Order.objects.create(
#             user=request.user,
#             item=self.cart,
#             total=cart.cart_total,
#             first_name=name,
#             last_name=last_name,
#             phone=phone,
#             card_number=card_number,
#             expiry_date=expiry_date,
#             card_code=card_code,
#             address=address,
#             comments=comments,
#             country=country,
#             city=city,
#             zipcode=zipcode,
#             NameonCard=NameonCard
#             )

#     def test_text_content(self):
#         post=Post.objects.get(id=1)
#         expected_object_name = f'{post.text}'
#         self.assertEqual(expected_object_name, 'just a test')