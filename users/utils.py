from django.contrib.auth import authenticate, login
from users.models import User


def login_user(request,
	          username,
	          password):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return None, "user does not exists"

	if user.check_password(password):
		login(request, user)
		return user, "registered"

	return None, "password not match"
