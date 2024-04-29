import os
import zipfile

from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions  import AllowAny
from rest_framework.exceptions import APIException

from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.files.storage import FileSystemStorage


from nxtbn.core.api.dashboard.serializers import ZipFileUploadSerializer

PLUGIN_UPLOAD_DIR = getattr(settings, 'PLUGIN_UPLOAD_DIR')

os.makedirs(PLUGIN_UPLOAD_DIR, exist_ok=True)


plugin_storage = FileSystemStorage(location=PLUGIN_UPLOAD_DIR)

class PlugginsUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ZipFileUploadSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']

            storage = FileSystemStorage(location=PLUGIN_UPLOAD_DIR)
            file_path = storage.save(uploaded_file.name, uploaded_file)

            full_file_path = os.path.join(PLUGIN_UPLOAD_DIR, uploaded_file.name)
            with zipfile.ZipFile(full_file_path, 'r') as zip_ref:
                zip_ref.extractall(PLUGIN_UPLOAD_DIR)

            return Response(
                {'message': 'ZIP file uploaded and extracted successfully'},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)