from django.http import HttpResponse
from django.shortcuts import render, redirect
from .recycleForms import RecyclingRequestForm, RecyclingRequestSearchForm
from .models import RecyclingRequest


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def post_recycling_request(request):
    if request.method == 'POST':
        form = RecyclingRequestForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('e_waste_app:search_recycling_requests')
    else:
        form = RecyclingRequestForm(user=request.user)
    return render(request, 'e_waste_app/post_request.html', {'form': form})


def search_recycling_requests(request):
    form = RecyclingRequestSearchForm(request.GET or None)
    results = RecyclingRequest.objects.all()

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        category = form.cleaned_data.get('category')
        city = form.cleaned_data.get('city')

        if keyword:
            results = results.filter(description__icontains=keyword)
        if category:
            results = results.filter(category=category)
        if city:
            results = results.filter(contact_city__icontains=city)

    return render(request, 'e_waste_app/search_requests.html', {'form': form, 'results': results})
