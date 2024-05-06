from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views as home_views


urlpatterns = [
    path('', home_views.home, name='home'),
    path("robots.txt", home_views.robots_txt, name="robots_txt"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)