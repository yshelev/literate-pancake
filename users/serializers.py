from rest_framework import serializers

from ads.models import ExchangeProposal
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["username",
		          "password",
		          "email"]

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["username",
		          "email"]

