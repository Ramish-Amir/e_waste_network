from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import Product  # Assuming Product is your model

# Create your views here.
def home(request):
    return render(request,'e_waste_app/home.html')
def footer(request):
    return render(request,'e_waste_app/footer.html')

def aboutus(request):
    return render(request,'e_waste_app/aboutus.html')

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


def home(request):
    return render(request, 'e_waste_app/home.html')

def search_results(request):
    name_query = request.GET.get('name', '')
    zipcode_query = request.GET.get('zipcode', '')

    # Filter products based on name and zipcode
    products = Product.objects.filter(name__icontains=name_query, zipcode=zipcode_query)

    context = {
        'products': products
    }
    return render(request, 'e_waste_app/search_results.html', context)


