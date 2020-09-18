from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from ecomapp.Card import CreditCardField, ExpiryDateField, VerificationValueField
from ecomapp.models import Order, Messages


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Username'
		self.fields['password'].label = 'Password'
	
	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		if not User.objects.filter(username=username).exists():
			raise forms.ValidationError('User with this login not exist!')
		user = User.objects.get(username=username)
		if user and not user.check_password(password):
			raise forms.ValidationError('Password not right!')



class RegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password_check = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'password_check',
			'first_name',
			'last_name',
			'email'
		]
	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Username'
		self.fields['password'].label = 'Password'
		self.fields['password'].help_text = 'Create a password'
		self.fields['password_check'].label = 'Retype password'
		self.fields['first_name'].label = 'Name'
		self.fields['last_name'].label = 'Last Name'
		self.fields['email'].label = 'Your mail'
		self.fields['email'].help_text = 'Please provide a real address'


	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']
		email = self.cleaned_data['email']
		if User.objects.filter (username = username) .exists ():
			raise forms.ValidationError ('A user with this login is already registered in the system!')
		if User.objects.filter (email = email) .exists ():
			raise forms.ValidationError ('A user with this mailing address is already registered!')
		if password  != password_check:
			raise forms.ValidationError ('Your passwords do not match! Try again!')


class OrderForm(forms.Form):

	name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	phone = forms.CharField()
	date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
	# card_number = CreditCardField(placeholder=u'0000 0000 0000 0000', min_length=12, max_length=19)
	card_number = forms.CharField()
	expiry_date = ExpiryDateField(required=True)
	card_code = VerificationValueField()
	address = forms.CharField(required=True)
	comments = forms.CharField(widget=forms.Textarea, required=False)
	city = forms.CharField(required=True)
	country = forms.CharField(required=True)
	zipcode = forms.CharField(required=True)
	NameonCard = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Name Surname'}))
	# expiry_date.widget.attrs.update({'id_expiry_date_0' : 'your_id'})


	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields['expiry_date'].label = 'Expiries end'
		self.fields['expiry_date'].widget.attrs['class'] = 'btn  dropdown-toggle dropdown-toggle-split center'

		self.fields['card_code'].label = 'CVV'
		# self.fields['name'].widget.attrs.update({'div' : 'label'})
		# self.fields['last_name'].widget.attrs.update({'div' : 'label'})
		self.fields ['name']. label = 'Name'
		self.fields ['last_name']. label = 'Last Name'
		self.fields ['phone']. label = 'Contact phone'
		self.fields ['phone']. help_text = 'Please indicate the real phone number by which you can be contacted'
		self.fields ['address']. label = 'Delivery address'
		self.fields ['address']. help_text = '* Be sure to include the city!'
		self.fields ['comments']. label = 'Order Comments'
		self.fields ['date']. label = 'Delivery Date'
		self.fields ['card_number']. label = 'Card number'
		self.fields ['date']. help_text = 'Delivery is made on the next day after placing the order. The manager will contact you first! '


class CommentForm(forms.Form):

	comment = forms.CharField(required=True, min_length=12)
	

	def __init__(self, *args, **kwargs):
		super(CommentForm, self).__init__(*args, **kwargs)

		# self.fields['name'].widget.attrs.update({'div' : 'label'})
		# self.fields['last_name'].widget.attrs.update({'div' : 'label'})
		self.fields['comment'].label = 'Your comment'

class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['message']
        labels = {'message': ""}


	
