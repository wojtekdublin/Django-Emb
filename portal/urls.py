from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('salary_calculator', views.salary_calculator, name='salary_calculator'),
    path('translator', views.translator, name='translator'),
    path('blog', views.blog, name="blog"),
    path('post/<str:pk>', views.post, name="post"),
]
