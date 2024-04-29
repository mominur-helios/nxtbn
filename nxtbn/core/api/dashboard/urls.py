from django.urls import path
from nxtbn.core.api.dashboard.views import PlugginsUploadView

urlpatterns = [
    path('upload-pluggins/', PlugginsUploadView.as_view(), name='upload_pluggins'),
]
