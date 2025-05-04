from django.urls import path
from .views import LoginUserView, UserView, LogoutUserView

urlpatterns = [
	path("", UserView.as_view(), name="user_view"),
	path("login/", LoginUserView.as_view(), name="login_view"),
	path("logout/", LogoutUserView.as_view(), name="logout_view"),
]