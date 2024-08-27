from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

# Create your views here.
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # You need to create this template
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()  # Assuming a ForeignKey or ManyToMany relationship
        return context
    
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after registration
            return redirect('list_books')  # Redirect to the desired page after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def Admin(user):
        return user.userprofile.role == 'Admin'

@user_passes_test(Admin)
def admin_view(request):
    return HttpResponse("Welcome to the Admin view!")
    
class Librarian():
    def is_librarian(user):
        return user.userprofile.role == 'Librarian'

    @user_passes_test(is_librarian)
    def librarian_view(request):
        return HttpResponse("Welcome to the Librarian view!")
class Member():
   def is_member(user):
    return user.userprofile.role == 'Member'

    @user_passes_test(is_member)
    def member_view(request):
        return HttpResponse("Welcome to the Member view!")