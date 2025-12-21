from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Photo
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



class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model=Photo
        fields=['id','title','description','photo','private']
       
    def get_photo(self, obj): 
        return obj.photo.url if obj.photo else None