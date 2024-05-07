from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
 class Meta:
  model = CustomUser
  fields =  ('username', 'fname', 'lname','phone' , 'address', 'AccessLevel')

    # fields =  ["id", "fname","lname","mobile", "username","password"]