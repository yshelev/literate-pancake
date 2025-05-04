import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import AdSerializer, UpdateExchangeProposalSerializer, CreateExchangeProposalSerializer, \
	ExchangeProposalSerializer

from ads.models import Ad, AdCategory, ExchangeProposal
from .utils import get_filtered_data, get_paginated_data


class AdDeletePutView(APIView):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	@swagger_auto_schema(
		operation_description="Удаление объекта рекламы",
		responses={
			202: "Object deleted",
			400: "bad request",
			404: "ad with ad_id is not found",
			403: "you cannot access another's ad"
		}
	)
	def delete(self, request, ad_id):
		if ad_id is None:
			return Response(data={"message": "no ad's id in data"},
			                status=status.HTTP_400_BAD_REQUEST)

		try:
			ad = Ad.objects.get(id=ad_id)
		except Ad.DoesNotExist:
			return Response(data={"message": f"ad with id {ad_id} is not found"},
			                status=status.HTTP_404_NOT_FOUND)

		if ad.user_id != request.user.id:
			return Response(data={"message": "you cannot access another's ad"},
			                status=status.HTTP_403_FORBIDDEN)

		ad.delete()

		return Response(data={"message": "ad deleted"},
		                status=status.HTTP_202_ACCEPTED)

	@swagger_auto_schema(
		operation_description="Изменение объекта рекламы",
		request_body=AdSerializer,
		responses={
			202: AdSerializer,
			400: "bad request",
			404: "ad\category is not found",
			403: "you cannot access another's ad"
		}
	)
	def put(self, request, ad_id):
		data = request.data

		category_id = data.get("category")

		if category_id is not None:
			try:
				_ = AdCategory.objects.get(id=category_id)
			except AdCategory.DoesNotExist:
				return Response(data={"message": "category does not exists"},
				                status=status.HTTP_404_NOT_FOUND)

		try:
			ad = Ad.objects.get(id=ad_id)
		except Ad.DoesNotExist:
			return Response(data={"message": "object that you try to patch does not exists,"
			                                 " you can try use post method to create new object"},
			                status=status.HTTP_404_NOT_FOUND)


		if ad.user_id != request.user.id:
			return Response(data={"message": "you cannot access another's ad"},
			                status=status.HTTP_403_FORBIDDEN)

		serializer = AdSerializer(data=data, instance=ad, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(data=serializer.data,
		                status=status.HTTP_202_ACCEPTED)

class AdView(APIView):
	@swagger_auto_schema(
		operation_description="Выдача рекламы по id",
		manual_parameters=[
			openapi.Parameter(
			'id',
			openapi.IN_QUERY,
			description="Поиск по id",
			type=openapi.TYPE_INTEGER
		)],
		responses={
			200: AdSerializer,
			404: "ad with id not found"
		}
	)
	def get(self, request):
		id_ = request.query_params.get("id")

		try:
			ad = Ad.objects.get(id=id_)
		except Ad.DoesNotExist as e:
			return Response(data={"message": "Ad is not found"},
			                status=status.HTTP_404_NOT_FOUND)

		serializer = AdSerializer(instance=ad)

		return Response(data=serializer.data,
		                status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Создание объекта рекламы",
		request_body=AdSerializer,
		responses={
			201: AdSerializer,
			400: "bad request"
		}
	)
	def post(self, request):
		data = request.data

		serializer = AdSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(data=serializer.data,
		                status=status.HTTP_201_CREATED)


class ExchangeProposalGetPostView(APIView):
	@swagger_auto_schema(
		operation_description="Получение предложения по id",
		manual_parameters=[
			openapi.Parameter(
				'id',
				openapi.IN_QUERY,
				description="Поиск по id",
				type=openapi.TYPE_INTEGER
			)],
		responses={
			200: ExchangeProposalSerializer,
			404: "proposal with ad_id is not found"
		}
	)
	def get(self, request):
		id_ = request.query_params.get("id")
		exchange_proposal = get_object_or_404(ExchangeProposal, id=id_)
		serializer = ExchangeProposalSerializer(instance=exchange_proposal)

		return Response(status=status.HTTP_200_OK,
		                data=serializer.data)

	@swagger_auto_schema(
		operation_description="Создание объекта предложения",
		request_body=CreateExchangeProposalSerializer,
		responses={
			201: "Object created",
			400: "bad request",
			404: "ad with ad_id is not found"
		}
	)
	def post(self, request):
		data = request.data
		print(request.user)
		if not data:
			return Response(status=status.HTTP_400_BAD_REQUEST,
			                data={"message": "body is empty"})

		receiver = data.get("ad_receiver")
		sender = data.get("ad_sender")

		if receiver is None or sender is None:
			return Response(status=status.HTTP_400_BAD_REQUEST,
			                data={"message": "receiver and sender needed"})

		if receiver == sender:
			return Response(status=status.HTTP_400_BAD_REQUEST,
			                data={"message": "receiver must not be equal to sender"})

		serializer = CreateExchangeProposalSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(status=status.HTTP_201_CREATED,
		                data=serializer.data)


class ExchangeProposalDeletePutView(APIView):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	@swagger_auto_schema(
		operation_description="Удаление объекта предложения",
		responses={
			200: "Object deleted",
			400: "bad request",
			404: "proposal with proposal_id is not found"
		}
	)
	def delete(self, request, proposal_id):
		exchange_proposal = get_object_or_404(ExchangeProposal, id=proposal_id)
		exchange_proposal.delete()
		return Response(status=status.HTTP_200_OK,
		                data={"message": f"object with id {proposal_id} deleted"})

	@swagger_auto_schema(
		operation_description="Изменение объекта предложения",
		responses={
			202: UpdateExchangeProposalSerializer,
			400: "bad request",
			404: "proposal with proposal_id is not found"
		}
	)
	def put(self, request, proposal_id):
		data = request.data
		if not data:
			return Response(status=status.HTTP_400_BAD_REQUEST,
			                data={"message": "body is empty"})

		exchange_proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

		serializer = UpdateExchangeProposalSerializer(data=data, instance=exchange_proposal)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(status=status.HTTP_202_ACCEPTED,
		                data=serializer.data)



class SearchAdView(APIView):
	@swagger_auto_schema(
		operation_description="Поиск рекламы",
		manual_parameters=[
			openapi.Parameter(
				"category",
				openapi.IN_QUERY,
				description="категория",
				type=openapi.TYPE_INTEGER
			),
			openapi.Parameter(
				"condition",
				openapi.IN_QUERY,
				description="условия",
				type=openapi.TYPE_STRING
			),
			openapi.Parameter(
				"title",
				openapi.IN_QUERY,
				description="название",
				type=openapi.TYPE_STRING
			),
			openapi.Parameter(
				"description",
				openapi.IN_QUERY,
				description="описание",
				type=openapi.TYPE_STRING
			),
			openapi.Parameter(
				"page_size",
				openapi.IN_QUERY,
				description="размер страницы",
				type=openapi.TYPE_INTEGER
			),
			openapi.Parameter(
				"page",
				openapi.IN_QUERY,
				description="номер страницы",
				type=openapi.TYPE_INTEGER
			),
		],
		response={
			200: AdSerializer,
		}
	)
	def get(self, request):
		queryset = Ad.objects.all()

		category = self.request.query_params.get("category")
		condition = self.request.query_params.get("condition")
		title = self.request.query_params.get("title")
		description = self.request.query_params.get("description")
		page_size = self.request.query_params.get("page_size", 20)

		filtered_data = get_filtered_data(queryset,
	                                      category,
	                                      description,
	                                      condition,
	                                      title)

		paginated_data = get_paginated_data(page_size,
		                                    filtered_data,
		                                    request)

		serializer = AdSerializer(paginated_data, many=True)

		return Response(data=serializer.data,
		                status=status.HTTP_200_OK)