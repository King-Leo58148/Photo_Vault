from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Photo,Album
User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['id','username','password','email']
    def create(self,validated_data):
        user=User( username=validated_data['username'],
                    email=validated_data['email'])
            
        user.set_password (validated_data['password'])
        user.save()
        return user

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model=Album
        fields=['album_name']

class PhotoSerializer(serializers.ModelSerializer):
    album = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    class Meta:
        model=Photo
        fields=['id','title','description','photo','private','album']
    def create(self, validated_data):
         album_name = validated_data.pop('album', None) 
         album = None 
         if album_name: 
            album, _ = Album.objects.get_or_create(album_name=album_name) 
         return Photo.objects.create(album=album, **validated_data)