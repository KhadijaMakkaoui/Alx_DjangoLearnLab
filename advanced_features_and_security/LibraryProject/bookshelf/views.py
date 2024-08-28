from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Book
from django import forms
from .forms import ExampleForm
# Create your views here.
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})


class BookSearchForm(forms.Form):
    query = forms.CharField(max_length=100)

def search_books(request):
    form = BookSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        books = Book.objects.filter(title__icontains=query)
        return render(request, 'books/search_results.html', {'books': books})
    else:
        return render(request, 'books/search.html', {'form': form})
