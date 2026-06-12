from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, AuthSerializer, ConfirmSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import ConfirmationCode
import random


@api_view(['POST'])
def registration_api_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )

    code = str(random.randint(100000, 999999))

    ConfirmationCode.objects.create(
        user=user,
        code=code
    )

    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id,'code': code})


@api_view(['POST'])
def authorization_api_view(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(
        username=username,
        password=password
    )

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)

        return Response(data={'key': token.key})

    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def confirm_api_view(request):
    serializer = ConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    code = serializer.validated_data['code']

    try:
        confirmation = ConfirmationCode.objects.get(code=code)
    except ConfirmationCode.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = confirmation.user
    user.is_active = True
    user.save()

    confirmation.delete()

    return Response(data={'message': 'User confirmed'})