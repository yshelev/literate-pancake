from django.db import models
from users.models import User


class AdCategory(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.name


class Ad(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)
	title = models.CharField(max_length=50, unique=True)
	description = models.CharField(max_length=300)
	image_url = models.URLField(max_length=500, blank=True, null=True)
	category = models.ForeignKey(
		AdCategory,
		on_delete=models.CASCADE
	)
	condition = models.CharField(max_length=300)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

class ExchangeProposal(models.Model):
	class StatusChoices(models.TextChoices):
		WAITING = "WT", "ожидает"
		ACCEPTED = "AT", "принята"
		REJECTED = "RJ", "отклонена"


	ad_sender = models.ForeignKey(
		Ad,
		related_name="ad_sender",
		on_delete=models.CASCADE
	)
	ad_receiver = models.ForeignKey(
		Ad,
		related_name="ad_receiver",
		on_delete=models.CASCADE
	)

	status = models.CharField(
		max_length=2,
		choices=StatusChoices.choices,
		default=StatusChoices.WAITING
	)
	comment = models.CharField(
		max_length=300,
	)

	created_at = models.DateTimeField(auto_now_add=True)