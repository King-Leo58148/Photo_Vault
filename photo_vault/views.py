from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication,authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import status
from . serializers import UserSerializer,PhotoSerializer
from django.contrib.auth import get_user_model

User=get_user_model()
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
  serializer=UserSerializer(data=request.data)
  if serializer.is_valid():
    user=serializer.save()
    token=Token.objects.create(user=user)
    return Response({'token':token.key,'user':serializer.data},status=status.HTTP_201_CREATED)
  return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
  username=request.data.get('username')
  password=request.data.get('password')
  if username is None or password is None :
    return Response({"error":"Please provide both username and password"})
  user=authenticate(username=username,password=password)
  if not user:
    return Response({"error":"Invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)
  token,create=Token.objects.get_or_create(user=user)
  return Response({"token":token.key,"message":"Login Successful"})

@api_view(['POST'])
def logout(request):
  request.user.auth_token.delete()
  return Response({"message":"Logged out Successfully"})