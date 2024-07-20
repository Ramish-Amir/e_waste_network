from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import LoginForm, RegisterForm, PasswordResetForm
from django.utils import timezone
from django.contrib import messages
from .forms import ContactForm
from .models import Product, Member, RecycleItem
from django.db.models import Q
from django.shortcuts import render, redirect
from .recycleForms import AddRecycleItemForm, SearchRecycleItemsForm
from .models import RecycleItem


# Create your views here.


def profile(request):
    render(request, '', {})


def user_register(request):
    print(request)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            #form.save()
            #print("this is username",form.cleaned_data)
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
            user = User.objects.create_user(username=username, email=email, password=user_password)
            user.save()
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
    #return HttpResponseRedirect(reverse('myapp:index'))


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


def footer(request):
    return render(request, 'e_waste_app/footer.html')


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
    results = RecycleItem.objects.all()

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        category = form.cleaned_data.get('category')
        location = form.cleaned_data.get('location')
        sort_by = form.cleaned_data.get('sort_by')

        if keyword:
            results = results.filter(Q(description__icontains=keyword) | Q(item_type__icontains=keyword))
        if category:
            results = results.filter(category=category)
        if location:
            results = results.filter(Q(postal_code=location) | Q(address__icontains=location)
                                     | Q(city__icontains=location) | Q(country__icontains=location)
                                     | Q(province__icontains=location))

        if sort_by:
            results = results.order_by(sort_by)

    # Convert CATEGORY_CHOICES to a dictionary
    category_choices_dict = dict(RecycleItem.CATEGORY_CHOICES)

    context = {
        'form': form,
        'results': results,
        'category_choices': category_choices_dict,
    }

    return render(request, 'e_waste_app/search_items.html', context)
