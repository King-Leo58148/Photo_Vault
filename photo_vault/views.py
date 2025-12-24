from django.shortcuts import render,get_object_or_404,get_list_or_404
from rest_framework.authentication import SessionAuthentication,authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import status
from . serializers import UserSerializer,PhotoSerializer
from . models import Photo
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

@api_view(['POST'])
def upload_photo(request):
  serializer=PhotoSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save(user=request.user)
    return Response(serializer.data,status = status.HTTP_201_CREATED)
  return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['GET'])
def list_photos(request):
      photos = Photo.objects.filter(user=request.user)
      serializer = PhotoSerializer(photos, many=True)
      return Response(serializer.data)

@api_view(['GET'])
def view_photo(request, photo_id):
  photo=get_object_or_404(Photo,user=request.user,pk=photo_id)
  serializer = PhotoSerializer(photo)
  return Response(serializer.data)

@api_view(['GET'])
def public_photo(request, photo_id):
  photo=get_object_or_404(Photo,pk=photo_id,private=False)
  serializer = PhotoSerializer(photo)
  return Response(serializer.data)

@api_view(['GET'])
def all_public_photos(request):
  photos=get_list_or_404(Photo,private=False)
  serializer=PhotoSerializer(photos,many=True)
  return Response(serializer.data)

@api_view(['DELETE'])
def delete_photo(request,photo_id):
   photo=get_object_or_404(Photo,pk=photo_id)
   photo.delete()
   return Response({"message":"photo deleted"},status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def get_album(request,album_name):
  album=get_list_or_404(Photo,user=request.user,album__album_name=album_name)
  serializer=PhotoSerializer(album,many=True)
  return Response(serializer.data)