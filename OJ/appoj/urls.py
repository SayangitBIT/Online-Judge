from django.urls import path
from appoj.views import login, register
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', login.as_view()),
    path('register', register.as_view()),
    path('problems', views.problems, name='problems'),
]