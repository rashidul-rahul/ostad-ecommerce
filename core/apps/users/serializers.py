from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.utils import timezone

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'password2', 'first_name', 'last_name')

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')


class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Override the username_field so that it uses phone_number instead of username.
    username_field = 'phone_number'

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        if phone_number and password:
            # Ensure that the payload has the phone_number key.
            attrs[self.username_field] = phone_number
        else:
            raise serializers.ValidationError('Must include "phone_number" and "password".')

        # Call the superclass to validate and generate tokens.
        data = super().validate(attrs)

        # Calculate expires_in (remaining seconds until token expiration)
        exp_timestamp = self.get_token(self.user)['exp']
        current_timestamp = int(timezone.now().timestamp())
        data['expires_in'] = exp_timestamp - current_timestamp

        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh_token = self.initial_data.get("refresh")
        refresh_obj = RefreshToken(refresh_token)

        new_access_token = refresh_obj.access_token
        data = {"access": str(new_access_token)}

        exp_timestamp = new_access_token["exp"]
        current_timestamp = int(timezone.now().timestamp())
        data["expires_in"] = exp_timestamp - current_timestamp

        return data
