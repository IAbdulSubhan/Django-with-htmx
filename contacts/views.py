from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . models import *
from django.db.models import Q
from contacts.forms import *
from django.views.decorators.http import require_http_methods


# Create your views here.
@login_required
def index(request):
    contacts = request.user.contacts.all().order_by('-created_at')
    print(contacts)
    context = {"contacts": contacts,
               "form": ContactForm()
               }
    return render(request, 'contacts.html', context)


@login_required
def search_contact(request):
    import time
    time.sleep(2)
    query = request.GET.get('search', '')

    print(query)
    contacts = request.user.contacts.filter(
        Q(name__icontains=query) | Q(email__icontains=query)
    )
    context = {'contacts': contacts}

    return render(request, 'partials/contact-list.html', context)

@login_required
@require_http_methods(['POST'])
def create_contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        contact = form.save(commit=False) #dont save form directly associate the user with this first
        contact.user = request.user
        contact.save()  