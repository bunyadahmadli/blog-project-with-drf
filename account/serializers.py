from rest_framework import serializers
from account.models import Profile
from django.contrib.auth.models import User 
from django.contrib.auth.password_validation import validate_password

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields =('id','note','twitter')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        print(User)
        fields =('id','first_name','last_name','profile')
    

    def update(self,instance,validate_data):
        profile =validate_data.pop('profile')
        porfile_serializer = ProfileSerializer(instance.profile,data = profile)
        porfile_serializer.is_valid(raise_exception=True)
        porfile_serializer.save()
        return super(UserSerializer,self).update(instance,validate_data)

class ChangePassworSerializer(serializers.Serializer):
    old_password =serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password( self,value):
        validate_password(value)
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id','username','password')

    def validate(self,attrs):
        validate_password(attrs["password"])
        return attrs

    def create(self,validated_data):
        user = User.objects.create(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user
