from django.shortcuts import render
from core.generator import PDFGenerator


def home(request):
    return render(request, 'core/home.html', {})

def contacts(request):
    return render(request, 'core/contacts.html', {})

def docs(request):
    return render(request, 'core/docs.html', {})
