from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import CreateView
from .forms import PasswordResetConfirmForm, ProfileForm, ArticleForm
from .forms import LoginForm, RegisterForm, PasswordResetForm
from django.utils import timezone
from django.contrib import messages
from .forms import ContactForm
from .forms import FeedbackForm
from .models import Member, RecycleItem, Article
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_str
from .recycleForms import AddRecycleItemForm, SearchRecycleItemsForm, EditRecycleItemForm, HomepageSearchForm

#userhistory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Avg
from .models import RecycleItem, UserVisit
from datetime import date
import datetime



# Create your views here.

@login_required()
def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to view your profile.')
        return redirect('e_waste_app:login')

    user = request.user
    print('username: ', user.username)
    if request.user.is_authenticated:
        member_id = request.user.pk
        try:
            member = Member.objects.get(pk=member_id)
        except Member.DoesNotExist:
            messages.error(request, 'Member profile not found.')
            return redirect('e_waste_app:home')
    else:
        try:
            member_id = request.session.get('member_id')
            member = Member.objects.get(pk=member_id)
        except Member.DoesNotExist:
            messages.error(request, 'Member profile not found.')
            return redirect('e_waste_app:home')

    #print('member: ', member_id)
    #print('member username ', Member.objects.get(pk=member_id).username, "is authenticated: ", member.is_authenticated)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=member)  # Bind the form with the existing instance
        if form.is_valid():
            form.save()  # Update the existing instance
            return redirect('e_waste_app:home')
        else:
            messages.error(request, 'Please correct the errors.')
            return render(request, 'e_waste_app/profile.html', {'form': form})
    else:
        form = ProfileForm(instance=member)  # Initialize form with the existing instance
    return render(request, 'e_waste_app/profile.html', {'form': form})


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Member.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            request.session['member_id'] = user.id
            login(request, user)
            current_login = timezone.now().strftime("%d/%m/%Y %H:%M:%S")
            request.session['last_login'] = current_login
            request.session.set_expiry(60 * 60)
            messages.success(request, 'Your account has been activated!')
            return redirect('e_waste_app:profile')
        else:
            messages.error(request, 'The activation link is invalid or has expired.')
            return redirect('e_waste_app:login')


class LandingPageView(TemplateView):
    template_name = 'e_waste_app/landing_page.html'


class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'e_waste_app/Register.html'
    success_url = reverse_lazy('e_waste_app:landing')

    def send_verification_email(self, user, request):
        try:
            subject = "Activate your account"
            email_template_name = "e_waste_app/account_verification_email.html"
            c = {
                'email': user.email,
                'domain': get_current_site(request).domain,
                'site_name': 'E Waste Network',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',
                'username': user.username
            }
            email = render_to_string(email_template_name, c)
            send_mail(subject, email, "ewastenetwork@gmail.com", [user.email])
            print(f"Verification email sent to {user.email}")
            messages.info(request, f"Verification email sent to {user.email}")
        except Exception as e:
            print(f"Failed to send verification email: {e}")
            messages.error(request, f"Failed to send verification email: {e}")
            raise e

    def _validate_password(self, password):
        print('password', password)
        if password is not None:
            if len(password) < 8:
                raise ValidationError('Password must be at least 8 characters long')
            if password.isdigit():
                raise ValidationError('Password cannot contain only numbers')
            common_passwords = ['qwerty@123', '12345678']
            if password in common_passwords:
                raise ValidationError('Password is too common')
            validators = [CommonPasswordValidator()]
            for validator in validators:
                validator.validate(password)
        else:
            raise ValidationError('Empty Password')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        # Check if the username already exists
        if Member.objects.filter(username=username).exists():
            print('username', username, 'user exists')
            form.add_error('username', 'Username already taken')
            return self.form_invalid(form)
        print('username', username, 'user doesnt exists')
        # Validate password here
        try:
            self._validate_password(password)
        except ValidationError as e:
            form.add_error('password', e.message)
            return self.form_invalid(form)

        # Create the user
        member = Member.objects.create_user(username=username, email=email, password=password)
        member.is_active = False
        member.save()

        # Send verification email
        self.send_verification_email(member, self.request)
        self.request.session['member_id'] = member.id
        messages.success(self.request, f'Account created for {username}')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an issue with your input or Password did not match.')
        return super().form_invalid(form)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    current_login = timezone.now().strftime("%d/%m/%Y %H:%M:%S")
                    request.session['last_login'] = current_login
                    request.session.set_expiry(60 * 60)
                    #messages.success(request, 'Login successful')
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
    else:
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).last()  # Since multiple users with same email is acceptable
            # therefore latest created account will be considered for now
            if user:
                subject = "Password Reset Request"
                email_template_name = "e_waste_app/password_rest_email.html"
                c = {
                    'email': user.email,
                    'domain': get_current_site(request).domain,
                    'site_name': 'E Waste Network',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http',
                    'username': user.username
                }
                email = render_to_string(email_template_name, c)
                send_mail(subject, email, "ewastenetwork@gmail.com", [user.email])
            return redirect('e_waste_app:password_reset_done')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'e_waste_app/Password_reset.html', {'PasswordResetForm': PasswordResetForm()})


def password_reset_done(request):
    return render(request, 'e_waste_app/password_reset_done.html')


class HomeView(TemplateView):
    template_name = 'e_waste_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = HomepageSearchForm()
        context['featured_articles'] = Article.objects.filter(is_featured=True)
        return context


class AboutUsView(TemplateView):
    template_name = 'e_waste_app/aboutus.html'


class ContactUsView(FormView):
    template_name = 'e_waste_app/contact_us.html'
    form_class = ContactForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your message has been sent successfully!')
        return redirect('e_waste_app:contactus')


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()  # Assuming the form is saving the data
            messages.success(request, 'Thanks for giving feedback!')
            return redirect('e_waste_app:home')  # Redirect to the home page
    else:
        form = FeedbackForm()

    return render(request, 'e_waste_app/feedback.html', {'form': form})


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
            #print('--new_password1:', password1)  # Debugging line
            #print('--new_password2:', password2)  # Debugging line

            if password1 != password2:
                #form.add_error('password', 'Passwords do not match')
                #raise ValidationError('Passwords do not match')
                messages.error(self.request, 'Password do not match.')

                return self.form_invalid(form)

            try:
                print('password1:', password1)  # Debugging line
                print('password2:', password2)  # Debugging line
                user.set_password(password1)
                user.save()
                return super().form_valid(form)
            except ValidationError as e:
                form.add_error(None, str(e))
                return self.form_invalid(form)
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

            fields = [
                ('email', 'Email'),
                ('phone_number', 'Phone number'),
                ('address', 'Address'),
                ('city', 'City'),
                ('province', 'Province'),
                ('postal_code', 'Postal code'),
                ('country', 'Country')
            ]

            if form.cleaned_data['use_profile_contact']:
                # Check for missing fields in the profile
                missing_fields = [label for field, label in fields if not getattr(current_member, field)]

                if missing_fields:
                    form.add_error(None, "Your profile is missing contact information. "
                                         "Either complete your profile first or enter details manually.")
                    
            else:
                # Check if the form is missing required contact fields
                missing_form_fields = [label for field, label in fields if not form.cleaned_data.get(field)]

                if missing_form_fields:
                    form.add_error(None, "Please provide the missing contact information in the form.")

            if not form.errors:
                # Save the instance to the database
                recycling_request.save()

                #UserHistory
                # Increment action taken
                if 'actions_taken_today' in request.session:
                    request.session['actions_taken_today'] += 1
                else:
                    request.session['actions_taken_today'] = 1

                # Update the session with the recent post
                if 'recent_posts' not in request.session:
                    request.session['recent_posts'] = []

                recent_posts = request.session['recent_posts']
                recent_posts.append({
                    'id': recycling_request.id,
                    'item_type': recycling_request.item_type,
                    'description': recycling_request.description,
                    'created_at': recycling_request.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Store date in ISO format
                })
                # Keep only the 5 most recent posts
                request.session['recent_posts'] = recent_posts[-5:]
                request.session.modified = True

                return redirect('e_waste_app:view_recycle_items')
    else:
        form = AddRecycleItemForm()

    return render(request, 'e_waste_app/add_item.html', {'form': form})


def view_recycle_items(request):
    form = SearchRecycleItemsForm(request.GET or None)
    results = RecycleItem.objects.filter(is_active=True).order_by('-created_at')

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

    context = {
        'form': form,
        'results': results,
        'category_choices': dict(RecycleItem.CATEGORY_CHOICES),
        'condition_choices': dict(RecycleItem.CONDITION_CHOICES),
    }
    return render(request, 'e_waste_app/search_items.html', context)


@login_required
def view_my_items(request):
    current_member = Member.objects.get(username=request.user)
    my_items = RecycleItem.objects.filter(user=current_member).order_by('-created_at')
    active_items = my_items.filter(is_active=True)
    inactive_items = my_items.filter(is_active=False)

    context = {
        'active_items': active_items,
        'inactive_items': inactive_items,
        'category_choices': dict(RecycleItem.CATEGORY_CHOICES),
        'condition_choices': dict(RecycleItem.CONDITION_CHOICES),
    }

    return render(request, 'e_waste_app/my_items.html', context)


@login_required
def mark_as_unavailable(request, pk):
    item = get_object_or_404(RecycleItem, pk=pk, user=request.user)
    if request.method == "POST":
        item.is_active = False
        item.save()
        return redirect('e_waste_app:view_my_items')
    return render(request, 'confirm_unavailable_item.html', {'item': item})


@login_required
def delete_item(request, pk):
    item = get_object_or_404(RecycleItem, pk=pk, user=request.user)
    if request.method == "POST":
        item.delete()
        return redirect(reverse_lazy('e_waste_app:view_my_items'))
    return render(request, 'confirm_delete_item.html', {'item': item})


@login_required
def edit_item(request, pk):
    item = get_object_or_404(RecycleItem, pk=pk, user=request.user)
    if request.method == "POST":
        form = EditRecycleItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('e_waste_app:view_my_items'))
    else:
        form = EditRecycleItemForm(instance=item)
    return render(request, 'e_waste_app/item_edit_form.html', {'form': form, 'user': item.user})


def recycle_item_detail(request, pk):
    item = get_object_or_404(RecycleItem, pk=pk)
    context = {
        'item': item,
        'category_choices': dict(RecycleItem.CATEGORY_CHOICES),
        'condition_choices': dict(RecycleItem.CONDITION_CHOICES),
    }
    return render(request, 'e_waste_app/recycle_item_detail.html', context)


def not_found(request, exception):
    return render(request, 'e_waste_app/404.html', status=404)


def article_list_view(request):
    articles = Article.objects.all()
    return render(request, 'e_waste_app/articles_list.html', {'articles': articles})


def article_detail_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'e_waste_app/article_detail.html', {'article': article})


@login_required
def member_articles(request):
    articles = Article.objects.filter(author=request.user)
    return render(request, 'e_waste_app/member_articles.html', {'articles': articles})


@login_required
def article_create_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            print(request.user)
            article.author = Member.objects.get(username=request.user)
            # Set the author to the current user
            article.save()
            messages.success(request, 'Article created successfully!')
            return redirect(reverse_lazy('e_waste_app:article_list'))
    else:
        form = ArticleForm()
    return render(request, 'e_waste_app/article_form.html', {'form': form})


@login_required
def article_update_view(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect(reverse_lazy('e_waste_app:article_list'))
    else:
        if article.author.username != request.user.username:
            messages.error(request, 'You are not authorized to edit this article.')
            return redirect('e_waste_app:article_list')
        form = ArticleForm(instance=article)

    return render(request, 'e_waste_app/article_form.html', {'form': form})


@login_required
def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.author.username != request.user.username:
        messages.error(request, 'You are not authorized to delete this article.')
        return redirect('e_waste_app:article_list')

    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted successfully!')
        return redirect(reverse_lazy('e_waste_app:article_list'))

    return render(request, 'e_waste_app/article_confirm_delete.html', {'article': article})


#Userhistory
@login_required
def dashboard(request):
    #Last Login
    user = request.user
    # Track last login time
    if not user.last_login:
        user.last_login = timezone.now()
        user.save()
    last_login_time = user.last_login
    # Store last visit time in session
    if 'last_visit' not in request.session:
        request.session['last_visit'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    #Session Posts
    recent_posts = request.session.get('recent_posts', [])

    # Update last visit time
    current_time = timezone.now()
    request.session['last_visit'] = current_time.strftime('%Y-%m-%d %H:%M:%S')

    # Number of visits today
    today = date.today().strftime("%Y-%m-%d")
    session_key = f"visits_{today}"
    visits_today = request.session.get(session_key, 0)


    total_visit_duration_today = request.session.get('total_visit_duration_today', 0)
    hours, remainder = divmod(total_visit_duration_today, 3600)
    minutes, seconds = divmod(remainder, 60)
    actions_taken_today = request.session.get('actions_taken_today', 0)
    #last_login_time = request.session.get('last_login_time', 'N/A')
    context = {
        'total_visit_duration_today': f"{int(hours)}h {int(minutes)}m {int(seconds)}s",
        'actions_taken_today': actions_taken_today,
        'last_login_time': last_login_time,
        'recent_posted_requests': recent_posts,
        'number_of_visits_today': visits_today,
    }
    return render(request, 'e_waste_app/dashboard.html', context)