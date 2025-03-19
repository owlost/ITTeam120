from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

def home_redirect(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('accounts/', include('accounts.urls')),
    path("api/", include("books.urls")),
    path('', home_redirect, name='home'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
