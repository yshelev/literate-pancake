from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from ads.models import Ad, AdCategory, ExchangeProposal
from users.models import User


class ViewTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(
			username="test",
			password="test",
			email="test@example.com",
		)

		self.client.force_authenticate(user=self.user)

		adc = AdCategory.objects.create(
			name="Тестовая категория"
		)

		self.ad = Ad.objects.create(
			title="test_title",
			description="test_description",
			image_url="https://test.jpg",
			condition="test",
			created_at="2025-05-04 22:52:43.000",
			user=self.user,
			category=adc
		)
		self.ad2 = Ad.objects.create(
			title="second_test_title",
			description="second_test_description",
			image_url="https://2test.jpg",
			condition="test2",
			created_at="2025-05-04 22:52:43.000",
			user=self.user,
			category=adc
		)

		self.ad3 = Ad.objects.create(
			title="3_test_title",
			description="3_test_description",
			condition="test_3",
			created_at="2025-05-04 22:52:43.000",
			user=self.user,
			category=adc
		)

		self.proposal = ExchangeProposal.objects.create(
			ad_sender=self.ad,
			ad_receiver=self.ad2,
			comment="test_comment",
			created_at=timezone.now
		)

	def test_getting_ad(self):
		response = self.client.get(f"/api/ad/?id={self.ad.id}")
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'test_description')

	def test_false_getting_ad(self):
		response = self.client.get("/api/ad/?id=-1")
		self.assertEqual(response.status_code, 404)

	def test_update_ad_and_check(self):
		response = self.client.get(f"/api/ad/?id={self.ad.id}")
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "test_title")

		response = self.client.put(f"/api/ad/{self.ad.id}", {
			"title": "title_test"
		})
		self.assertEqual(response.status_code, 202)

		response = self.client.get(f"/api/ad/?id={self.ad.id}")
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "title_test")

	def test_delete_ad_and_get(self):
		response = self.client.get(f"/api/ad/?id={self.ad.id}")
		self.assertEqual(response.status_code, 200)
		response = self.client.delete(f"/api/ad/{self.ad.id}")
		self.assertEqual(response.status_code, 202)
		response = self.client.get(f"/api/ad/?id={self.ad.id}")
		self.assertEqual(response.status_code, 404)

	def test_exchange_proposal_view_put_get(self):
		response = self.client.get(f"/api/proposal/?id={self.proposal.id}")
		self.assertEqual(response.status_code, 200)

		response = self.client.put(f"/api/proposal/{self.proposal.id}/", {
			"comment": "123"
		})
		self.assertEqual(response.status_code, 202)

		response = self.client.get(f"/api/proposal/?id={self.proposal.id}")
		self.assertContains(response, "123")

	def test_exchange_proposal_view_delete(self):
		response = self.client.delete(f"/api/proposal/{self.proposal.id}/")
		self.assertEqual(response.status_code, 200)

		response = self.client.get(f"/api/proposal/?id={self.proposal.id}")
		self.assertEqual(response.status_code, 404)



