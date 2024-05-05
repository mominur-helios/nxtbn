# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from nxtbn.users.api.storefront.serializers import CustomTokenObtainPairSerializer, SignupSerializer
from allauth.account import app_settings as allauth_settings
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions  import AllowAny
from allauth.account.utils import complete_signup
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from allauth.account.models import EmailAddress



from rest_framework_simplejwt.views import TokenObtainPairView

from nxtbn.users.utils.jwt_utils import generate_access_token, generate_jwt_token, verify_jwt_token


class SignupView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        complete_signup(request._request, user, allauth_settings.EMAIL_VERIFICATION, None)

        response_data = {"detail": _("Verification e-mail sent. Please check your email.")}

        if allauth_settings.EMAIL_VERIFICATION != allauth_settings.EmailVerificationMethod.MANDATORY:
            # If email verification is not mandatory, return an access token
            access_token = generate_access_token(user)
            response_data = {
                'user': serializer.data,
                'token': {
                    'access': access_token,
                },
            }

        return Response(response_data, status=status.HTTP_201_CREATED)



class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if user:
            # Check if email verification is mandatory
            email_verification_required = (
                allauth_settings.EMAIL_VERIFICATION == allauth_settings.EmailVerificationMethod.MANDATORY
            )
            email_verified = EmailAddress.objects.filter(user=user, verified=True).exists()

            if email_verification_required and not email_verified:
                return Response(
                    {"detail": "Email not verified. Please verify your email."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            access_token = generate_access_token(user)

            return Response(
                {
                    "user": {"email": user.email},
                    "token": {"access": access_token},
                },
                status=status.HTTP_200_OK,
            )

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    


class TokenRefreshView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = verify_jwt_token(refresh_token)

        if user:
            access_token = generate_access_token(user)
            return Response(
                {
                    "token": {
                        "access": access_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "Invalid or expired refresh token."},
            status=status.HTTP_401_UNAUTHORIZED,
        )