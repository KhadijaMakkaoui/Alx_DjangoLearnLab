from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
auth_views.LoginView.as_view()
auth_views.LogoutView.as_view()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to profile page
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/templates/blog/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        request.user.email = email
        request.user.save()
        return redirect('profile')
    return render(request, 'blog/templates/blog/profile.html')