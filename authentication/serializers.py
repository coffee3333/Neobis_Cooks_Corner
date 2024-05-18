from django.contrib.auth.models import User
from rest_framework import serializers
from authentication.models import User



class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password',
            'photo',
            'user_bio',
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'photo',
            'user_bio',
            'count_followers',
            'count_following',
            'count_recipes',
        ]


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "username",
            "photo",
            "user_bio",
        ]

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.email)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.user_bio = validated_data.get('user_bio', instance.user_bio)

        instance.save()

        return instance