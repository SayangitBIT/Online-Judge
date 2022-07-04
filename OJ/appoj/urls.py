from django.urls import path
from appoj.views import login_view, register, to_problems
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', login_view.as_view()),
    path('register', register.as_view()),
    path('problems', views.problems, name='problems'),
    path('submissions', views.submissions_view, name='submissions'),
    path('problems/<int:p_no>/', to_problems.as_view()),
    path('logout', views.logout_view, name='logout')
]