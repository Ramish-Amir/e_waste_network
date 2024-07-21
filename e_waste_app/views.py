from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import FormView
from .forms import PasswordResetConfirmForm, ProfileForm
from .forms import LoginForm, RegisterForm, PasswordResetForm
from django.utils import timezone
from django.contrib import messages
from .forms import ContactForm
from .models import Product, Member, RecycleItem
from django.db.models import Q
from django.shortcuts import render, redirect
from .recycleForms import AddRecycleItemForm, SearchRecycleItemsForm

# Create your views here.


def profile(request):
    user = request.user
    member = get_object_or_404(Member, username=user.username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=member)  # Bind the form with the existing instance
        if form.is_valid():
            form.save()  # Update the existing instance
            return redirect('e_waste_app:home')
        else:
            print("Form errors:", form.errors)
            return render(request, 'e_waste_app/profile.html', {'form': form})
    else:
        form = ProfileForm(instance=member)  # Initialize form with the existing instance
    return render(request, 'e_waste_app/profile.html', {'form': form})


def user_register(request):
    print(request)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user_password = form.cleaned_data.get('password')
            user_confirm_password = form.cleaned_data.get('confirm_password')

            if User.objects.filter(username=username).exists():
                print('Username already taken')
                messages.error(request, 'Username already taken')
                return render(request, 'e_waste_app/Register.html', {'form': form})
            if user_password != user_confirm_password:
                messages.error(request, 'Passwords do not match')
                print('Password dont match', user_password, user_confirm_password)
                return render(request, 'e_waste_app/Register.html', {'form': form})

            member = Member.objects.create_user(username=username, email=email, password=user_password)
            member.save()
            messages.success(request, f'account created for {username}')
            return redirect('e_waste_app:login')

        else:
            form = RegisterForm()
            print("invalid input")
            return render(request, 'e_waste_app/Register.html', {'form': form})

    else:
        print("this is get req")
        form = RegisterForm()
        return render(request, 'e_waste_app/Register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print("user authenticated", user)
            if user:
                print("user activated?", user)
                if user.is_active:
                    login(request, user)
                    current_login = timezone.now().strftime("%d/%m/%Y %H:%M:%S")
                    request.session['last_login'] = current_login
                    request.session.set_expiry(60 * 60)
                    messages.success(request, 'Login successful')
                    print("successful login")
                    return redirect('e_waste_app:home')

                else:
                    messages.error(request, 'Account not active')
                    return render(request, 'e_waste_app/Login.html', {'form': form})
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, 'e_waste_app/Login.html', {'form': form})
        else:
            messages.error(request, 'Invalid form details')
            return render(request, 'e_waste_app/Login.html', {'invalid_credentials': 'Invalid form details'})
    else:  # request.method==GET
        if request.user.is_authenticated:
            return redirect('e_waste_app:home')
        return render(request, 'e_waste_app/Login.html', {'form': LoginForm()})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('e_waste_app:logout'))


def password_reset(request):
    if request.method == 'GET':
        return render(request, 'e_waste_app/Password_reset.html', {'PasswordResetForm': PasswordResetForm()})
    else:  #POST
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            if user:
                subject = "Password Reset Request"
                email_template_name = "e_waste_app/password_reset_email.txt"
                c = {
                    'email': user.email,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }
                email = render_to_string(email_template_name, c)
                send_mail(subject, email, "no-reply@e_waste_network.com", [user.email])
            return redirect('e_waste_app:password_reset_done')
        else:
            return render(request, 'e_waste_app/Password_reset.html', {'PasswordResetForm': PasswordResetForm()})


def password_reset_done(request):
    return render(request, 'e_waste_app/password_reset_done.html')


def home(request):
    return render(request, 'e_waste_app/home.html')




def aboutus(request):
    return render(request, 'e_waste_app/aboutus.html')


def article1(request):
    return render(request, 'e_waste_app/article1.html')


def article2(request):
    return render(request, 'e_waste_app/article2.html')


def article3(request):
    return render(request, 'e_waste_app/article3.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contactus')
    else:
        form = ContactForm()
    return render(request, 'e_waste_app/contact_us.html', {'form': form})


def search_results(request):
    name_query = request.GET.get('name', '')
    zipcode_query = request.GET.get('zipcode', '')

    # Filter products based on name and zipcode
    products = Product.objects.filter(name__icontains=name_query, zipcode=zipcode_query)

    context = {
        'products': products
    }
    return render(request, 'e_waste_app/search_results.html', context)


def _validate_password(password):
    print('password', password)
    if password is not None:
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        if password.isdigit():
            raise ValidationError('Password must not contain only numbers')
        common_passwords = ['qwerty@123', '12345678']
        if password in common_passwords:
            raise ValidationError('Password cant be commonly used password')
        validators = [CommonPasswordValidator()]
        for validator in validators:
            validator.validate(password)
    else:
        raise ValidationError('Password is empty')


class CustomPasswordResetConfirmView(FormView):
    template_name = 'e_waste_app/password_reset_confirm.html'
    success_url = reverse_lazy('e_waste_app:password_reset_complete')
    form_class = PasswordResetConfirmForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')
        UserModel = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel.objects.get(pk=uid)
            print('user:', user.email)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        kwargs['user'] = user  # Provide the user to the form
        return kwargs

    def form_valid(self, form):
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')
        UserModel = get_user_model()
        print('uidb64: ', uidb64)
        print('token: ', token)
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            password1 = form.cleaned_data.get('new_password1')
            password2 = form.cleaned_data.get('new_password2')
            print('--new_password1:', password1)  # Debugging line
            print('--new_password2:', password2)  # Debugging line

            if password1 != password2:
                form.add_error(None, 'Passwords do not match')
                return self.form_invalid(form)

            try:
                print('password1:', password1)  # Debugging line
                print('password2:', password2)  # Debugging line

            except ValidationError as e:
                form.add_error(None, e.message)
                return self.form_invalid(form)

            user.set_password(password1)
            user.save()
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid token or user ID')
            return self.form_invalid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form,
                                                         'uid': self.kwargs['uidb64'],
                                                         'token': self.kwargs['token']})

    def get_context_data(self, **kwargs):
        # Add 'uidb64' and 'token' to the context in case of successful form submission
        context = super().get_context_data(**kwargs)
        context['uid'] = self.kwargs['uidb64']
        context['token'] = self.kwargs['token']
        return context


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'e_waste_app/password_reset_complete.html'


@login_required
def add_recycle_item(request):
    if request.method == 'POST':
        form = AddRecycleItemForm(request.POST, request.FILES)

        if form.is_valid():
            # Create instance but don't save to database yet
            recycling_request = form.save(commit=False)
            current_member = Member.objects.get(username=request.user)
            recycling_request.user = current_member
            if form.cleaned_data['user_profile_contact']:
                print("USER PROFILE CONTACT")
                recycling_request.email = current_member.email
                recycling_request.phone = current_member.phone_number
                recycling_request.address = current_member.address
                recycling_request.city = current_member.city
                recycling_request.province = current_member.province
                recycling_request.postal_code = current_member.postal_code
                recycling_request.country = current_member.country

            # Save the instance to the database
            recycling_request.save()
            return redirect('e_waste_app:view_recycle_items')
    else:
        form = AddRecycleItemForm()
    return render(request, 'e_waste_app/add_item.html', {'form': form})


def view_recycle_items(request):
    form = SearchRecycleItemsForm(request.GET or None)
    results = RecycleItem.objects.all().order_by('-created_at')

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        category = form.cleaned_data.get('category')
        location = form.cleaned_data.get('location')
        condition = form.cleaned_data.get('condition')
        sort_by = form.cleaned_data.get('sort_by')

        if keyword:
            results = results.filter(Q(description__icontains=keyword) | Q(item_type__icontains=keyword))
        if category:
            results = results.filter(category=category)
        if condition:
            results = results.filter(condition=condition)
        if location:
            results = results.filter(Q(postal_code=location) | Q(address__icontains=location)
                                     | Q(city__icontains=location) | Q(country__icontains=location)
                                     | Q(province__icontains=location))

        if sort_by:
            results = results.order_by(sort_by)

    # Convert CATEGORY_CHOICES to a dictionary
    category_choices_dict = dict(RecycleItem.CATEGORY_CHOICES)
    condition_choices_dict = dict(RecycleItem.CONDITION_CHOICES)

    context = {
        'form': form,
        'results': results,
        'category_choices': category_choices_dict,
        'condition_choices': condition_choices_dict,
    }

    return render(request, 'e_waste_app/search_items.html', context)

def recycle_item_detail(request, pk):
    item = get_object_or_404(RecycleItem, pk=pk)
    context = {
        'item': item,
        'category_choices': dict(RecycleItem.CATEGORY_CHOICES),
        'condition_choices': dict(RecycleItem.CONDITION_CHOICES),
    }
    return render(request, 'e_waste_app/recycle_item_detail.html', context)
