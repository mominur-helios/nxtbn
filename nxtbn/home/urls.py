from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from nxtbn.home import views as home_views
from nxtbn.seo import views as seo_views


urlpatterns = [
    path('', home_views.home, name='home'),
    path("robots.txt", seo_views.robots_txt, name="robots_txt"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)