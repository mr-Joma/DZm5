from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView

from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterValidateSerializer,
    AuthValidateSerializer,
    ConfirmationSerializer,
    TokenObtainPairSerializer,
)
from .models import CustomUser
import random
import string
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.cache import cache

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class AuthorizationAPIView(CreateAPIView):
    serializer_class = AuthValidateSerializer

    def post(self, request):
        # from users.tasks import add
        # add.delay(2, 2)
        
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            from users.tasks import login_log

            login_log.delay(user.email)
            
            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User account is not activated yet!'}
                )

            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={'error': 'User credentials are wrong!'}
        )


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        phone_number = serializer.validated_data.get('phone_number')
        birthdate = serializer.validated_data.get('birthdate')

        # Use transaction to ensure data consistency
        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                phone_number=phone_number,
                birthdate=birthdate,
                is_active=False
            )

            # Create a random 6-digit code
            code = ''.join(random.choices(string.digits, k=6))

            cache.set(
                f"confirmation_code:{user.id}",
                code,
                timeout=300
            )
            
            from users.tasks import send_email
            send_email.delay(code, email)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'user_id': user.id,
                'confirmation_code': code
            }
        )


class ConfirmUserAPIView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        
        code = serializer.validated_data["code"]

        redis_code = cache.get(f"confirmation_code:{user_id}")

        if redis_code is None:
            return Response(
                {"error": "Confirmation code expired or not found!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if redis_code != code:
            return Response(
                {"error": "Invalid confirmation code!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

            cache.delete(f"confirmation_code:{user.id}")

        return Response(
            status=status.HTTP_200_OK,
            data={
                'message': 'User аккаунт успешно активирован',
                'key': token.key
            }
        )