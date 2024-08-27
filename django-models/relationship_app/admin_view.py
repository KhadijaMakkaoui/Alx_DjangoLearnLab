from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

def is_admin(user):
    return user.userprofile.role == 'Admin'

@user_passes_test(is_admin)
def admin_view(request):
    return HttpResponse("Welcome to the Admin view!")