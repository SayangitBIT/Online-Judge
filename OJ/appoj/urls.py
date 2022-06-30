from django.urls import path
from appoj.views import login_view, register
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', login_view.as_view()),
    path('register', register.as_view()),
    path('problems', views.problems, name='problems'),
    path('logout', views.logout_view, name='logout')
]