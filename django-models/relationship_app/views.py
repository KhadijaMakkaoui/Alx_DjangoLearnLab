from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from .models import Library


# Create your views here.
def list_books(request):
    books = Book.objects.all()
    response_text = '\n'.join([f"{book.title} by {book.author}" for book in books])
    return HttpResponse(response_text, content_type='text/plain')

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # You need to create this template
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()  # Assuming a ForeignKey or ManyToMany relationship
        return context