from django.utils import timezone
from rest_framework import serializers

from .models import Ad, AdCategory, ExchangeProposal

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = AdCategory
		fields = [
			"name"
		]

class AdSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ad
		fields = [
			"title",
			"description",
			"condition",

			"category",
			"user"
		]

	def create(self, validated_data):
		ad = Ad.objects.create(**validated_data)
		ad.last_login = timezone.now
		return ad

	def update(self, instance, validated_data):
		instance.title = validated_data.get("title", instance.title)
		instance.description = validated_data.get("description", instance.description)
		instance.image_url = validated_data.get("image_url", instance.image_url)
		instance.condition = validated_data.get("condition", instance.condition)
		instance.category = validated_data.get("category", instance.category)

		instance.save()

		return instance


class CreateExchangeProposalSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExchangeProposal
		fields = ["ad_sender",
		          "ad_receiver",
		          "comment"]


	def create(self, validated_data):
		if validated_data.get("status"):
			validated_data.pop("status")
		return ExchangeProposal.objects.create(**validated_data)

class ExchangeProposalSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExchangeProposal
		fields = "__all__"

class UpdateExchangeProposalSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExchangeProposal
		fields = ["comment"]

	def update(self, instance, validated_data):
		instance.comment = validated_data.get("comment", instance.comment)
		status = validated_data.get("status")
		if status in [ExchangeProposal.StatusChoices.ACCEPTED,
		              ExchangeProposal.StatusChoices.REJECTED]:
			instance.status = status

		instance.save()
		return instance