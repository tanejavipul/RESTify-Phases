from django.core.validators import validate_email
from django.shortcuts import redirect
from rest_framework import serializers, request
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
import re

from accounts.models import User


class SignUpSerializer(ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'phone', 'last_name', 'email', 'password', 'password2']

    def validate(self, attrs):
        # NAMES
        # ^([A-Za-z]+[' .-]?)*$
        if 'first_name' in attrs:
            if re.search("^[A-Za-z][A-Za-z' .-]*$", attrs['first_name']) is None and len(attrs['first_name']) != 0:
                raise serializers.ValidationError({"name": "Names can only contain letters, spaces and '-."})
        if 'last_name' in attrs:
            if re.search("^[A-Za-z][A-Za-z' .-]*$", attrs['last_name']) is None and len(attrs['last_name']) != 0:
                raise serializers.ValidationError({"name": "Names can only contain letters, spaces and '-."})

        #USERNAME
        if re.search("^([A-Za-z][A-Za-z0-9_.-]*){4,}$", attrs['username']) is None:
            raise serializers.ValidationError(
                {"username": "Username must start with a letter. Can contain numbers and (-_.). (Minimum Length: 4)"})

        if len(attrs['password']) < 8:
            raise serializers.ValidationError({"password": "Password To Short."})
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email', '')
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        phone = validated_data.get('phone', '') #+12223334444

        user = User.objects.create(
            username=validated_data['username'],
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ProfileSerializer(ModelSerializer):

    username = serializers.CharField(read_only=True, required=False)  # username will only be printed out
    old_password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    new_password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    new_password2 = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'avatar', 'old_password', 'new_password', 'new_password2']

    def validate(self, attrs):
        # NAMES
        # ^([A-Za-z]+[' .-]?)*$
        if 'first_name' in attrs:
            if re.search("^[A-Za-z][A-Za-z' .-]*$", attrs['first_name']) is None and len(attrs['first_name']) != 0:
                raise serializers.ValidationError({"firstname": "Names can only contain letters, spaces and '-."})

        if 'last_name' in attrs:
            if re.search("^[A-Za-z][A-Za-z' .-]*$", attrs['last_name']) is None and len(attrs['last_name']) != 0:
                raise serializers.ValidationError({"lastname": "Names can only contain letters, spaces and '-."})

        if 'email' in attrs:
            try:
                validate_email(attrs['email'])
            except:
                raise serializers.ValidationError({"email": "Please provide a valid email address"})

        if 'old_password' in attrs and 'new_password' not in attrs:
            raise serializers.ValidationError({"password": "New Password Not Provided"})

        if 'new_password' in attrs:
            if not self.instance.check_password(attrs['old_password']):
                raise serializers.ValidationError({"password": "Old password entered is incorrect."})
            if len(attrs['new_password']) < 8:
                raise serializers.ValidationError({"password": "New password minimum length has to be 8 characters."})
            if 'new_password2' not in attrs or attrs['new_password'] != attrs['new_password2']:
                raise serializers.ValidationError({"password": "New password field's did not match."})
        return attrs

    def update(self, instance, validated_data):
        if 'old_password' in validated_data and 'new_password' in validated_data:
            instance.set_password(validated_data['new_password'])

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()

        return instance




