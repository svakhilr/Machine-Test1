from rest_framework import serializers
from .models import UserProfile,CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email    = serializers.CharField(source='user.email')
    password = serializers.CharField(source='user.password',write_only=True)
    confirm_password = serializers.CharField(source='user.confirm_password',write_only=True)
   
    class Meta:
        model= UserProfile
        fields = ("username","email","profile_name","mobile_number","password","confirm_password")

    def validate(self, attrs):
        print(attrs["user"]["password"])
        email = attrs["user"]["email"]
        username = attrs["user"]["username"]
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username must be Unique")
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email Already Exists")
        if attrs["user"]['password'] != attrs["user"]["confirm_password"]:
            raise serializers.ValidationError("password doesn't match")
        return super().validate(attrs)

    def create(self, validated_data):
        user = validated_data.pop("user")
        user = CustomUser.objects.create_user(email = user["email"],username = user["username"],password=user["password"])
        validated_data["user"] = user
        return super().create(validated_data)
    

class ProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email    = serializers.CharField(source='user.email')

    class Meta:
        model = UserProfile 
        fields = ("username","email","profile_name","mobile_number")

    def validate(self, attrs):
        user_data = attrs.get("user")
        if user_data:
            if "username" in user_data:
                if CustomUser.objects.filter(username= user_data["username"]).exists():
                    raise serializers.ValidationError("Username already taken")
            if "email" in user_data:
                if CustomUser.objects.filter(email= user_data["email"]).exists():
                    raise serializers.ValidationError("Email Already Taken")
        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user',None)
        if user_data:
            CustomUser.objects.filter(id=instance.user.id).update(**user_data)
        return super().update(instance,validated_data)
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()