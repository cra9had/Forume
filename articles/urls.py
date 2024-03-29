from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "articles"

urlpatterns = [
    path('', views.index, name="index"),
    path('auth', views.auth, name="auth"),
    path('register', views.register, name="register"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('article/<int:id>/', views.post_view, name="id"),
    path('article/<int:id>/like', views.post_like, name="post_like"),
    path('article/<int:id>/read', views.read_article, name="read_article"),
]
