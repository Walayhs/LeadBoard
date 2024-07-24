from django.contrib import admin
from django.urls import path, include  # include is for including other URL configurations
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('repo.api_urls')),  # API routes
    path('', include('repo.web_urls')),  # HTML template routes
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
