from rest_framework import serializers
from django.contrib.auth.models import User
from .models import bugs_report

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class BugSerializer(serializers.ModelSerializer):
    class Meta:
        model = bugs_report
        fields = ['id', 'bug_title', 'bug_description', 'status']
