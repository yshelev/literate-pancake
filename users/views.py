import json

from django.contrib.auth import logout
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import User
from users.serializers import UserSerializer, UserCreateSerializer
from users.utils import login_user


class UserView(APIView):
	@swagger_auto_schema(
		operation_description="create user",
		request_body=UserCreateSerializer,
		responses={
			201: UserCreateSerializer,
			400: "bad data"
		}
	)
	def post(self, request):
		data = request.data
		if not data:
			return Response(data={"message": "bad data"},
			                status=status.HTTP_400_BAD_REQUEST)

		serializer = UserCreateSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(data=serializer.data,
		                status=status.HTTP_201_CREATED)

	@swagger_auto_schema(
		operation_description="get user by id",
		manual_parameters=[
			openapi.Parameter(
				'id',
				openapi.IN_QUERY,
				description="search by id",
				type=openapi.TYPE_INTEGER
			)],
		responses={
			200: "return filtered objects",
			404: "user does not exists"
		}
	)
	def get(self, request):
		id_ = request.query_params.get("id")

		try:
			user = User.objects.get(id=id_)
		except User.DoesNotExist:
			return Response(data={"message": "user does not exists"},
			                status=status.HTTP_404_NOT_FOUND)

		serializer = UserSerializer(instance=user)

		return Response(status=status.HTTP_200_OK,
		                data=serializer.data)

class LoginUserView(APIView):
	@swagger_auto_schema(
		operation_description="login user",
		request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
        },
    ),
		responses={
			200: "login user",
			400: "bad data",
			404: "user not found or password doesnt match"
		}
	)
	def post(self, request):
		data = request.data
		if not data:
			return Response(data={"message": "bad data"},
			                status=status.HTTP_400_BAD_REQUEST)

		username = data.get("username")
		password = data.get("password")

		user, message = login_user(request,
		                          username,
		                          password)

		if not user:
			return Response(data={"message": message},
			                status=status.HTTP_404_NOT_FOUND)

		serializer = UserSerializer(instance=user)

		return Response(data=serializer.data,
		                status=status.HTTP_200_OK)

class LogoutUserView(APIView):
	@swagger_auto_schema(
		operation_description="user logout",
		responses={
			200: "logout successfully",
		}
	)
	def post(self, request):
		logout(request)
		return Response(data={"message": "logout successfully"},
		                status=status.HTTP_200_OK)

